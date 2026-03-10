import { useEffect, useState } from 'react';
import TaskInputForm from '@/components/TaskInputForm';
import SubtaskModal from '@/components/SubtaskModal';
import type { Task } from '@/types';

export default function HomePage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);

  const addTask = (task: Task) => {
    setTasks((prev) => [...prev, task]);
  };

  return (
    <main className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">Task Keeper</h1>
      <TaskInputForm onTaskCreated={addTask} />
      <section className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">Your Tasks</h2>
        {tasks.length === 0 ? (
          <p className="text-gray-400">No tasks yet. Create one above.</p>
        ) : (
          <ul className="space-y-3">
            {tasks.map((t) => (
              <li
                key={t.task_id}
                className="p-4 bg-gray-800 rounded hover:bg-gray-700 cursor-pointer"
                onClick={() => setSelectedTaskId(t.task_id)}
              >
                <div className="flex justify-between items-center">
                  <span className="font-medium">{t.title}</span>
                  {t.due_date && (
                    <span className="text-sm text-gray-400">Due {new Date(t.due_date).toLocaleString()}</span>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
      {selectedTaskId && (
        <SubtaskModal taskId={selectedTaskId} onClose={() => setSelectedTaskId(null)} />
      )}
    </main>
  );
}
