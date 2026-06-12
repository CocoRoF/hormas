// 파일 위치: src/app/hormas/layout.js
// 이 파일의 내용을 아래 코드로 완전히 교체하세요.
"use client";
import React, { useState } from "react";
import SidebarAdmin from "@/app/hormas/components/SidebarAdmin";
import "@/app/hormas/assets/hormas-global.scss";


export default function HormASLayout({ children }) {
    const [isSidebarExpanded, setSidebarExpanded] = useState(false);

    return (
        <div 
            className={`hormas-layout ${isSidebarExpanded ? 'sidebar-expanded' : ''}`}
        >
            <SidebarAdmin 
                onMouseEnter={() => setSidebarExpanded(true)}
                onMouseLeave={() => setSidebarExpanded(false)}
            />
            <main className="hormas-main-content">
                {children}
            </main>
        </div>
    );
}