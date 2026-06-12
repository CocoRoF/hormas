"use client";
import React from 'react';
import styles from '@/app/hormas/assets/HormasDemo.module.scss';
import Loading from '@/app/_common/components/Common_Loading'; 

export default function ResultDisplay({ 
    isLoading, 
    isSuccess,
    data, 
    data2, 
    userSentiment, 
    userEmotion, 
    userIntention, 
    reviewUrgency 
}) {
    
    if (isLoading) {
        return (
            <div className={styles.resultPlaceholder}>
                <Loading />
                <p>The AI is analyzing the review<br/>and generating a response.</p>
            </div>
        );
    }

    // Initial state or error message display
    if (!isSuccess) {
        return (
            <div className={styles.resultPlaceholder}>
                <h3>AI Generation Result</h3>
                <p>{data || "Generated responses will be displayed here."}</p>
            </div>
        );
    }

    // When results are successfully received
    return (
        <div className={styles.resultContainer}>
            {/* Display analysis results if available */}
            {userSentiment && (
                <div className={styles.analysisGrid}>
                    <div className={styles.analysisItem}>
                        <span>Sentiment</span><p>{userSentiment}</p>
                    </div>
                    <div className={styles.analysisItem}>
                        <span>Emotion</span><p>{userEmotion}</p>
                    </div>
                    <div className={styles.analysisItem}>
                        <span>Intention</span><p>{userIntention}</p>
                    </div>
                    <div className={styles.analysisItem}>
                        <span>Urgency</span><p>{reviewUrgency}</p>
                    </div>
                </div>
            )}

            {/* Display HormAS response */}
            <div className={styles.responseBox}>
                <h3>HormAS Generated Response</h3>
                <p>{data}</p>
            </div>

            {/* Display standard AI response if available */}
            {data2 && (
                 <div className={`${styles.responseBox} ${styles.standard}`}>
                    <h3>Standard AI Generated Response</h3>
                    <p>{data2}</p>
                </div>
            )}
        </div>
    );
}