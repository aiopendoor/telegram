import WeeklySchedule from '@/components/WeeklySchedule';
import PasswordGate from '@/components/PasswordGate';
import styles from './page.module.css';

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <PasswordGate>
          <WeeklySchedule />
        </PasswordGate>
      </main>
    </div>
  );
}

