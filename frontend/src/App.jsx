
import { useCallback, useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [words, setWords] = useState([]);
  const [word, setWord] = useState("");
  const [definition, setDefinition] = useState("");
  const [language, setLanguage] = useState("English");
  const [history, setHistory] = useState(null);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [showDefinition, setShowDefinition] = useState(false);

  const loadWords = useCallback(async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/words/due/`);
      setWords(Array.isArray(response.data) ? response.data : []);
    } catch {
      setMessage("Could not load due words. Check that FastAPI is running.");
    } finally {
      setLoading(false);
    }
  }, []);

  const loadHistory = useCallback(async () => {
    try {
      const response = await axios.get(`${API}/words/history/`);
      setHistory(response.data);
    } catch {
      setHistory(null);
    }
  }, []);

  const loadInsights = useCallback(async () => {
    try {
      const response = await axios.get(`${API}/words/insights/`);
      setInsights(response.data);
    } catch {
      setInsights(null);
    }
  }, []);

  const refreshDashboard = useCallback(async () => {
    await Promise.all([loadWords(), loadHistory(), loadInsights()]);
  }, [loadWords, loadHistory, loadInsights]);

  useEffect(() => {
    refreshDashboard();
  }, [refreshDashboard]);

  async function addWord(event) {
    event.preventDefault();
    setMessage("");

    try {
      await axios.post(`${API}/words/`, {
        word: word.trim(),
        definition: definition.trim(),
        language: language.trim(),
      });

      setWord("");
      setDefinition("");
      setLanguage("English");
      setMessage("Word added successfully!");
      await refreshDashboard();
    } catch (error) {
      setMessage(error.response?.data?.detail || "Could not add the word.");
    }
  }

  async function reviewWord(wordId, score) {
    try {
      await axios.post(`${API}/words/${wordId}/review/`, { score });
      setMessage(`Review submitted with score ${score}/5.`);
      setShowDefinition(false);
      await refreshDashboard();
    } catch (error) {
      setMessage(error.response?.data?.detail || "Could not submit the review.");
    }
  }

  async function deleteWord(wordId) {
    if (!window.confirm("Are you sure you want to delete this word?")) return;

    try {
      await axios.delete(`${API}/words/${wordId}`);
      setMessage("Word deleted successfully.");
      await refreshDashboard();
    } catch (error) {
      setMessage(error.response?.data?.detail || "Could not delete the word.");
    }
  }

  const currentWord = words[0];
  const totalReviews = history?.total_reviews ?? 0;
  const accuracy = history?.accuracy_percentage ?? 0;
  const upcomingReviews = insights?.upcoming_reviews ?? [];
  const difficultWords = insights?.difficult_words ?? [];
  const streak = insights?.learning_streak_days ?? 0;

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand-mark">V</div>
        <div>
          <h1>VocaMind</h1>
          <p>AI Spaced Repetition Vocabulary Trainer</p>
        </div>
        <button className="refresh-button" onClick={refreshDashboard}>
          ↻ Refresh
        </button>
      </header>

      <main className="dashboard">
        <section className="welcome">
          <span className="eyebrow">YOUR DAILY LEARNING SPACE</span>
          <h2>Small steps. <span>Stronger memory.</span></h2>
          <p>Learn new words, review what you know, and build a lasting vocabulary.</p>
        </section>

        {message && (
          <div className="message" role="status">
            {message}
            <button onClick={() => setMessage("")} aria-label="Dismiss message">×</button>
          </div>
        )}

        <section className="stats">
          <article className="stat-card">
            <span className="stat-icon">📚</span>
            <p>Words due now</p>
            <h3>{words.length}</h3>
          </article>
          <article className="stat-card">
            <span className="stat-icon">🎯</span>
            <p>Total reviews</p>
            <h3>{totalReviews}</h3>
          </article>
          <article className="stat-card">
            <span className="stat-icon">✨</span>
            <p>Accuracy</p>
            <h3>{accuracy}%</h3>
          </article>
          <article className="stat-card">
            <span className="stat-icon">🔥</span>
            <p>Learning streak</p>
            <h3>{streak} {streak === 1 ? "day" : "days"}</h3>
          </article>
        </section>

        <div className="content-grid">
          <section className="panel add-panel">
            <div className="section-heading">
              <div>
                <span className="eyebrow">GROW YOUR VOCABULARY</span>
                <h2>Add a new word</h2>
              </div>
              <span className="heading-icon">＋</span>
            </div>

            <form onSubmit={addWord}>
              <label htmlFor="word">Word</label>
              <input
                id="word"
                value={word}
                onChange={(event) => setWord(event.target.value)}
                placeholder="e.g. Resilient"
                required
                maxLength={200}
              />

              <label htmlFor="definition">Definition</label>
              <textarea
                id="definition"
                value={definition}
                onChange={(event) => setDefinition(event.target.value)}
                placeholder="What does this word mean?"
                rows="3"
                required
                maxLength={2000}
              />

              <label htmlFor="language">Language</label>
              <input
                id="language"
                value={language}
                onChange={(event) => setLanguage(event.target.value)}
                required
                maxLength={100}
              />

              <button className="primary-button" type="submit">
                + Add word
              </button>
            </form>
          </section>

          <section className="panel review-panel">
            <div className="section-heading">
              <div>
                <span className="eyebrow">SPACED REPETITION</span>
                <h2>Time to review</h2>
              </div>
              <span className="heading-icon">◷</span>
            </div>

            {loading ? (
              <p className="empty-state">Loading your words...</p>
            ) : currentWord ? (
              <div className="word-card">
                <span className="word-label">
                  {currentWord.language || "Vocabulary"}
                </span>
                <h3>{currentWord.word}</h3>

                {showDefinition ? (
                  <p className="definition">{currentWord.definition}</p>
                ) : (
                  <button
                    className="reveal-button"
                    onClick={() => setShowDefinition(true)}
                  >
                    Reveal definition
                  </button>
                )}

                <p className="score-label">How well did you remember?</p>
                <div className="scores">
                  {[0, 1, 2, 3, 4, 5].map((score) => (
                    <button
                      key={score}
                      className={`score score-${score}`}
                      onClick={() => reviewWord(currentWord.id, score)}
                      title={`Rate your recall ${score} out of 5`}
                    >
                      {score}
                    </button>
                  ))}
                </div>
                <p className="score-help">0 = Forgot completely · 5 = Perfect recall</p>

                <button
                  className="delete-button"
                  onClick={() => deleteWord(currentWord.id)}
                >
                  Delete this word
                </button>
              </div>
            ) : (
              <div className="empty-state">
                <div className="empty-emoji">🎉</div>
                <h3>You're all caught up!</h3>
                <p>No words are due right now. Add a word to start learning.</p>
                <button className="secondary-button" onClick={loadWords}>
                  Check again
                </button>
              </div>
            )}
          </section>
        </div>

        <section className="panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">PLAN AHEAD</span>
              <h2>Upcoming reviews</h2>
            </div>
            <span className="heading-icon">📅</span>
          </div>

          {upcomingReviews.length ? (
            <div className="history-list">
              {upcomingReviews.map((item) => (
                <div className="history-item" key={item.word_id}>
                  <div>
                    <strong>{item.word}</strong>
                    <span>
                      {new Date(item.next_review).toLocaleString()}
                    </span>
                  </div>
                  <span className="history-score">
                    In {item.interval} {item.interval === 1 ? "day" : "days"}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="muted">
              {insights
                ? "No future reviews scheduled yet."
                : "Upcoming reviews will appear when the backend is available."}
            </p>
          )}
        </section>

        <section className="panel history-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">FOCUS ON WHAT'S HARD</span>
              <h2>Difficult words</h2>
            </div>
            <span className="heading-icon">🧠</span>
          </div>

          {difficultWords.length ? (
            <div className="history-list">
              {difficultWords.map((item) => (
                <div className="history-item" key={item.word_id}>
                  <div>
                    <strong>{item.word}</strong>
                    <span>{item.review_count} recorded reviews</span>
                  </div>
                  <span className="history-score">
                    Average: {item.average_score}/5
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="muted">
              {insights
                ? "No difficult words identified yet. Words averaging below 3/5 will appear here."
                : "Difficult words will appear when the backend is available."}
            </p>
          )}
        </section>

        <section className="panel history-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">YOUR PROGRESS</span>
              <h2>Learning history</h2>
            </div>
            <span className="heading-icon">↗</span>
          </div>

          {history ? (
            <>
              <div className="history-summary">
                <div>
                  <span>Total reviews</span>
                  <strong>{totalReviews}</strong>
                </div>
                <div>
                  <span>Successful reviews</span>
                  <strong>{history.successful_reviews ?? 0}</strong>
                </div>
                <div>
                  <span>Accuracy</span>
                  <strong>{accuracy}%</strong>
                </div>
              </div>

              {Array.isArray(history.history) && history.history.length > 0 ? (
                <div className="history-list">
                  {history.history.slice(0, 8).map((item, index) => (
                    <div
                      className="history-item"
                      key={`${item.word_id}-${item.review_date}-${index}`}
                    >
                      <div>
                        <strong>{item.word}</strong>
                        <span>
                          {item.review_date
                            ? new Date(item.review_date).toLocaleString()
                            : ""}
                        </span>
                      </div>
                      <span className="history-score">
                        Score: {item.score}/5
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="muted">
                  Your review activity will appear here as you learn.
                </p>
              )}
            </>
          ) : (
            <p className="muted">
              Progress will appear when the backend is available.
            </p>
          )}
        </section>

        <footer>
          <span>VocaMind</span> · One word at a time, one day at a time.
        </footer>
      </main>
    </div>
  );
}

export default App;
