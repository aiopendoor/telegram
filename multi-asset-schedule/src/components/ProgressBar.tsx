import styles from './ProgressBar.module.css';

interface ProgressBarProps {
    total: number;
    completed: number;
    showPercentage?: boolean;
}

export default function ProgressBar({ total, completed, showPercentage = true }: ProgressBarProps) {
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

    return (
        <div className={styles.container}>
            <div className={styles.barWrapper}>
                <div
                    className={styles.bar}
                    style={{ width: `${percentage}%` }}
                />
            </div>
            <div className={styles.label}>
                <span className={styles.count}>{completed}/{total}</span>
                {showPercentage && (
                    <span className={styles.percentage}>{percentage}%</span>
                )}
            </div>
        </div>
    );
}
