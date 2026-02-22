'use client';

import { useState, useRef, useEffect } from 'react';
import styles from './EditableText.module.css';

interface EditableTextProps {
    value: string;
    onSave: (newValue: string) => void;
    placeholder?: string;
    multiline?: boolean;
    className?: string;
    tag?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'p' | 'span';
}

export default function EditableText({
    value,
    onSave,
    placeholder = '클릭하여 편집',
    multiline = false,
    className = '',
    tag = 'span'
}: EditableTextProps) {
    const [isEditing, setIsEditing] = useState(false);
    const [editValue, setEditValue] = useState(value);
    const inputRef = useRef<HTMLInputElement | HTMLTextAreaElement>(null);

    useEffect(() => {
        setEditValue(value);
    }, [value]);

    useEffect(() => {
        if (isEditing && inputRef.current) {
            inputRef.current.focus();
            inputRef.current.select();
        }
    }, [isEditing]);

    const handleClick = () => {
        setIsEditing(true);
    };

    const handleBlur = () => {
        setIsEditing(false);
        if (editValue.trim() !== value.trim() && editValue.trim() !== '') {
            onSave(editValue.trim());
        } else {
            setEditValue(value);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !multiline) {
            e.preventDefault();
            handleBlur();
        } else if (e.key === 'Escape') {
            setEditValue(value);
            setIsEditing(false);
        }
    };

    const Tag = tag;

    if (isEditing) {
        if (multiline) {
            return (
                <textarea
                    ref={inputRef as React.RefObject<HTMLTextAreaElement>}
                    value={editValue}
                    onChange={(e) => setEditValue(e.target.value)}
                    onBlur={handleBlur}
                    onKeyDown={handleKeyDown}
                    className={`${styles.input} ${styles.textarea} ${className}`}
                    placeholder={placeholder}
                    rows={3}
                />
            );
        }

        return (
            <input
                ref={inputRef as React.RefObject<HTMLInputElement>}
                type="text"
                value={editValue}
                onChange={(e) => setEditValue(e.target.value)}
                onBlur={handleBlur}
                onKeyDown={handleKeyDown}
                className={`${styles.input} ${className}`}
                placeholder={placeholder}
            />
        );
    }

    return (
        <Tag
            onClick={handleClick}
            className={`${styles.editable} ${className}`}
            title="클릭하여 편집"
        >
            {value || placeholder}
        </Tag>
    );
}
