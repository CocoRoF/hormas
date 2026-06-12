"use client";
import React from 'react';
import styles from '@/app/hormas/assets/HormasDemo.module.scss';

export default function ReviewInput({ inputText, setInputText }) {
    
    const examples = {
        positive: 'The room was immaculate and the staff were so kind, I was truly touched. Thanks especially to [Employee Name] in the lobby, we had a very comfortable trip. I would definitely love to visit again!',
        negative: 'We waited over 30 minutes to check in, and when we got to the room, it hadn\'t been cleaned properly. There were stains on the towels and a strange smell coming from the air conditioner. We will not be coming back.',
        neutral: 'The location was good, but the room was smaller than I expected. The breakfast didn\'t have many options, but it was decent. Considering the price, it was an okay choice.'
    };

    return (
        <div className={`${styles.panel} ${styles.reviewPanel}`}>
            <h2 className={styles.panelTitle}>Review Input</h2>
            
            <div className={styles.exampleButtons}>
                <button type="button" onClick={() => setInputText(examples.positive)}>Positive Example</button>
                <button type="button" onClick={() => setInputText(examples.negative)}>Negative Example</button>
                <button type="button" onClick={() => setInputText(examples.neutral)}>Neutral Example</button>
            </div>

            <textarea 
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                className={styles.reviewTextarea}
                placeholder="Enter or paste the customer review here..."
                required
            />
        </div>
    );
}