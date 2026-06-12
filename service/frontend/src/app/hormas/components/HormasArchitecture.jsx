import React from 'react';
import Image from 'next/image';
import styles from '@/app/hormas/assets/HormasArchitecture.module.scss';

import raraarch1 from '@/assets/img/raraarch2.jpg';

const techStack = [
    { 
        name: 'Sentiment Analysis', 
        description: 'Analyzes the overall tone of the review (e.g., Positive, Negative, Neutral) to set the foundational mood and direction for the AI-generated response.' 
    },
    { 
        name: 'Emotion Detection', 
        description: 'Identifies specific feelings expressed by the customer (e.g., Anger, Happiness, Disgust) to enable a more empathetic and validating response that directly acknowledges their state.' 
    },
    { 
        name: 'Intention Recognition', 
        description: 'Determines the underlying purpose or goal of the review (e.g., Sharing Experience, Warning Others, Expressing Dissatisfaction) to ensure the response directly addresses the customer’s core need.' 
    },
];

export default function HormasArchitecture() {
    return (
        <div className={styles.container}>
            <div className={styles.contentSection}>
                <h1 className={styles.title}>Architecture</h1>
                <p className={styles.paragraph}>
                    The purpose of this research was to determine if we can design an effective Review-Response System for practical business use by applying prompt engineering techniques, including Chain of Thought (CoT), Zero-shot CoT, and the analysis of customer sentiment, emotion, and intention.
                </p>
                
                <div className={styles.techList}>
                    {techStack.map((tech, index) => (
                        <div key={index} className={styles.techItem}>
                            <h3>{tech.name}</h3>
                            <p>{tech.description}</p>
                        </div>
                    ))}
                </div>
            </div>

            <div className={styles.imageSection}>
                <div className={styles.imageBox}>
                    <div className={styles.imageWrapper}>
                        <Image 
                            src={raraarch1} 
                            alt="System architecture diagram"
                            fill
                            sizes="(max-width: 1024px) 100vw, 50vw"
                            style={{ objectFit: 'scale-down' }}
                        />
                    </div>
                    <h4>- System architecture diagram -</h4>
                </div>

            </div>
        </div>
    );
}