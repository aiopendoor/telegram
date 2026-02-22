'use client';

import { useState, useEffect } from 'react';
import styles from './PasswordGate.module.css';

interface PasswordGateProps {
    children: React.ReactNode;
}

export default function PasswordGate({ children }: PasswordGateProps) {
    const [password, setPassword] = useState('');
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(true);

    // 환경 변수나 설정값에서 비밀번호 가져오기 (기본값 설정)
    const CORRECT_PASSWORD = process.env.NEXT_PUBLIC_APP_PASSWORD || '3313';

    useEffect(() => {
        const checkSession = () => {
            const session = localStorage.getItem('app-session');
            if (session === 'authenticated') {
                setIsAuthenticated(true);
            }
            setIsLoading(false);
        };
        checkSession();
    }, []);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (password === CORRECT_PASSWORD) {
            setIsAuthenticated(true);
            localStorage.setItem('app-session', 'authenticated');
            setError('');
        } else {
            setError('비밀번호가 올바르지 않습니다.');
            setPassword('');
        }
    };

    if (isLoading) return null;

    if (!isAuthenticated) {
        return (
            <div className={styles.overlay}>
                <div className={styles.container}>
                    <div className={styles.icon}>🔒</div>
                    <h2>Multi-Asset Schedule</h2>
                    <p>본 페이지는 보호되어 있습니다.<br />비밀번호를 입력해 주세요.</p>
                    <form onSubmit={handleSubmit} className={styles.form}>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="비밀번호 입력"
                            className={styles.input}
                            autoFocus
                        />
                        {error && <p className={styles.error}>{error}</p>}
                        <button type="submit" className={styles.button}>
                            접속하기
                        </button>
                    </form>
                    <p className={styles.footer}>© 2024 Multi-Asset Team</p>
                </div>
            </div>
        );
    }

    return <>{children}</>;
}
