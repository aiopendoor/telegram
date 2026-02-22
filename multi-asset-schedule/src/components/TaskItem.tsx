import { Task } from '@/lib/types';
import EditableText from './EditableText';
import styles from './TaskItem.module.css';

interface TaskItemProps {
    task: Task;
    onToggle: (taskId: string) => void;
    onTaskUpdate: (taskId: string, updates: Partial<Task>) => void;
    onDelete?: () => void;
}

export default function TaskItem({ task, onToggle, onTaskUpdate, onDelete }: TaskItemProps) {
    const handleChange = () => {
        onToggle(task.id);
    };

    const handleDescriptionSave = (newDescription: string) => {
        onTaskUpdate(task.id, { description: newDescription });
    };


    return (
        <div className={`${styles.taskItem} ${task.completed ? styles.completed : ''}`}>
            <label className={styles.checkboxLabel}>
                <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={handleChange}
                    className={styles.checkbox}
                />
                <span className={styles.checkmark}></span>
                <EditableText
                    value={task.description}
                    onSave={handleDescriptionSave}
                    className={styles.description}
                    multiline={true}
                />
            </label>
            {onDelete && (
                <button className={styles.deleteButton} onClick={onDelete} title="할일 삭제">
                    ×
                </button>
            )}
        </div>
    );
}
