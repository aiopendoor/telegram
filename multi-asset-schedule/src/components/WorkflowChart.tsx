import { WorkflowStep } from '@/lib/types';
import EditableText from './EditableText';
import styles from './WorkflowChart.module.css';

interface WorkflowChartProps {
    steps: WorkflowStep[];
    projectName: string;
    activeStepId?: string;
    onProjectNameSave: (newName: string) => void;
    onStepUpdate: (stepId: string, updates: Partial<WorkflowStep>) => void;
    onToggleActiveStep: (stepId: string) => void;
}

export default function WorkflowChart({
    steps,
    projectName,
    activeStepId,
    onProjectNameSave,
    onStepUpdate,
    onToggleActiveStep
}: WorkflowChartProps) {
    const getStatusColor = (step: WorkflowStep) => {
        if (activeStepId === step.id) {
            return styles.activeStep; // 푸른색 (현재 단계)
        }
        return styles.inactiveStep; // 회색 (나머지)
    };

    const getStatusClass = (status: WorkflowStep['status']) => {
        switch (status) {
            case 'completed':
                return styles.completed;
            case 'in-progress':
                return styles.inProgress;
            case 'blocked':
                return styles.blocked;
            default:
                return styles.notStarted;
        }
    };


    // const formatDeadline = (deadline?: string) => {
    //     if (!deadline) return '';
    //     const date = new Date(deadline);
    //     return `${date.getMonth() + 1}/${date.getDate()}`;
    // };

    const sortedSteps = [...steps].sort((a, b) => a.order - b.order);

    return (
        <div className={styles.container}>
            <EditableText
                value={projectName}
                onSave={onProjectNameSave}
                tag="h4"
                className={styles.projectName}
            />
            <div className={styles.flowChart}>
                {sortedSteps.map((step, index) => (
                    <div key={step.id} className={styles.stepWrapper}>
                        <div
                            className={`${styles.step} ${getStatusColor(step)}`}
                            onClick={() => onToggleActiveStep(step.id)}
                            style={{ cursor: 'pointer' }}
                        >
                            <div className={styles.stepHeader}>
                                <span className={styles.stepNumber}>{step.order}</span>
                                <select
                                    className={`${styles.statusSelect} ${getStatusClass(step.status)}`}
                                    value={step.status}
                                    onChange={(e) => {
                                        onStepUpdate(step.id, { status: e.target.value as WorkflowStep['status'] });
                                    }}
                                    onClick={(e) => e.stopPropagation()}
                                >
                                    <option value="not-started">Pending</option>
                                    <option value="in-progress">In Progress</option>
                                    <option value="completed">Completed</option>
                                    <option value="blocked">Blocked</option>
                                </select>
                            </div>
                            <EditableText
                                value={step.name}
                                onSave={(newName) => onStepUpdate(step.id, { name: newName })}
                                className={styles.stepName}
                            />
                            <div className={styles.stepDeadline}>
                                <span>마감: </span>
                                <EditableText
                                    value={step.deadline || ''}
                                    onSave={(newDeadline) => onStepUpdate(step.id, { deadline: newDeadline })}
                                    placeholder="날짜 입력"
                                    className={styles.deadlineInput}
                                />
                            </div>
                        </div>
                        {index < sortedSteps.length - 1 && (
                            <div className={styles.arrow}>→</div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}
