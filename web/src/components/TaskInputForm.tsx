import { useState } from 'react';
import { createTask, type TaskResponse } from '@/lib/api';

type Props = {
  onTaskCreated: (task: TaskResponse) => void;
};

export default function TaskInputForm({ onTaskCreated }: Props) {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const task = await createTask(text.trim());
      onTaskCreated(task);
      setText('');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-2">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Describe your task, e.g. ‘Prepare presentation for client meeting next Monday at 10am’"
        className="flex-1 p-2 rounded bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        rows={2}
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading}
        className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-500 disabled:opacity-50"
      >
        {loading ? 'Creating…' : 'Add Task'}
      </button>
      {error && <p className="text-red-400 mt-1">{error}</p>}
    </form>
  );
}
