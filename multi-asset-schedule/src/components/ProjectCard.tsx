'use client';

import { Project, Task, WorkflowStep } from '@/lib/types';
import WorkflowChart from './WorkflowChart';
import TaskItem from './TaskItem';
import EditableText from './EditableText';
import styles from './ProjectCard.module.css';

interface ProjectCardProps {
    project: Project;
    weekNumber: number;
    onTaskToggle: (taskId: string) => void;
    onProjectUpdate: (updates: Partial<Project>) => void;
    onTaskUpdate: (taskId: string, updates: Partial<Task>) => void;
    onWorkflowStepUpdate: (stepId: string, updates: Partial<WorkflowStep>) => void;
    onWorkflowStepDelete: (stepId: string) => void;
    onAddTask: () => void;
    onAddStep: () => void;
    onToggleActiveStep: (stepId: string) => void;
    onToggleComplete: () => void;
    onDeleteProject: () => void;
    onDeleteTask: (taskId: string) => void;
}

export default function ProjectCard({
    project,
    weekNumber,
    onTaskToggle,
    onProjectUpdate,
    onTaskUpdate,
    onWorkflowStepUpdate,
    onWorkflowStepDelete,
    onAddTask,
    onAddStep,
    onToggleActiveStep,
    onToggleComplete,
    onDeleteProject,
    onDeleteTask
}: ProjectCardProps) {
    const weekTasks = project.tasks.filter(task => task.weekNumber === weekNumber);

    // 진행률 계산: 현재 활성 단계 순서 / 전체 단계 수
    const totalSteps = project.workflowSteps.length;
    const activeStepIndex = project.workflowSteps.findIndex(s => s.id === project.activeStepId);
    const currentStepNum = activeStepIndex !== -1 ? activeStepIndex + 1 : 0;
    const percentage = totalSteps > 0 ? Math.round((currentStepNum / totalSteps) * 100) : 0;

    const handleProjectNameSave = (newName: string) => {
        onProjectUpdate({ name: newName });
    };

    const handleDepartmentSave = (newDept: string) => {
        onProjectUpdate({ department: newDept as Project['department'] });
    };

    return (
        <div className={`${styles.card} ${project.isCompleted ? styles.projectCompleted : ''}`}>
            <div className={styles.header}>
                <div className={styles.headerTitleGroup}>
                    <EditableText
                        value={project.department}
                        onSave={handleDepartmentSave}
                        tag="h3"
                        className={styles.department}
                    />
                    <button
                        className={`${styles.completeButton} ${project.isCompleted ? styles.active : ''}`}
                        onClick={onToggleComplete}
                        title={project.isCompleted ? "프로젝트 진행 중으로 변경" : "프로젝트 완료 처리"}
                    >
                        {project.isCompleted ? "✅ Completed" : "Mark Completed"}
                    </button>
                    <button
                        className={styles.deleteProjectButton}
                        onClick={onDeleteProject}
                        title="프로젝트 삭제"
                    >
                        🗑️
                    </button>
                </div>
                <div className={styles.progress}>
                    {currentStepNum}/{totalSteps} ({percentage}%)
                </div>
            </div>

            {/* 워크플로우 차트 */}
            <div className={styles.workflowContainer}>
                <WorkflowChart
                    steps={project.workflowSteps}
                    projectName={project.name}
                    activeStepId={project.activeStepId}
                    onProjectNameSave={handleProjectNameSave}
                    onStepUpdate={onWorkflowStepUpdate}
                    onToggleActiveStep={onToggleActiveStep}
                />
                <div className={styles.workflowActions}>
                    <button className={styles.addStepButton} onClick={onAddStep}>
                        + 단계 추가
                    </button>
                    <button
                        className={styles.deleteStepButton}
                        onClick={() => {
                            if (project.workflowSteps.length > 1) {
                                if (confirm('마지막 단계를 삭제하시겠습니까?')) {
                                    const lastStep = project.workflowSteps[project.workflowSteps.length - 1];
                                    onWorkflowStepDelete(lastStep.id);
                                }
                            } else {
                                alert('최소 한 개의 단계는 필요합니다.');
                            }
                        }}
                    >
                        - 단계 삭제
                    </button>
                </div>
            </div>

            {/* 세부 할일 체크리스트 */}
            <div className={styles.taskSection}>
                <div className={styles.taskHeaderRow}>
                    <h5 className={styles.taskHeader}>세부 할일</h5>
                    <button className={styles.addTaskButton} onClick={onAddTask}>
                        + 할일 추가
                    </button>
                </div>
                <div className={styles.taskList}>
                    {weekTasks.length > 0 ? (
                        weekTasks.map(task => (
                            <TaskItem
                                key={task.id}
                                task={task}
                                onToggle={onTaskToggle}
                                onTaskUpdate={onTaskUpdate}
                                onDelete={() => onDeleteTask(task.id)}
                            />
                        ))
                    ) : (
                        <p className={styles.emptyMessage}>등록된 업무가 없습니다.</p>
                    )}
                </div>
            </div>
        </div>
    );
}
