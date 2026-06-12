"use client";
import React from 'react';
import Select from "react-select";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
import styles from '@/app/hormas/assets/HormasDemo.module.scss';

// react-select custom styles (no changes needed)
const selectCustomStyles = {
    control: (provided) => ({ ...provided, backgroundColor: 'var(--hormas-surface)', border: '1px solid var(--hormas-border)', boxShadow: 'none', '&:hover': { borderColor: 'var(--hormas-primary)' } }),
    menu: (provided) => ({ ...provided, backgroundColor: 'var(--hormas-surface)', border: '1px solid var(--hormas-border)' }),
    option: (provided, { isFocused, isSelected }) => ({ ...provided, backgroundColor: isSelected ? 'var(--hormas-primary)' : isFocused ? 'rgba(255, 255, 255, 0.08)' : 'var(--hormas-surface)', '&:active': { backgroundColor: 'var(--hormas-primary-variant)' } }),
    singleValue: (provided) => ({ ...provided, color: 'var(--hormas-text-primary)' }),
    input: (provided) => ({ ...provided, color: 'var(--hormas-text-primary)' }),
    placeholder: (provided) => ({...provided, color: 'var(--hormas-text-secondary)'}),
};

const Tooltip = ({ text }) => (
    <div className={styles.tooltip}>
        <FontAwesomeIcon icon={faQuestionCircle} />
        <span className={styles.tooltipText}>{text}</span>
    </div>
);

export default function SettingsPanel({
    model, setModel, analysisModel, setAnalysisModel, prompt, setPrompt,
    inputName, setInputName, inputContact, setInputContact,
    inputRetrieval, setInputRetrieval
}) {
    const modelOptions = [
        { value: 'gpt-4o-2024-05-13', label: 'OpenAI: GPT-4o' },
        { value: 'gpt-4-turbo', label: 'OpenAI: GPT-4 Turbo' },
    ];
    const promptOptions = [{ value: 'final', label: 'HormAS-Final' }];

    // 예시 데이터를 로드하는 핸들러 함수
    const handleLoadExample = () => {
        // react-select는 value와 label이 모두 포함된 객체로 상태를 업데이트해야 합니다.
        const exampleModel = modelOptions.find(opt => opt.value === 'gpt-4o-2024-05-13');
        const examplePrompt = promptOptions.find(opt => opt.value === 'final');

        setModel(exampleModel);
        setAnalysisModel(exampleModel);
        setPrompt(examplePrompt);

        // 선택적 입력 필드에 예시 데이터 설정
        setInputName("Manager - Haryeom Jang");
        setInputContact("Hrjang@hormashotel.com");
        setInputRetrieval(
            "- The swimming pool is open from 9 AM to 8 PM.\n- Check-out time is 11 AM.\n- A late check-out fee of $50 applies."
        );
    };

    return (
        <div className={styles.panel}>
            <div className={styles.panelHeader}>
                <h2 className={styles.panelTitle}>AI Settings</h2>
                {/* 예시 로드 버튼 추가 */}
                <button type="button" onClick={handleLoadExample} className={styles.loadExampleBtn}>
                    Load Example
                </button>
            </div>
            
            <div className={styles.grid}>
                <div className={styles.formGroup}>
                    <label htmlFor="model-select">Response Generation Model</label>
                    <Select id="model-select" instanceId="model-select" options={modelOptions} value={model} onChange={setModel} styles={selectCustomStyles} placeholder="Select a model..." />
                </div>
                <div className={styles.formGroup}>
                    <label htmlFor="analysis-model-select">Review Analysis Model</label>
                    <Select id="analysis-model-select" instanceId="analysis-model-select" options={modelOptions} value={analysisModel} onChange={setAnalysisModel} styles={selectCustomStyles} placeholder="Select a model..." />
                </div>
                <div className={`${styles.formGroup} ${styles.fullWidth}`}>
                    <label htmlFor="prompt-select">Prompt Version</label>
                    <Select id="prompt-select" instanceId="prompt-select" options={promptOptions} value={prompt} onChange={setPrompt} styles={selectCustomStyles} placeholder="Select a version..." />
                </div>
                <div className={styles.formGroup}>
                    <label htmlFor="responder-name">
                        Responder Name (Optional)
                        <Tooltip text="Enter the name or business name to be included in the response. Ex: Manager John Doe" />
                    </label>
                    <input id="responder-name" type="text" value={inputName} onChange={(e) => setInputName(e.target.value)} placeholder="Ex: HormAS Hotel" />
                </div>
                <div className={styles.formGroup}>
                     <label htmlFor="contact-info">
                        Contact Information (Optional)
                        <Tooltip text="Enter the email, phone number, etc., to provide to the customer." />
                    </label>
                    <input id="contact-info" type="text" value={inputContact} onChange={(e) => setInputContact(e.target.value)} placeholder="Ex: help@hormas.com" />
                </div>
                <div className={`${styles.formGroup} ${styles.fullWidth}`}>
                    <label htmlFor="retrieval-input">
                        Reference Information (RAG, Optional)
                         <Tooltip text="Additional information for the AI to reference when generating the response. Please separate each piece of information with a new line." />
                    </label>
                    <textarea id="retrieval-input" value={inputRetrieval} onChange={(e) => setInputRetrieval(e.target.value)} placeholder="- Breakfast is served from 7 AM to 10 AM.&#10;- Parking is free of charge." rows="5" />
                </div>
            </div>
        </div>
    );
}