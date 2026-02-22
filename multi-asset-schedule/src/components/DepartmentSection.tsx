'use client';

import { Department, Task } from '@/lib/types';
import TaskItem from './TaskItem';
import ProgressBar from './ProgressBar';
import styles from './DepartmentSection.module.css';

interface DepartmentSectionProps {
    department: Department;
    tasks: Task[];
    onTaskToggle: (taskId: string) => void;
    onTaskUpdate: (taskId: string, updates: Partial<Task>) => void;
}

export default function DepartmentSection({ department, tasks, onTaskToggle, onTaskUpdate }: DepartmentSectionProps) {
    const completedCount = tasks.filter(t => t.completed).length;
    const totalCount = tasks.length;

    return (
        <div className={styles.section}>
            <div className={styles.header}>
                <h3 className={styles.title}>{department}</h3>
                <ProgressBar total={totalCount} completed={completedCount} />
            </div>

            <div className={styles.taskList}>
                {tasks.length > 0 ? (
                    tasks.map(task => (
                        <TaskItem
                            key={task.id}
                            task={task}
                            onToggle={onTaskToggle}
                            onTaskUpdate={onTaskUpdate}
                        />
                    ))
                ) : (
                    <p className={styles.emptyMessage}>등록된 업무가 없습니다.</p>
                )}
            </div>
        </div>
    );
}
