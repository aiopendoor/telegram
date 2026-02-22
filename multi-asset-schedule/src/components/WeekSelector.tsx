import styles from './WeekSelector.module.css';

interface WeekSelectorProps {
    currentWeek: number;
    weeks: Array<{ weekNumber: number; startDate: string; endDate: string }>;
    onWeekChange: (week: number) => void;
}

export default function WeekSelector({ currentWeek, weeks, onWeekChange }: WeekSelectorProps) {
    const formatDateRange = (startDate: string, endDate: string) => {
        const start = new Date(startDate);
        const end = new Date(endDate);

        const formatDate = (date: Date) => {
            const month = date.getMonth() + 1;
            const day = date.getDate();
            return `${month}.${day}`;
        };

        return `${formatDate(start)} ~ ${formatDate(end)}`;
    };

    const getWeekLabel = (weekNumber: number) => {
        return weekNumber === 1 ? '이번주' : '다음주';
    };

    return (
        <div className={styles.container}>
            {weeks.map((week) => (
                <button
                    key={week.weekNumber}
                    className={`${styles.tab} ${currentWeek === week.weekNumber ? styles.active : ''}`}
                    onClick={() => onWeekChange(week.weekNumber)}
                >
                    <span className={styles.label}>{getWeekLabel(week.weekNumber)}</span>
                    <span className={styles.dateRange}>
                        ({formatDateRange(week.startDate, week.endDate)})
                    </span>
                </button>
            ))}
        </div>
    );
}
