
"use client";
import React from "react";
import Link from "next/link";
import { usePathname } from 'next/navigation';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { 
    faHouse, faLightbulb, faUserGraduate, faMicrochip, 
    faNewspaper, faPowerOff 
} from "@fortawesome/free-solid-svg-icons";

import { hormasSidebarAdmin } from "@/app/hormas/constants/sidebar_contents";
import styles from '@/app/hormas/assets/SidebarAdmin.module.scss';

const iconMap = {
    "fa fa-house": faHouse,
    "fa fa-lightbulb": faLightbulb,
    "fa fa-user-graduate": faUserGraduate,
    "fa fa-microchip": faMicrochip,
    "fa fa-newspaper": faNewspaper,
    "fa fa-power-off": faPowerOff
};

// onMouseEnter와 onMouseLeave props를 받도록 수정
export default function SidebarAdmin({ onMouseEnter, onMouseLeave }) {
    const pathname = usePathname();

    return (
        <nav 
            className={styles.sidebar} 
            onMouseEnter={onMouseEnter} 
            onMouseLeave={onMouseLeave}
        >
            <ul className={styles.navList}>
                {hormasSidebarAdmin.map((item, idx) => {
                    const isActive = pathname === item.url;
                    return (
                        <li key={idx} className={isActive ? styles.active : ''}>
                            <Link href={item.url} title={item.text}>
                                <div className={styles.iconWrapper}>
                                    <FontAwesomeIcon icon={iconMap[item.class] || faHouse} />
                                </div>
                                <span className={styles.navText}>{item.text}</span>
                            </Link>
                        </li>
                    );
                })}
            </ul>
        </nav>
    );
}