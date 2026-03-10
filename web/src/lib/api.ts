export interface TaskResponse {
  task_id: string;
  title: string;
  due_date?: string;
  priority?: string;
  category?: string;
}

export async function createTask(naturalLanguageText: string): Promise<TaskResponse> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ natural_language_text: naturalLanguageText }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.message || 'Failed to create task');
  }
  return res.json();
}

export interface Subtask {
  id: string;
  title: string;
}

export async function generateSubtasks(taskId: string): Promise<Subtask[]> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${taskId}/subtasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task_id: taskId }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.message || 'Failed to generate subtasks');
  }
  const data = await res.json();
  return data.subtasks;
}
