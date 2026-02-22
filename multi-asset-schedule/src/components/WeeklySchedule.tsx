'use client';

import { useState, useEffect } from 'react';
import { StorageData, WeekData, Project, Task, WorkflowStep } from '@/lib/types';
import { loadFromStorage, saveToStorage, createInitialData } from '@/lib/storage'; // createInitialData is used now
import ProjectCard from './ProjectCard';
import EditableText from './EditableText';
import styles from './WeeklySchedule.module.css';

// Assuming migrateData is defined elsewhere or should be replaced by createInitialData
// If migrateData is not defined, this will cause a runtime error.
// For the purpose of this edit, we'll assume it's a valid function that returns StorageData.
// function migrateData(): StorageData {
//     return createInitialData();
// }

export default function WeeklySchedule() {
    const [storageData, setStorageData] = useState<StorageData | null>(null);
    const [loading, setLoading] = useState(true);
    const [pageTitle, setPageTitle] = useState('멀티에셋본부 주간보고');

    // 1. 초기 데이터 로드 및 보정
    useEffect(() => {
        const initData = async () => {
            setLoading(true);
            try {
                let data = await loadFromStorage();
                if (!data) {
                    data = createInitialData();
                }
                const currentData: StorageData = data;

                // 데이터 보정: 동일 접두사 프로젝트 간 정보(이름, 스텝 등) 강제 동기화
                let changed = false;
                if (data.weeks && data.weeks.length > 0) {
                    const syncedWeeks = data.weeks.map((week: WeekData) => {
                        const updatedProjects = week.projects.map(project => {
                            const prefix = project.id.split('-').slice(0, 2).join('-');
                            // 이번주 프로젝트를 기준으로 삼음
                            const sourceProject = currentData.weeks[0].projects.find(p => p.id.startsWith(prefix));
                            if (sourceProject && project.id !== sourceProject.id) {
                                const stepsMatch = JSON.stringify(project.workflowSteps) === JSON.stringify(sourceProject.workflowSteps);
                                if (project.name !== sourceProject.name || !stepsMatch || project.activeStepId !== sourceProject.activeStepId) {
                                    changed = true;
                                    return {
                                        ...project,
                                        name: sourceProject.name,
                                        department: sourceProject.department,
                                        workflowSteps: sourceProject.workflowSteps,
                                        activeStepId: sourceProject.activeStepId,
                                        isCompleted: sourceProject.isCompleted
                                    };
                                }
                            }
                            return project;
                        });
                        return { ...week, projects: updatedProjects };
                    });

                    if (changed) {
                        console.log('Fixed data inconsistency during load');
                        data = { ...data, weeks: syncedWeeks };
                    }
                }

                setStorageData(data); // data is guaranteed to be StorageData here

                // 페이지 제목 로드
                const savedTitle = localStorage.getItem('page-title');
                if (savedTitle) {
                    setPageTitle(savedTitle);
                }
            } catch (error) {
                console.error('Initialization failed:', error);
                // Fallback to initial data if loading fails
                setStorageData(createInitialData());
            } finally {
                setLoading(false);
            }
        };
        initData();
    }, []);

    // 2. 데이터 변경 시 자동 저장
    useEffect(() => {
        const saveData = async () => {
            if (storageData && !loading) {
                await saveToStorage(storageData);
            }
        };
        saveData();
    }, [storageData, loading]);

    const handleTitleSave = (newTitle: string) => {
        setPageTitle(newTitle);
        localStorage.setItem('page-title', newTitle);
    };

    const handleTaskToggle = (taskId: string) => {
        if (!storageData) return;

        let updatedWeeks = [...storageData.weeks];
        let taskFound = false;

        updatedWeeks = updatedWeeks.map(week => {
            const updatedProjects = week.projects.map(project => {
                const updatedTasks = project.tasks.map(task => {
                    if (task.id === taskId) {
                        taskFound = true;
                        const newCompleted = !task.completed;
                        return {
                            ...task,
                            completed: newCompleted,
                            completedAt: newCompleted ? new Date().toISOString() : undefined,
                            status: newCompleted ? 'completed' as const : 'pending' as const
                        };
                    }
                    return task;
                });

                return {
                    ...project,
                    tasks: updatedTasks
                };
            });

            return {
                ...week,
                projects: updatedProjects,
                updatedAt: taskFound ? new Date().toISOString() : week.updatedAt
            };
        });

        if (taskFound) {
            setStorageData({
                ...storageData,
                weeks: updatedWeeks,
                lastSync: new Date().toISOString()
            });
        }
    };

    // 프로젝트 완료 상태 토글 및 하단 정렬 로직
    const handleToggleProjectCompletion = (projectId: string) => {
        if (!storageData) return;

        const updatedWeeks = storageData.weeks.map(week => {
            const updatedProjects = week.projects.map(project => {
                if (project.id === projectId || project.id.split('-').slice(0, 2).join('-') === projectId.split('-').slice(0, 2).join('-')) {
                    return { ...project, isCompleted: !project.isCompleted };
                }
                return project;
            });
            return { ...week, projects: updatedProjects, updatedAt: new Date().toISOString() };
        });

        setStorageData({
            ...storageData,
            weeks: updatedWeeks,
            lastSync: new Date().toISOString()
        });
    };

    // 활성 단계 변경 (이번주/다음주 동일 프로젝트 완벽 동기화)
    const handleToggleActiveStep = (projectId: string, stepId: string) => {
        if (!storageData) return;

        const projectPrefix = projectId.split('-').slice(0, 2).join('-');

        const updatedWeeks = storageData.weeks.map(week => {
            const updatedProjects = week.projects.map(project => {
                const currentPrefix = project.id.split('-').slice(0, 2).join('-');
                if (currentPrefix === projectPrefix) {
                    return { ...project, activeStepId: stepId };
                }
                return project;
            });
            return { ...week, projects: updatedProjects, updatedAt: new Date().toISOString() };
        });

        setStorageData({
            ...storageData,
            weeks: updatedWeeks,
            lastSync: new Date().toISOString()
        });
    };

    const handleProjectUpdate = (weekNumber: number, projectId: string, updates: Partial<Project>) => {
        if (!storageData) return;

        const projectPrefix = projectId.split('-').slice(0, 2).join('-');

        const updatedWeeks = storageData.weeks.map(week => {
            const updatedProjects = week.projects.map(project => {
                const currentPrefix = project.id.split('-').slice(0, 2).join('-');

                // 프로젝트명이나 부서명 수정 시 모든 주차의 동일 프로젝트에 반영
                if (currentPrefix === projectPrefix) {
                    return { ...project, ...updates };
                }
                return project;
            });

            return {
                ...week,
                projects: updatedProjects,
                updatedAt: new Date().toISOString()
            };
        });

        setStorageData({
            ...storageData,
            weeks: updatedWeeks,
            lastSync: new Date().toISOString()
        });
    };

    const handleTaskUpdate = (weekNumber: number, projectId: string, taskId: string, updates: Partial<Task>) => {
        if (!storageData) return;

        const updatedWeeks = storageData.weeks.map(week => {
            if (week.weekNumber !== weekNumber) return week;

            const updatedProjects = week.projects.map(project => {
                if (project.id !== projectId) return project;

                const updatedTasks = project.tasks.map(task => {
                    if (task.id !== taskId) return task;
                    return { ...task, ...updates };
                });

                return {
                    ...project,
                    tasks: updatedTasks
                };
            });

            return {
                ...week,
                projects: updatedProjects,
                updatedAt: new Date().toISOString()
            };
        });

        setStorageData({
            ...storageData,
            weeks: updatedWeeks,
            lastSync: new Date().toISOString()
        });
    };

    const handleWorkflowStepUpdate = (
        weekNumber: number,
        projectId: string,
        stepId: string,
        updates: Partial<WorkflowStep>
    ) => {
        if (!storageData) return;

        const projectPrefix = projectId.split('-').slice(0, 2).join('-');

        // 1. 수정이 일어난 원본 스텝 목록을 먼저 만듦
        let targetWorkflowSteps: WorkflowStep[] = [];
        const foundProject = storageData.weeks.find(w => w.weekNumber === weekNumber)?.projects.find(p => p.id === projectId);
        if (foundProject) {
            targetWorkflowSteps = foundProject.workflowSteps.map(step =>
                step.id === stepId ? { ...step, ...updates } : step
            );
        } else {
            return;
        }

        // 2. 모든 주차의 해당 프로젝트에 동일한 스텝 목록 강제 적용
        const updatedWeeks = storageData.weeks.map(week => {
            const updatedProjects = week.projects.map(project => {
                if (project.id.startsWith(projectPrefix)) {
                    return { ...project, workflowSteps: targetWorkflowSteps };
                }
                return project;
            });

            return {
                ...week,
                projects: updatedProjects,
                updatedAt: new Date().toISOString()
            };
        });

        setStorageData({
            ...storageData,
            weeks: updatedWeeks,
            lastSync: new Date().toISOString()
        });
    };

    const handleAddProject = (weekNumber: number) => {
        if (!storageData) return;

        // 접두사 공유를 위한 타임스탬프
        const timestamp = Date.now();
        const prefix = `proj-${timestamp}`;
        const stepId = `step-${timestamp}-1`;

        const newProjectTemplate = (specificWeekNumber: number): Project => ({
            id: `${prefix}-w${specificWeekNumber}`,
            name: '새 프로젝트',
            department: '브릿지',
            workflowSteps: [
                { id: stepId, name: '단계 1', status: 'not-started', order: 1 }
            ],
            tasks: [],
            isCompleted: false,
            activeStepId: stepId
        });

        const updatedWeeks = storageData.weeks.map(week => ({
            ...week,
            projects: [...week.projects, newProjectTemplate(week.weekNumber)],
            updatedAt: new Date().toISOString()
        }));

        setStorageData({
            ...storageData,
            weeks: updatedWeeks,
            lastSync: new Date().toISOString()
        });
    };

    const handleAddTask = (weekNumber: number, projectId: string) => {
        if (!storageData) return;

        const newTask: Task = {
            id: `task-${Date.now()}`,
            department: '브릿지', // 프로젝트 부서로 맞춰야 함
            description: '새로운 할일',
            completed: false,
            priority: 'medium',
            status: 'pending',
            createdAt: new Date().toISOString(),
            weekNumber: weekNumber
        };

        const updatedWeeks = storageData.weeks.map(week => {
            if (week.weekNumber !== weekNumber) return week;

            const updatedProjects = week.projects.map(project => {
                if (project.id !== projectId) return project;
                newTask.department = project.department;
                return {
                    ...project,
                    tasks: [...project.tasks, newTask]
                };
            });

            return {
                ...week,
                projects: updatedProjects,
                updatedAt: new Date().toISOString()
            };
        });

        setStorageData({
            ...storageData,
            weeks: updatedWeeks,
            lastSync: new Date().toISOString()
        });
    };

    const handleAddWorkflowStep = (weekNumber: number, projectId: string) => {
        if (!storageData) return;

        const projectPrefix = projectId.split('-').slice(0, 2).join('-');
        const timestamp = Date.now();
        const newStepId = `step-${timestamp}`;

        // 1. 기준 프로젝트의 스텝 목록 가져오기 및 추가
        const sourceProject = storageData.weeks.find(w => w.weekNumber === weekNumber)?.projects.find(p => p.id === projectId);
        if (!sourceProject) return;

        const newSteps: WorkflowStep[] = [
            ...sourceProject.workflowSteps,
            { id: newStepId, name: '새 단계', status: 'not-started', order: sourceProject.workflowSteps.length + 1 }
        ];

        // 2. 모든 주차에 동일한 스텝 목록 강제 주입
        const updatedWeeks = storageData.weeks.map(week => {
            const updatedProjects = week.projects.map(project => {
                const currentPrefix = project.id.split('-').slice(0, 2).join('-');
                if (currentPrefix === projectPrefix) {
                    return { ...project, workflowSteps: newSteps };
                }
                return project;
            });

            return {
                ...week,
                projects: updatedProjects,
                updatedAt: new Date().toISOString()
            };
        });

        setStorageData({
            ...storageData,
            weeks: updatedWeeks,
            lastSync: new Date().toISOString()
        });
    };

    const handleDeleteWorkflowStep = (weekNumber: number, projectId: string, stepId: string) => {
        if (!storageData) return;

        const projectPrefix = projectId.split('-').slice(0, 2).join('-');

        // 1. 기준 프로젝트에서 해당 스텝 삭제 및 순서 재조정
        const sourceProject = storageData.weeks.find(w => w.weekNumber === weekNumber)?.projects.find(p => p.id === projectId);
        if (!sourceProject) return;

        const filteredSteps = sourceProject.workflowSteps.filter(s => s.id !== stepId);
        const reorderedSteps = filteredSteps.map((s, idx) => ({ ...s, order: idx + 1 }));

        // 2. 삭제된 단계가 활성 단계였다면 다른 단계로 변경
        let newActiveStepId = sourceProject.activeStepId;
        if (newActiveStepId === stepId) {
            newActiveStepId = reorderedSteps.length > 0 ? reorderedSteps[0].id : undefined;
        }

        // 3. 모든 주차에 동일하게 적용
        const updatedWeeks = storageData.weeks.map(week => {
            const updatedProjects = week.projects.map(project => {
                const currentPrefix = project.id.split('-').slice(0, 2).join('-');
                if (currentPrefix === projectPrefix) {
                    return {
                        ...project,
                        workflowSteps: reorderedSteps,
                        activeStepId: newActiveStepId === stepId ? (reorderedSteps.length > 0 ? reorderedSteps[0].id : undefined) : newActiveStepId
                    };
                }
                return project;
            });

            return {
                ...week,
                projects: updatedProjects,
                updatedAt: new Date().toISOString()
            };
        });

        setStorageData({
            ...storageData,
            weeks: updatedWeeks,
            lastSync: new Date().toISOString()
        });
    };

    const handleDeleteProject = (projectId: string) => {
        if (!storageData) return;

        if (!confirm('정말로 이 프로젝트를 삭제하시겠습니까? 모든 주차의 데이터가 삭제됩니다.')) {
            return;
        }

        const projectPrefix = projectId.split('-').slice(0, 2).join('-');

        const updatedWeeks = storageData.weeks.map(week => ({
            ...week,
            projects: week.projects.filter(p => !p.id.startsWith(projectPrefix)),
            updatedAt: new Date().toISOString()
        }));

        setStorageData({
            ...storageData,
            weeks: updatedWeeks,
            lastSync: new Date().toISOString()
        });
    };

    const handleDeleteTask = (weekNumber: number, projectId: string, taskId: string) => {
        if (!storageData) return;

        if (!confirm('이 할 일을 삭제하시겠습니까?')) {
            return;
        }

        const updatedWeeks = storageData.weeks.map(week => {
            if (week.weekNumber !== weekNumber) return week;

            const updatedProjects = week.projects.map(project => {
                if (project.id !== projectId) return project;

                return {
                    ...project,
                    tasks: project.tasks.filter(t => t.id !== taskId)
                };
            });

            return {
                ...week,
                projects: updatedProjects,
                updatedAt: new Date().toISOString()
            };
        });

        setStorageData({
            ...storageData,
            weeks: updatedWeeks,
            lastSync: new Date().toISOString()
        });
    };

    // const sortProjects = (projects: Project[]) => {
    //     return [...projects].sort((a, b) => {
    //         if (a.isCompleted && !b.isCompleted) return 1;
    //         if (!a.isCompleted && b.isCompleted) return -1;
    //         return 0;
    //     });
    // };

    if (loading) {
        return (
            <div className={styles.loading}>
                <div className={styles.spinner}></div>
                <p>데이터를 불러오는 중...</p>
            </div>
        );
    }

    if (!storageData || storageData.weeks.length < 2) {
        return (
            <div className={styles.error}>
                <p>데이터를 불러올 수 없습니다.</p>
            </div>
        );
    }

    const week1 = storageData.weeks[0];
    const week2 = storageData.weeks[1];

    // 모든 고유 프로젝트 식별자 추출 (동기화된 프로젝트들)
    const allProjectPrefixes = Array.from(new Set([
        ...week1.projects.map(p => p.id.split('-').slice(0, 2).join('-')),
        ...week2.projects.map(p => p.id.split('-').slice(0, 2).join('-'))
    ]));

    // 정렬: 미완료 프로젝트 우선, 그 후 접두사순
    const sortedPrefixes = allProjectPrefixes.sort((a, b) => {
        const projA = week1.projects.find(p => p.id.startsWith(a)) || week2.projects.find(p => p.id.startsWith(a));
        const projB = week1.projects.find(p => p.id.startsWith(b)) || week2.projects.find(p => p.id.startsWith(b));

        if (projA?.isCompleted && !projB?.isCompleted) return 1;
        if (!projA?.isCompleted && projB?.isCompleted) return -1;
        return a.localeCompare(b);
    });

    return (
        <div className={styles.container}>
            <header className={styles.mainHeader}>
                <EditableText
                    value={pageTitle}
                    onSave={handleTitleSave}
                    tag="h1"
                    className={styles.pageTitle}
                />
                <div className={styles.headerInfo}>
                    <div className={styles.hint}>* 모든 텍스트를 클릭하여 수정할 수 있습니다. 업무 단계를 클릭하여 현재 단계를 표시하세요.</div>
                    <div className={styles.lastUpdate}>마지막 업데이트: {new Date(storageData.lastSync).toLocaleString('ko-KR')}</div>
                </div>
            </header>

            <div className={styles.scheduleGrid}>
                {/* 그리드 헤더: 주차 타이틀 */}
                <div className={styles.gridRowHeader}>
                    <div className={styles.weekHeaderCell}>
                        <h2 className={styles.weekTitle}>이번주</h2>
                        <p className={styles.weekDate}>
                            {formatDateRange(week1.startDate, week1.endDate)}
                        </p>
                    </div>
                    <div className={styles.weekHeaderCell}>
                        <h2 className={styles.weekTitle}>다음주</h2>
                        <p className={styles.weekDate}>
                            {formatDateRange(week2.startDate, week2.endDate)}
                        </p>
                    </div>
                </div>

                {/* 프로젝트 행들 */}
                <div className={styles.projectGrid}>
                    {sortedPrefixes.map(prefix => {
                        const p1 = week1.projects.find(p => p.id.startsWith(prefix));
                        const p2 = week2.projects.find(p => p.id.startsWith(prefix));

                        return (
                            <div key={prefix} className={styles.projectRow}>
                                <div className={styles.projectCell}>
                                    {p1 && (
                                        <ProjectCard
                                            project={p1}
                                            weekNumber={1}
                                            onTaskToggle={handleTaskToggle}
                                            onProjectUpdate={(updates) => handleProjectUpdate(1, p1.id, updates)}
                                            onTaskUpdate={(taskId, updates) => handleTaskUpdate(1, p1.id, taskId, updates)}
                                            onWorkflowStepUpdate={(stepId, updates) =>
                                                handleWorkflowStepUpdate(1, p1.id, stepId, updates)
                                            }
                                            onWorkflowStepDelete={(stepId) => handleDeleteWorkflowStep(1, p1.id, stepId)}
                                            onAddTask={() => handleAddTask(1, p1.id)}
                                            onAddStep={() => handleAddWorkflowStep(1, p1.id)}
                                            onToggleActiveStep={(stepId) => handleToggleActiveStep(p1.id, stepId)}
                                            onToggleComplete={() => handleToggleProjectCompletion(p1.id)}
                                            onDeleteProject={() => handleDeleteProject(p1.id)}
                                            onDeleteTask={(taskId) => handleDeleteTask(1, p1.id, taskId)}
                                        />
                                    )}
                                </div>
                                <div className={styles.projectCell}>
                                    {p2 && (
                                        <ProjectCard
                                            project={p2}
                                            weekNumber={2}
                                            onTaskToggle={handleTaskToggle}
                                            onProjectUpdate={(updates) => handleProjectUpdate(2, p2.id, updates)}
                                            onTaskUpdate={(taskId, updates) => handleTaskUpdate(2, p2.id, taskId, updates)}
                                            onWorkflowStepUpdate={(stepId, updates) =>
                                                handleWorkflowStepUpdate(2, p2.id, stepId, updates)
                                            }
                                            onWorkflowStepDelete={(stepId) => handleDeleteWorkflowStep(2, p2.id, stepId)}
                                            onAddTask={() => handleAddTask(2, p2.id)}
                                            onAddStep={() => handleAddWorkflowStep(2, p2.id)}
                                            onToggleActiveStep={(stepId) => handleToggleActiveStep(p2.id, stepId)}
                                            onToggleComplete={() => handleToggleProjectCompletion(p2.id)}
                                            onDeleteProject={() => handleDeleteProject(p2.id)}
                                            onDeleteTask={(taskId) => handleDeleteTask(2, p2.id, taskId)}
                                        />
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>

                {/* 추가 버튼 행 */}
                <div className={styles.addButtonsRow}>
                    <button
                        className={styles.addProjectButton}
                        onClick={() => handleAddProject(1)}
                    >
                        + 새 프로젝트 추가
                    </button>
                </div>
            </div>

            <footer className={styles.footer}>
                <p className={styles.lastUpdate}>
                    마지막 업데이트: {new Date(storageData.lastSync).toLocaleString('ko-KR')}
                </p>
            </footer>
        </div>
    );
}

function formatDateRange(startDate: string, endDate: string): string {
    const start = new Date(startDate);
    const end = new Date(endDate);

    const formatDate = (date: Date) => {
        const month = date.getMonth() + 1;
        const day = date.getDate();
        return `${month}.${day}`;
    };

    return `${formatDate(start)} ~ ${formatDate(end)}`;
}
