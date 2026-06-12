'use client';
import React, { useEffect, useRef, useCallback } from 'react';
import styles from '@/app/_common/assets/SpaceBackground.module.scss';
import { throttle } from 'lodash'; // 마우스 이동 이벤트 최적화를 위해 lodash.throttle 사용

// 별, 달, 유성의 기본 설정을 위한 상수
const NUM_STARS = 700; // 별의 개수 (기존 150개에서 증가, Canvas에서는 더 많이 처리 가능)
const MOON_BASE_RADIUS = 100; // 달의 기본 반지름
const STAR_INTERACTION_RADIUS = 300; // 별과 마우스 상호작용 반경
const MOON_INTERACTION_RADIUS = 100; // 달과 마우스 상호작용 반경

export default function SpaceBackground() {
    const canvasRef = useRef(null); // Canvas 요소 참조
    const containerRef = useRef(null); // 배경 컨테이너 div 참조
    
    // 애니메이션 상태 및 객체들을 저장하기 위한 Ref
    const starsRef = useRef([]);
    const moonRef = useRef(null);
    const shootingStarsRef = useRef([]);
    const mousePosRef = useRef({ x: undefined, y: undefined });
    const scrollYRef = useRef(0);
    const animationFrameIdRef = useRef(null);

    // Canvas 크기 조절 함수
    const resizeCanvas = useCallback(() => {
        const canvas = canvasRef.current;
        const container = containerRef.current;
        if (canvas && container) {
            canvas.width = container.offsetWidth;
            canvas.height = container.offsetHeight;
        }
    }, []);

    // 초기화 함수 (별, 달 생성)
    const initializeElements = useCallback(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const { width, height } = canvas;

        // 별 생성
        starsRef.current = [];
        for (let i = 0; i < NUM_STARS; i++) {
            starsRef.current.push({
                x: Math.random() * width,
                y: Math.random() * height,
                originalY: Math.random() * height, // 스크롤 패럴랙스용 원래 Y 위치
                radius: Math.random() * 2 + Math.random() * 3 + 0.1, // 별의 반지름 (0.5 ~ 2.0)
                opacity: Math.random() * 0.5 + 0.2, // 별의 투명도 (0.2 ~ 0.7)
                twinkleSpeed: Math.random() * 0.005, // 반짝임 속도
                twinklePhase: Math.random() * Math.PI * 2, // 반짝임 시작 위상
                isBright: Math.random() > 0.8, // 밝은 별 여부
                parallaxFactor: Math.random() * 0.3 + 0.1, // 스크롤 패럴랙스 계수
                // 마우스 상호작용용 속성
                targetRadius: Math.random() * 1.5 + 0.5,
                currentRadius: Math.random() * 1.5 + 0.5,
                targetOpacity: Math.random() * 0.5 + 0.2,
                currentOpacity: Math.random() * 0.5 + 0.2,
            });
        }

        // 달 생성
        moonRef.current = {
            x: width * 0.85, // 화면 오른쪽 상단 부근
            y: height * 0.15,
            originalX: width * 0.85,
            originalY: height * 0.15,
            radius: MOON_BASE_RADIUS,
            targetRadius: MOON_BASE_RADIUS,
            currentRadius: MOON_BASE_RADIUS,
            pulsePhase: 0,
            pulseSpeed: 0.01,
            parallaxFactor: 0.005, // 달은 별보다 천천히 움직임
            craters: [ // 간단한 크레이터 정보
                { xOffset: -15, yOffset: -10, radius: 7, color: 'rgba(0,0,0,0.2)' },
                { xOffset: 10, yOffset: 5, radius: 12, color: 'rgba(0,0,0,0.15)' },
                { xOffset: 5, yOffset: 18, radius: 5, color: 'rgba(0,0,0,0.2)' },
            ]
        };
        shootingStarsRef.current = [];

    }, []);

    // 유성 생성 함수
    const createShootingStar = useCallback(() => {
        const canvas = canvasRef.current;
        if (!canvas || shootingStarsRef.current.length > 30) return;

        const { width, height } = canvas;
        const duration = Math.random() * 16000 + 2500;
        shootingStarsRef.current.push({
            startX: Math.random() * width,
            startY: Math.random() * height * 0.4, // 화면 상단 40% 이내에서 시작
            angle: Math.PI / 4 + (Math.random() * Math.PI / 8 - Math.PI / 16), // 대각선 방향 (약간의 변화)
            speed: Math.random() * 2.5 + 2, // 속도 (2 ~ 4.5)
            opacity: 1,
            startTime: Date.now(),
            duration: duration,
            headRadius: Math.random() * 5 + 2, // 유성 머리 반지름 (2px ~ 4px)
            tailLength: Math.random() * 100 + 160, // 꼬리 길이 (80px ~ 180px)
            colorStops: [ // 꼬리 그라데이션 색상
                { stop: 0, color: 'rgba(255, 255, 255, 0.8)' }, // 머리 근처
                { stop: 0.3, color: 'rgba(255, 255, 220, 0.5)' },
                { stop: 1, color: 'rgba(255, 220, 180, 0)' }    // 꼬리 끝 (투명)
            ]
        });
    }, []);
    
    // 애니메이션 루프
    const animate = useCallback(() => {
        const canvas = canvasRef.current;
        const ctx = canvas?.getContext('2d');
        if (!ctx || !canvas) {
            animationFrameIdRef.current = requestAnimationFrame(animate);
            return;
        }

        const { width, height } = canvas;
        ctx.clearRect(0, 0, width, height);

        const currentTime = Date.now();
        const mouseX = mousePosRef.current.x;
        const mouseY = mousePosRef.current.y;

        // 별 그리기 및 업데이트
        starsRef.current.forEach(star => {
            // 반짝임 효과
            star.currentOpacity = star.opacity + Math.sin(star.twinklePhase + currentTime * star.twinkleSpeed) * (star.opacity * 0.5);
            
            // 마우스 상호작용
            if (mouseX !== undefined && mouseY !== undefined) {
                const dx = star.x - mouseX;
                const dy = star.y - mouseY;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < STAR_INTERACTION_RADIUS) {
                    const proximityEffect = 1 - (distance / STAR_INTERACTION_RADIUS);
                    star.targetOpacity = star.opacity + proximityEffect * 0.5; // 더 밝게
                    star.targetRadius = star.radius + proximityEffect * 2;    // 더 크게
                    if (star.isBright) {
                       star.targetRadius = star.radius + proximityEffect * 3;
                    }
                } else {
                    star.targetOpacity = star.opacity;
                    star.targetRadius = star.radius;
                }
            } else {
                 star.targetOpacity = star.opacity;
                 star.targetRadius = star.radius;
            }
             // 부드러운 전환
            star.currentRadius += (star.targetRadius - star.currentRadius) * 0.1;
            star.currentOpacity += (star.targetOpacity - star.currentOpacity) * 0.1;
            if (star.currentOpacity < 0) star.currentOpacity = 0;
            if (star.currentOpacity > 1) star.currentOpacity = 1;


            // 스크롤 패럴랙스 효과
            star.y = star.originalY - scrollYRef.current * star.parallaxFactor;


            ctx.beginPath();
            ctx.arc(star.x, star.y, star.currentRadius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${star.currentOpacity})`;
            if (star.isBright && star.currentRadius > star.radius) { // 밝은 별이 커졌을 때 추가 효과
                ctx.shadowColor = 'rgba(255, 255, 255, 0.7)';
                ctx.shadowBlur = star.currentRadius * 2;
            } else {
                ctx.shadowColor = 'transparent';
                ctx.shadowBlur = 0;
            }
            ctx.fill();
            ctx.shadowColor = 'transparent'; // 그림자 초기화
            ctx.shadowBlur = 0;
        });

        // 달 그리기 및 업데이트
        const moon = moonRef.current;
        if (moon) {
            // 달 위치 (스크롤 패럴랙스)
            moon.x = moon.originalX - scrollYRef.current * moon.parallaxFactor;
            moon.y = moon.originalY - scrollYRef.current * moon.parallaxFactor;

            // 달 맥동 효과 (반지름 및 그림자)
            moon.pulsePhase += moon.pulseSpeed;
            const pulseValue = Math.sin(moon.pulsePhase);
            moon.currentRadius = moon.radius + pulseValue * 5; // 반지름 변화 폭 5px

            if (mouseX !== undefined && mouseY !== undefined) {
                const mdx = moon.x - mouseX;
                const mdy = moon.y - mouseY;
                const mDistance = Math.sqrt(mdx * mdx + mdy * mdy);
                if (mDistance < MOON_INTERACTION_RADIUS + moon.currentRadius) {
                     moon.targetRadius = MOON_BASE_RADIUS * 1.15; // 15% 크게
                } else {
                     moon.targetRadius = MOON_BASE_RADIUS;
                }
            } else {
                moon.targetRadius = MOON_BASE_RADIUS;
            }
            moon.currentRadius += (moon.targetRadius - moon.currentRadius) * 0.05;


            // 달 본체 그라데이션
            const moonGradient = ctx.createRadialGradient(moon.x, moon.y, 0, moon.x, moon.y, moon.currentRadius);
            moonGradient.addColorStop(0, '#f0f0e0');    // 밝은 부분
            moonGradient.addColorStop(0.4, '#e0e0d0');
            moonGradient.addColorStop(0.7, '#c0c0b0');
            moonGradient.addColorStop(1, '#a0a090');    // 어두운 부분
            
            ctx.fillStyle = moonGradient;

            // 달 그림자 (맥동 효과와 마우스 상호작용 반영)
            const shadowIntensity = 0.5 + (pulseValue + 1) * 0.25; // 0.5 ~ 1.0
            let shadowBlur = 20 + pulseValue * 10;
            if (moon.currentRadius > MOON_BASE_RADIUS) { // 마우스 호버 시
                shadowBlur = Math.max(shadowBlur, 30 + (moon.currentRadius - MOON_BASE_RADIUS));
            }

            ctx.shadowColor = `rgba(245, 245, 220, ${shadowIntensity * 0.6})`;
            ctx.shadowBlur = shadowBlur;
            ctx.shadowOffsetX = 0;
            ctx.shadowOffsetY = 0;

            ctx.beginPath();
            ctx.arc(moon.x, moon.y, moon.currentRadius, 0, Math.PI * 2);
            ctx.fill();
            
            // 달 크레이터 그리기
            moon.craters.forEach(crater => {
                ctx.beginPath();
                ctx.fillStyle = crater.color;
                // 크레이터는 그림자 효과를 받지 않도록 잠시 해제
                ctx.shadowColor = 'transparent';
                ctx.shadowBlur = 0;
                ctx.arc(moon.x + crater.xOffset, moon.y + crater.yOffset, crater.radius, 0, Math.PI * 2);
                ctx.fill();
            });
            
            ctx.shadowColor = 'transparent'; // 그림자 초기화
            ctx.shadowBlur = 0;
        }

        // 유성 그리기 및 업데이트
        shootingStarsRef.current = shootingStarsRef.current.filter(ss => {
            const elapsedTime = currentTime - ss.startTime;
            if (elapsedTime > ss.duration) return false;

            const progress = elapsedTime / ss.duration;
            const currentOpacity = (1 - progress) * ss.opacity; // 전체적인 투명도 조절

            // 유성 머리의 현재 위치 계산
            const headX = ss.startX + Math.cos(ss.angle) * ss.speed * progress * 150; // 이동 거리 스케일 조정
            const headY = ss.startY + Math.sin(ss.angle) * ss.speed * progress * 150;

            // 꼬리 끝점 계산
            const tailEndX = headX - Math.cos(ss.angle) * ss.tailLength;
            const tailEndY = headY - Math.sin(ss.angle) * ss.tailLength;

            // 꼬리 그라데이션 생성
            const tailGradient = ctx.createLinearGradient(headX, headY, tailEndX, tailEndY);
            ss.colorStops.forEach(cs => {
                // 꼬리 전체가 점점 투명해지도록 alpha 값 조절
                const alphaMatch = cs.color.match(/rgba\((\d+,\s*\d+,\s*\d+),\s*([\d.]+)\)/);
                if (alphaMatch) {
                    const baseColor = alphaMatch[1];
                    const baseAlpha = parseFloat(alphaMatch[2]);
                    tailGradient.addColorStop(cs.stop, `rgba(${baseColor}, ${baseAlpha * currentOpacity})`);
                } else {
                    tailGradient.addColorStop(cs.stop, cs.color); // Fallback
                }
            });
            
            // 꼬리 그리기
            ctx.beginPath();
            ctx.moveTo(tailEndX, tailEndY); // 꼬리 끝에서 시작
            ctx.lineTo(headX, headY);       // 머리 쪽으로 선을 그림
            ctx.strokeStyle = tailGradient;
            ctx.lineWidth = ss.headRadius * 1.5 + progress * 2; // 꼬리가 머리보다 약간 가늘게 시작해서 점점 가늘어짐
            ctx.stroke();

            // 머리 그리기 (꼬리 위에 덮어씌움)
            ctx.beginPath();
            // 머리 부분에 약간의 빛 확산 효과(그림자) 추가
            ctx.shadowColor = `rgba(255, 255, 220, ${currentOpacity * 0.7})`; // 밝은 노란색 계열
            ctx.shadowBlur = ss.headRadius * 3 + 5 * progress; // 진행될수록 확산이 줄어들 수 있도록
            
            ctx.arc(headX, headY, ss.headRadius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${currentOpacity})`; // 머리는 밝은 흰색
            ctx.fill();

            ctx.shadowColor = 'transparent'; // 그림자 초기화
            ctx.shadowBlur = 0;
            
            return true;
        });


        animationFrameIdRef.current = requestAnimationFrame(animate);
    }, []); // scrollYRef는 ref이므로 의존성 배열에 포함하지 않아도 됨

    // 마우스 이동 핸들러 (쓰로틀링 적용)
    const handleMouseMove = useCallback(throttle((e) => {
        mousePosRef.current = { x: e.clientX, y: e.clientY };
    }, 50), []); // 50ms 간격으로 쓰로틀링

    // 스크롤 핸들러
    const handleScroll = useCallback(throttle(() => {
        scrollYRef.current = window.scrollY;
    }, 16), []); // requestAnimationFrame과 유사한 간격으로 쓰로틀링 (약 60fps)


    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        resizeCanvas(); // 초기 크기 설정
        initializeElements(); // 별, 달 등 요소 초기화
        
        // 애니메이션 시작
        animationFrameIdRef.current = requestAnimationFrame(animate);

        // 유성 생성 타이머
        const shootingStarInterval = setInterval(createShootingStar, 1500); // 2.5초마다 유성 생성 시도

        // 이벤트 리스너 등록
        window.addEventListener('resize', resizeCanvas);
        document.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('scroll', handleScroll);

        // 클린업 함수
        return () => {
            cancelAnimationFrame(animationFrameIdRef.current);
            clearInterval(shootingStarInterval);
            window.removeEventListener('resize', resizeCanvas);
            document.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('scroll', handleScroll);
            handleMouseMove.cancel(); // throttle된 함수 취소
            handleScroll.cancel(); // throttle된 함수 취소
        };
    }, [resizeCanvas, initializeElements, animate, createShootingStar, handleMouseMove, handleScroll]);

    return (
        <div className={styles.starryBackground} ref={containerRef}>
            {/* 배경 그라데이션 등은 CSS로 처리 (기존 SCSS 활용) */}
            <div className={styles.colorfulNebula} />
            <div className={styles.milkyWay} />
            
            {/* Canvas 요소: 별, 달, 유성 등을 그림 */}
            <canvas ref={canvasRef} className={styles.mainCanvas} />
            
            {/* 기존 달 DOM 요소는 제거 (Canvas로 대체) */}
            {/* <div className={styles.moon} ref={moonRef} /> */}
            {/* 기존 유성 DOM 요소들도 제거 (Canvas로 대체) */}
        </div>
    );
}
