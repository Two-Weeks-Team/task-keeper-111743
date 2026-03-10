import { useEffect, useState } from 'react';
import { generateSubtasks, type Subtask } from '@/lib/api';

type Props = {
  taskId: string;
  onClose: () => void;
};

export default function SubtaskModal({ taskId, onClose }: Props) {
  const [subtasks, setSubtasks] = useState<Subtask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchSubtasks() {
      try {
        const data = await generateSubtasks(taskId);
        setSubtasks(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchSubtasks();
  }, [taskId]);

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-70 z-50">
      <div className="bg-gray-800 p-6 rounded w-full max-w-md">
        <h3 className="text-xl font-semibold mb-4">Generated Subtasks</h3>
        {loading && <p className="text-gray-400">Generating…</p>}
        {error && <p className="text-red-400">{error}</p>}
        {!loading && !error && (
          <ul className="list-disc list-inside space-y-2">
            {subtasks.map((s) => (
              <li key={s.id}>{s.title}</li>
            ))}
          </ul>
        )}
        <button
          onClick={onClose}
          className="mt-4 px-4 py-2 bg-blue-600 rounded hover:bg-blue-500"
        >
          Close
        </button>
      </div>
    </div>
  );
}
