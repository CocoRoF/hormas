

"use client";
import Link from 'next/link';
import React from 'react';
import Image from "next/image";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGithub } from '@fortawesome/free-brands-svg-icons';
import { faFileLines, faDatabase } from '@fortawesome/free-solid-svg-icons';

import { hormasAdminMainContents } from "@/app/hormas/constants/main_contents";
import styles from '@/app/hormas/assets/HormasAdminMain.module.scss';

const contentsToDisplay = hormasAdminMainContents.slice(0, 3);

const authors = ["Haryeom Jang", "Sanghyeak Yoon", "Sangwon Park", "Sung-Byung Yang"];
const links = {
    github: "https://github.com/CocoRoF/hormas",
    huggingface: "https://huggingface.co/datasets/CocoRoF/hotel_review_data",
    paper: ""
};

export default function HormasAdminMain() {
    return (
        <div className={styles.container}>
            <header className={styles.header}>
                <h1 className={styles.paperTitle}>
                    Designing a Generative Artificial Intelligence-Based Hotel Review Management Assistant: A Design Science Approach
                </h1>
                <div className={styles.authorList}>
                    {authors.map((author, index) => (
                        <span key={index} className={styles.authorName}>{author}</span>
                    ))}
                </div>
            </header>

            <nav className={styles.externalLinks}>
                <a href={links.github} target="_blank" rel="noopener noreferrer" className={styles.iconButton}>
                    <FontAwesomeIcon icon={faGithub} />
                    <span>GitHub</span>
                </a>
                <a href={links.huggingface} target="_blank" rel="noopener noreferrer" className={styles.iconButton}>
                    <FontAwesomeIcon icon={faDatabase} />
                    <span>HuggingFace</span>
                </a>
                {/* <a href={links.paper} target="_blank" rel="noopener noreferrer" className={styles.iconButton}>
                    <FontAwesomeIcon icon={faFileLines} />
                    <span>Paper(Unready)</span>
                </a> */}
            </nav>

            <div className={styles.gridContainer}>
                {contentsToDisplay.map((content) => (
                    <article key={content.title} className={styles.card}>
                        <Link href={content.url} className={styles.cardLink}>
                            <div className={styles.imageWrapper}>
                                <Image
                                    src={content.img}
                                    alt={content.alt}
                                    fill
                                    sizes="(max-width: 768px) 100vw, 33vw"
                                    style={{ objectFit: 'cover' }}
                                />
                            </div>
                            <div className={styles.overlay}>
                                <h2 className={styles.cardTitle}>{content.title}</h2>
                                <p className={styles.cardText}>{content.text}</p>
                            </div>
                        </Link>
                    </article>
                ))}
            </div>

        </div>
    );
};