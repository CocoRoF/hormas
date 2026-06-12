"use client";
import React, { useState } from 'react';
import styles from '@/app/hormas/assets/HormasDemo.module.scss';
import SettingsPanel from '@/app/hormas/components/SettingPanel';
import ReviewInput from '@/app/hormas/components/ReviewInput';
import ResultDisplay from '@/app/hormas/components/ResultDisplay';
// const baseURL = "http://localhost:8000/";
const baseURL = "https://hrletsgo.me:8443/"

export default function HormasDemo() {
    const [model, setModel] = useState(null);
    const [analysisModel, setAnalysisModel] = useState(null);
    const [prompt, setPrompt] = useState(null);
    const [inputName, setInputName] = useState('');
    const [inputContact, setInputContact] = useState('');
    const [inputRetrieval, setInputRetrieval] = useState('');
    const [inputText, setInputText] = useState('');
    
    const [isLoading, setIsLoading] = useState(false);
    const [isSuccess, setIsSuccess] = useState(false);
    const [isReady, setIsReady] = useState(false);
    
    // API 결과 상태들
    const [data, setData] = useState(null); // HormAS 답변
    const [data2, setData2] = useState(null); // 기본 AI 답변
    const [userSentiment, setUserSentiment] = useState(null);
    const [userEmotion, setUserEmotion] = useState(null);
    const [userIntention, setUserIntention] = useState(null);
    const [reviewUrgency, setReviewUrgency] = useState(null);

    // handleSubmit 함수에 원본 fetch 로직을 그대로 복원합니다.
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!model || !analysisModel || !prompt || !inputText) {
            alert('Please fill in all required fields: Model, Analysis Model, Prompt, and Review Content.'); // 수정: alert 메시지 영어로 변경
            return;
        }

        setIsLoading(true);
        setIsSuccess(false);
        setIsReady(false);
        setData(null);
        setData2(null);
        setUserSentiment(null);
        setUserEmotion(null);
        setUserIntention(null);
        setReviewUrgency(null);

        try {
            const url = baseURL + "api/rara/custom/";
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: model.value,
                    analysis_model: analysisModel.value,
                    responder_name: inputName,
                    contact: inputContact,
                    retrieval: inputRetrieval,
                    inputText: inputText,
                    response_method: prompt.value,
                }),
            });

            const result = await response.json();

            if (response.ok) {
                if (prompt.value === "custom") {
                    setData(result["response"]);
                } else if (prompt.value === "final") {
                    setUserSentiment(result["response"][0]);
                    setUserEmotion(result["response"][1]);
                    setUserIntention(result["response"][2]);
                    setData(result["response"][3]);
                    setData2(result["norm"]);
                    setReviewUrgency(result["response"][4]);
                }
                setIsSuccess(true);
                setIsReady(true);
            } else {
                setData("Server error or invalid request."); // 수정: 오류 메시지 영어로 변경
            }
        } catch (error) {
            setData("Failed to send the request."); // 수정: 오류 메시지 영어로 변경
            console.error('Failed to send the request.', error); // 수정: console.error 메시지 영어로 변경
        } finally {
            setIsLoading(false);
        }
    };
    
    const handleReset = () => {
        setModel(null);
        setAnalysisModel(null);
        setPrompt(null);
        setInputName('');
        setInputContact('');
        setInputRetrieval('');
        setInputText('');
        setIsLoading(false);
        setIsSuccess(false);
        setIsReady(false);
        setData(null);
        setData2(null);
        setUserSentiment(null);
        setUserEmotion(null);
        setUserIntention(null);
        setReviewUrgency(null);
    };

    return (
        <div className={styles.demoContainer}>
            <form className={styles.inputColumn} onSubmit={handleSubmit}>
                <SettingsPanel 
                    model={model} setModel={setModel}
                    analysisModel={analysisModel} setAnalysisModel={setAnalysisModel}
                    prompt={prompt} setPrompt={setPrompt}
                    inputName={inputName} setInputName={setInputName}
                    inputContact={inputContact} setInputContact={setInputContact}
                    inputRetrieval={inputRetrieval} setInputRetrieval={setInputRetrieval}
                />
                <ReviewInput 
                    inputText={inputText}
                    setInputText={setInputText}
                />
                <div className={styles.actionButtons}>
                    <button type="button" className={styles.resetButton} onClick={handleReset}>
                        Reset {/* 수정: 버튼 텍스트 영어로 변경 */}
                    </button>
                    <button type="submit" className={styles.submitButton} disabled={isLoading}>
                        {isLoading ? 'Generating...' : 'Generate AI Response'} {/* 수정: 버튼 텍스트 영어로 변경 */}
                    </button>
                </div>
            </form>

            <div className={styles.outputColumn}>
                {/* ResultDisplay에 모든 관련 상태를 props로 전달합니다. */}
                <ResultDisplay 
                    isLoading={isLoading} 
                    isSuccess={isSuccess}
                    data={data}
                    data2={data2}
                    userSentiment={userSentiment}
                    userEmotion={userEmotion}
                    userIntention={userIntention}
                    reviewUrgency={reviewUrgency}
                />
            </div>
        </div>
    );
}