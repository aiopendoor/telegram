import { NextResponse } from 'next/server';
import { StorageData } from '@/lib/types';
import { getLatestSchedule, saveSchedule } from '@/lib/db';

export async function GET() {
    try {
        const data = await getLatestSchedule();
        return NextResponse.json(data);
    } catch (error) {
        console.error('Failed to get schedule:', error);
        return NextResponse.json({ error: 'Failed to fetch data' }, { status: 500 });
    }
}

export async function POST(request: Request) {
    try {
        const data: StorageData = await request.json();
        await saveSchedule(data);
        return NextResponse.json({ success: true });
    } catch (error) {
        console.error('Failed to save schedule:', error);
        return NextResponse.json({ error: 'Failed to save data' }, { status: 500 });
    }
}
