import os
import json
import re
import logging
from typing import Any, Dict, List
import httpx

logger = logging.getLogger(__name__)

def _extract_json(text: str) -> str:
    """Extract JSON payload from LLM response, handling markdown code fences."""
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()

async def _call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    """Make a request to DigitalOcean Serverless Inference.
    Returns a dict parsed from the model's JSON output or a fallback.
    """
    api_key = os.getenv("DIGITALOCEAN_INFERENCE_KEY")
    model = os.getenv("DO_INFERENCE_MODEL", "openai-gpt-oss-120b")
    url = "https://inference.do-ai.run/v1/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "max_completion_tokens": max_tokens,
        "stream": False,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Typical OpenAI‑style response
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            raw_json = _extract_json(content)
            return json.loads(raw_json)
    except Exception as exc:
        logger.error("AI inference failed: %s", exc)
        return {"note": "AI service temporarily unavailable."}

# ---------------------------------------------------------------------------
# Public helper functions used by route handlers
# ---------------------------------------------------------------------------
async def parse_natural_language(text: str) -> Dict[str, Any]:
    """Parse a free‑form task description into structured fields.
    Expected output keys: title, due_date (ISO‑8601 string or null),
    priority (low|medium|high), category.
    """
    system_prompt = (
        "You are an assistant that extracts task details from natural language. "
        "Return a JSON object with the following keys: title (string), "
        "due_date (ISO‑8601 string or null), priority (low, medium, high or null), "
        "category (string or null). Do NOT include any additional text."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text},
    ]
    return await _call_inference(messages, max_tokens=512)

async def generate_subtasks(task_description: str) -> Dict[str, Any]:
    """Given a high‑level task description, generate 3‑5 concise subtask titles.
    Expected output: {"subtasks": ["subtask 1", "subtask 2", ...]}
    """
    system_prompt = (
        "You are an assistant that creates a short list of subtask titles for a given task. "
        "Return a JSON object with a single key \"subtasks\" containing an array of strings. "
        "Do not add explanations or extra fields."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task_description},
    ]
    return await _call_inference(messages, max_tokens=512)
