"use client";
import '@/app/globals.css';

export default function RootLayout({ children }) {
    return (
        <html lang="ko">
            <link rel="icon" type="image/svg+xml" href="hrweb_icon.svg" />
                <body>
                    {children}
                </body>
        </html>
    )
}
