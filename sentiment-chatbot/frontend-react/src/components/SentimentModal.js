import React from 'react';
import ReactMarkdown from 'react-markdown';
import './SentimentModal.css';

const SentimentModal = ({ isOpen, onClose, isLoading, reportData }) => {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <button className="close-btn" onClick={onClose}>×</button>

                {isLoading ? (
                    <div className="loading-container">
                        <div className="smilies-container">
                            <span className="smiley bounce-1">😊</span>
                            <span className="smiley bounce-2">😐</span>
                            <span className="smiley bounce-3">😠</span>
                        </div>
                        <h2>Generating your report !!</h2>
                    </div>
                ) : (
                    <div className="report-container">
                        <h2>Sentiment Analysis Report</h2>

                        {reportData && (
                            <>
                                <div className="overall-score">
                                    <h3>Overall Sentiment Score</h3>
                                    <div className="score-display">
                                        <p>Positive: {(reportData.overall_sentiment.pos * 100).toFixed(1)}%</p>
                                        <p>Neutral: {(reportData.overall_sentiment.neu * 100).toFixed(1)}%</p>
                                        <p>Negative: {(reportData.overall_sentiment.neg * 100).toFixed(1)}%</p>
                                        <p><strong>Compound: {reportData.overall_sentiment.compound.toFixed(4)}</strong></p>
                                    </div>
                                </div>

                                <div className="report-text">
                                    <ReactMarkdown>{reportData.report_text}</ReactMarkdown>
                                </div>
                            </>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default SentimentModal;
