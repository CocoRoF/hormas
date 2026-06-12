import React from 'react';
import Image from 'next/image';
import styles from '@/app/hormas/assets/HormasAbout.module.scss';

import rara1 from '@/assets/img/raraabout1.jpg';
import rara2 from '@/assets/img/raraabout2.jpg';

export default function HormasAbout() {
    return (
        <div className={styles.container}>
            <div className={styles.contentSection}>
                <h1 className={styles.title}>About HormAS</h1>
                <p className={styles.paragraph}>
                    HormAS stands for <strong>Hotel Review Management Assistant System</strong>. <br></br>It is a specialized AI system developed as part of a research project during the dawn of generative AI. <br></br><br></br>The project's goal was to explore how prompt engineering could be leveraged to significantly improve the quality of automated responses to customer reviews.
                </p>
                <p className={`${styles.paragraph} ${styles.borderBottom}`}>
                    The core of this research was to test a key hypothesis: that generating responses after first extracting a customer's{' '}
                    <strong>sentiment, emotion, intent, and urgency</strong>
                    {' '}would yield far more effective results than generic AI generation. <br></br><br></br>By applying this structured analysis, HormAS was designed to create nuanced, empathetic, and context-aware replies, mimicking the thoughtfulness of a skilled human manager.
                </p>
                <p className={styles.paragraph}>
                    This study demonstrates a foundational principle of early prompt engineering: applying specific domain knowledge is crucial for maximizing the impact of generative AI. <br></br><br></br>Furthermore, the project involved developing HormAS into a functional service and validating its effectiveness with both general users and industry experts. <br></br><br></br>This confirmed its potential for real-world business environments, proving that a strategic approach to AI can enhance both operational efficiency and genuine customer engagement.
                </p>
            </div>

            <div className={styles.imageSection}>
                <div className={styles.imageBox}>
                    <div className={styles.imageWrapper}>
                        <Image 
                            src={rara1} 
                            alt="An image of a book and pencil, symbolizing the importance of thoughtful review responses"
                            fill
                            sizes="(max-width: 768px) 100vw, 50vw"
                            style={{ objectFit: 'cover' }}
                        />
                    </div>
                    <h4>- The Importance of Responding to Customer Reviews -</h4>
                </div>
                <div className={styles.imageBox}>
                    <div className={styles.imageWrapper}>
                        <Image 
                            src={rara2} 
                            alt="An image visualizing the complex data analysis of an AI system"
                            fill
                            sizes="(max-width: 768px) 100vw, 50vw"
                            style={{ objectFit: 'cover' }}
                        />
                    </div>
                    <h4>- HormAS's Multi-Faceted Review Analysis -</h4>
                </div>
            </div>
        </div>
    );
}