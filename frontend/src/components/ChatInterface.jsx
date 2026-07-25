import { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import Stage1 from './Stage1';
import Stage2 from './Stage2';
import Stage3 from './Stage3';
import './ChatInterface.css';

import { api } from '../api';

export default function ChatInterface({
  conversation,
  onSendMessage,
  isLoading,
}) {
  const [input, setInput] = useState('');
  const [provider, setProvider] = useState('openrouter');
  const [showCustomModels, setShowCustomModels] = useState(false);
  const [councilModels, setCouncilModels] = useState(['', '', '', '']);
  const [chairmanModel, setChairmanModel] = useState('');
  const [presets, setPresets] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadModelPresets();
  }, []);

  useEffect(() => {
    if (presets && presets[provider]) {
      setCouncilModels([...presets[provider].council_models]);
      setChairmanModel(presets[provider].chairman_model);
    }
  }, [provider, presets]);

  const loadModelPresets = async () => {
    try {
      const data = await api.getModels();
      setPresets(data);
      if (data && data[provider]) {
        setCouncilModels([...data[provider].council_models]);
        setChairmanModel(data[provider].chairman_model);
      }
    } catch (e) {
      console.error('Failed to load model presets:', e);
    }
  };

  const handleCouncilModelChange = (index, value) => {
    const updated = [...councilModels];
    updated[index] = value;
    setCouncilModels(updated);
  };

  const handleResetModels = () => {
    if (presets && presets[provider]) {
      setCouncilModels([...presets[provider].council_models]);
      setChairmanModel(presets[provider].chairman_model);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversation]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      const filteredCouncil = councilModels.filter((m) => m && m.trim().length > 0);
      onSendMessage(input, {
        provider,
        councilModels: filteredCouncil.length > 0 ? filteredCouncil : null,
        chairmanModel: chairmanModel.trim() || null,
      });
      setInput('');
    }
  };

  const handleKeyDown = (e) => {
    // Submit on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  if (!conversation) {
    return (
      <div className="chat-interface">
        <div className="empty-state">
          <h2>Welcome to LLM Council</h2>
          <p>Create a new conversation to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-interface">
      <div className="messages-container">
        {conversation.messages.length === 0 ? (
          <div className="empty-state">
            <h2>Start a conversation</h2>
            <p>Ask a question to consult the LLM Council</p>
          </div>
        ) : (
          conversation.messages.map((msg, index) => (
            <div key={index} className="message-group">
              {msg.role === 'user' ? (
                <div className="user-message">
                  <div className="message-label">You</div>
                  <div className="message-content">
                    <div className="markdown-content">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="assistant-message">
                  <div className="message-label">LLM Council</div>

                  {/* Stage 1 */}
                  {msg.loading?.stage1 && (
                    <div className="stage-loading">
                      <div className="spinner"></div>
                      <span>Running Stage 1: Collecting individual responses...</span>
                    </div>
                  )}
                  {msg.stage1 && <Stage1 responses={msg.stage1} />}

                  {/* Stage 2 */}
                  {msg.loading?.stage2 && (
                    <div className="stage-loading">
                      <div className="spinner"></div>
                      <span>Running Stage 2: Peer rankings...</span>
                    </div>
                  )}
                  {msg.stage2 && (
                    <Stage2
                      rankings={msg.stage2}
                      labelToModel={msg.metadata?.label_to_model}
                      aggregateRankings={msg.metadata?.aggregate_rankings}
                    />
                  )}

                  {/* Stage 3 */}
                  {msg.loading?.stage3 && (
                    <div className="stage-loading">
                      <div className="spinner"></div>
                      <span>Running Stage 3: Final synthesis...</span>
                    </div>
                  )}
                  {msg.stage3 && <Stage3 finalResponse={msg.stage3} />}
                </div>
              )}
            </div>
          ))
        )}

        {isLoading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <span>Consulting the council...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {conversation.messages.length === 0 && (
        <form className="input-form" onSubmit={handleSubmit}>
          <div className="input-controls">
            <div className="provider-selector-row">
              <div className="provider-selector">
                <label htmlFor="provider-select" className="provider-label">Provider:</label>
                <select
                  id="provider-select"
                  className="provider-select"
                  value={provider}
                  onChange={(e) => setProvider(e.target.value)}
                  disabled={isLoading}
                >
                  <option value="openrouter">OpenRouter (GPT-4o, Gemini, Claude, GLM)</option>
                  <option value="nvidia_nim">NVIDIA NIM (Nemotron, Llama 3.3, Mistral, DeepSeek)</option>
                </select>
              </div>
              <button
                type="button"
                className="toggle-models-button"
                onClick={() => setShowCustomModels(!showCustomModels)}
              >
                {showCustomModels ? '⚙ Hide Custom Models' : '⚙ Customize Models'}
              </button>
            </div>

            {showCustomModels && (
              <div className="custom-models-panel">
                <div className="panel-header">
                  <span className="panel-title">Council Models (Stage 1 & 2)</span>
                  <button type="button" className="reset-models-button" onClick={handleResetModels}>
                    Reset Defaults
                  </button>
                </div>
                <div className="models-grid">
                  {councilModels.map((model, idx) => (
                    <div key={idx} className="model-input-group">
                      <label className="model-label">Member {idx + 1}:</label>
                      <input
                        type="text"
                        className="model-input"
                        value={model}
                        onChange={(e) => handleCouncilModelChange(idx, e.target.value)}
                        placeholder={`Model ${idx + 1} identifier`}
                        disabled={isLoading}
                      />
                    </div>
                  ))}
                </div>
                <div className="chairman-input-group">
                  <label className="model-label">Chairman Model (Stage 3 Synthesis):</label>
                  <input
                    type="text"
                    className="model-input"
                    value={chairmanModel}
                    onChange={(e) => setChairmanModel(e.target.value)}
                    placeholder="Chairman model identifier"
                    disabled={isLoading}
                  />
                </div>
              </div>
            )}

            <div className="input-row">
              <textarea
                className="message-input"
                placeholder="Ask your question... (Shift+Enter for new line, Enter to send)"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
                rows={3}
              />
              <button
                type="submit"
                className="send-button"
                disabled={!input.trim() || isLoading}
              >
                Send
              </button>
            </div>
          </div>
        </form>
      )}
    </div>
  );
}
