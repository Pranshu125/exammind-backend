
import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAI } from '../contexts/AIContext';
import { useAuth } from '../contexts/AuthContext';
import { db } from '../lib/firebase';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import { ArrowLeft, BookOpen, HelpCircle, ListChecks, Video, Sparkles, Loader2, PlayCircle, ExternalLink, MessageCircle, Send, Brain, Upload, Image as ImageIcon, Settings } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import MermaidRenderer from '../components/MermaidRenderer';

export default function PrepMode() {
  const { id, topic } = useParams();
  const navigate = useNavigate();
  const { engine, setEngine } = useAI();
  const { currentUser } = useAuth();
  const decodedTopic = decodeURIComponent(topic);
  
  const [activeTab, setActiveTab] = useState('notes');
  const [content, setContent] = useState({
    notes: null,
    qa: null,
    quiz: null,
    videos: null
  });
  const [loading, setLoading] = useState(false);

  // Chat Mode State (for Notes)
  const [chatMode, setChatMode] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMsg, setInputMsg] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Generation Settings (for QA & Quiz)
  const [settings, setSettings] = useState({ numQuestions: 5, difficulty: 'medium' });

  // Test Yourself State (QA)
  const [testMode, setTestMode] = useState(false);
  const [currentTestIndex, setCurrentTestIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [testFeedback, setTestFeedback] = useState(null);
  const [testLoading, setTestLoading] = useState(false);
  const [testSessionId, setTestSessionId] = useState(null);
  const [testHistory, setTestHistory] = useState([]);

  // Doubt Solver State
  const [doubtText, setDoubtText] = useState('');
  const [doubtFile, setDoubtFile] = useState(null);
  const [doubtAnswer, setDoubtAnswer] = useState(null);
  const [doubtLoading, setDoubtLoading] = useState(false);

  const tabs = [
    { id: 'notes', label: 'Study Notes', icon: BookOpen },
    { id: 'qa', label: 'Q&A Flashcards', icon: HelpCircle },
    { id: 'quiz', label: 'Practice Quiz', icon: ListChecks },
    { id: 'videos', label: 'Video Resources', icon: Video },
    { id: 'doubt', label: 'Doubt Solver', icon: Brain }
  ];

  
  const MarkdownComponents = {
    code({node, inline, className, children, ...props}) {
      const match = /language-(\w+)/.exec(className || '')
      if (!inline && match && match[1] === 'mermaid') {
        return <MermaidRenderer chart={String(children).replace(/\n$/, '')} />
      }
      return <code className={className} {...props}>{children}</code>
    }
  };

  const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

  const fetchNotesOrVideos = async (tabId) => {
    if (content[tabId]) return;
    setLoading(true);
    try {
      if (tabId === 'notes') {
        const res = await fetch(`${API_BASE}/api/generate-notes`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true' },
          body: JSON.stringify({ topic_name: decodedTopic, engine: engine || 'groq' })
        });
        const data = await res.json();
        let markdownText = "";
        if (data.sections) {
           markdownText = data.sections.map(s => `## ${s.heading}\n${s.content}`).join('\n\n');
           markdownText += `\n\n### Summary\n${data.summary}`;
        } else if (data.detail) {
           throw new Error(data.detail);
        } else {
           markdownText = data.notes || JSON.stringify(data);
        }
        setContent(prev => ({ ...prev, [tabId]: markdownText }));
      } 
      else if (tabId === 'videos') {
        const res = await fetch(`${API_BASE}/api/fetch-videos`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true' },
          body: JSON.stringify({ topic_name: decodedTopic, engine: engine || 'groq' })
        });
        const data = await res.json();
        if(data.detail) throw new Error(data.detail);
        setContent(prev => ({ ...prev, [tabId]: data.videos }));
      }
    } catch (error) {
      console.error(`Failed to generate ${tabId}:`, error);
      setContent(prev => ({ ...prev, [tabId]: `Failed to load: ${error.message}` }));
    } finally {
      setLoading(false);
    }
  };

  const generateQAOrQuiz = async (tabId) => {
    setLoading(true);
    try {
      if (tabId === 'qa') {
        const res = await fetch(`${API_BASE}/api/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true' },
          body: JSON.stringify({ 
            messages: [{ role: "user", content: `Generate exactly ${settings.numQuestions} important Question and Answer pairs for studying the topic: "${decodedTopic}" at a ${settings.difficulty} difficulty level. If a diagram helps, include a Mermaid.js markdown block in the answer string. Return ONLY a JSON array of objects with "question" and "answer" keys. Return raw JSON without wrapping in markdown blocks.` }],
            topic_name: decodedTopic,
            engine: engine || 'groq'
          })
        });
        const data = await res.json();
        if(data.detail) throw new Error(data.detail);
        let parsed = data.reply;
        if (typeof parsed === 'string') {
          let cleanStr = parsed.replace(/```json/g, '').replace(/```/g, '').trim();
            // Fix unescaped backslashes and newlines
            cleanStr = cleanStr.replace(/\n/g, "\\n").replace(/\r/g, "\\r").replace(/\t/g, "\\t");
            try {
              parsed = JSON.parse(cleanStr);
            } catch (e) {
              console.log("JSON Parse failed, attempting aggressive backslash fix", e);
              cleanStr = cleanStr.replace(/\\/g, "\\\\");
              parsed = JSON.parse(cleanStr);
            }
        }
        setContent(prev => ({ ...prev, [tabId]: parsed }));
      }
      else if (tabId === 'quiz') {
        const res = await fetch(`${API_BASE}/api/generate-quiz`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true' },
          body: JSON.stringify({ topic_name: decodedTopic, engine: engine || 'groq', difficulty: settings.difficulty, num_questions: Number(settings.numQuestions) })
        });
        const data = await res.json();
        if(data.detail) throw new Error(data.detail);
        setContent(prev => ({ ...prev, [tabId]: data.questions }));
      }
    } catch (error) {
      console.error(`Failed to generate ${tabId}:`, error);
      setContent(prev => ({ ...prev, [tabId]: `Failed to load: ${error.message}` }));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'notes' || activeTab === 'videos') {
      fetchNotesOrVideos(activeTab);
    }
  }, [activeTab]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, testHistory]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMsg.trim()) return;
    const userMsg = inputMsg.trim();
    setInputMsg('');
    const newMessages = [...messages, { role: 'user', content: userMsg }];
    setMessages(newMessages);
    setChatLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true' },
        body: JSON.stringify({ messages: newMessages, topic_name: decodedTopic, engine: engine || 'groq' })
      });
      const data = await res.json();
      setMessages([...newMessages, { role: 'assistant', content: data.reply }]);
    } catch (error) {
      console.error("Chat failed:", error);
    } finally {
      setChatLoading(false);
    }
  };

  const submitTestAnswer = async () => {
    if(!userAnswer.trim()) return;
    setTestLoading(true);
    const question = content.qa[currentTestIndex].question;
    const correctAnswer = content.qa[currentTestIndex].answer;
    
    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true' },
        body: JSON.stringify({ 
          messages: [{ role: 'user', content: `Question: ${question}\nCorrect Answer: ${correctAnswer}\nUser Answer: ${userAnswer}\n\nEvaluate the user's answer. Is it correct? Provide a very brief, encouraging 1-2 sentence feedback.` }],
          topic_name: decodedTopic,
          engine: engine || 'groq'
        })
      });
      const data = await res.json();
      
      const newEntry = { question, userAnswer, feedback: data.reply, timestamp: new Date() };
      setTestFeedback(data.reply);
      setTestHistory(prev => [...prev, newEntry]);

      // Save to Firebase
      if(currentUser) {
        let sid = testSessionId;
        if(!sid) {
           sid = `Practice Session ${Math.floor(Math.random()*1000)}`;
           setTestSessionId(sid);
        }
        await addDoc(collection(db, `users/${currentUser.uid}/practice_sessions`), {
           sessionId: sid,
           topic: decodedTopic,
           question,
           userAnswer,
           feedback: data.reply,
           createdAt: serverTimestamp()
        });
      }

    } catch(e) {
      console.error(e);
      setTestFeedback("Error grading answer.");
    } finally {
      setTestLoading(false);
    }
  };

  const nextTestQuestion = () => {
    setTestFeedback(null);
    setUserAnswer('');
    if(currentTestIndex < content.qa.length - 1) {
       setCurrentTestIndex(prev => prev + 1);
    } else {
       setTestMode(false);
    }
  };

  const handleDoubtSubmit = async (e) => {
    e.preventDefault();
    if(!doubtText.trim() && !doubtFile) return;
    setDoubtLoading(true);
    setDoubtAnswer(null);

    const formData = new FormData();
    formData.append('question', doubtText || "Please explain this image related to " + decodedTopic);
    if(doubtFile) formData.append('file', doubtFile);

    try {
      const res = await fetch(`${API_BASE}/api/solve-doubt`, {
        method: 'POST',
        headers: { 'Bypass-Tunnel-Reminder': 'true' },
        body: formData
      });
      const data = await res.json();
      if(data.detail) throw new Error(data.detail);
      setDoubtAnswer(data.answer);
    } catch(error) {
      console.error(error);
      setDoubtAnswer(`Error: ${error.message}`);
    } finally {
      setDoubtLoading(false);
    }
  };

  const renderContent = () => {
      if (chatMode) {
        return (
          <div className="flex flex-col bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 h-[800px] relative overflow-hidden">
            <div className="p-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 flex justify-between items-center shrink-0">
              <h3 className="font-bold text-lg flex items-center gap-2"><BookOpen size={18} /> Full Study Notes & Discussion</h3>
              <button onClick={() => setChatMode(false)} className="px-4 py-2 text-sm font-medium bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                Exit
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto p-8 space-y-8 pb-32">
              <div className="prose dark:prose-invert max-w-none prose-sm">
                <ReactMarkdown components={MarkdownComponents}>{content.notes}</ReactMarkdown>
              </div>

              <div className="flex items-center gap-4 my-8">
                <div className="h-px bg-gray-200 dark:bg-gray-700 flex-1"></div>
                <span className="text-gray-400 dark:text-gray-500 text-sm font-medium">Ask questions about these notes</span>
                <div className="h-px bg-gray-200 dark:bg-gray-700 flex-1"></div>
              </div>

              <div className="space-y-6">
                {messages.length === 0 && (
                  <div className="text-center text-gray-500 mt-10">
                    <p>No questions yet. Ask anything below!</p>
                  </div>
                )}
                {messages.map((msg, i) => (
                  <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[85%] rounded-2xl p-4 ${msg.role === 'user' ? 'bg-[var(--matte-primary)] text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'}`}>
                      <div className="prose dark:prose-invert max-w-none prose-sm"><ReactMarkdown components={MarkdownComponents}>{msg.content}</ReactMarkdown></div>
                    </div>
                  </div>
                ))}
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="max-w-[85%] rounded-2xl p-4 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100"><Loader2 className="w-5 h-5 animate-spin" /></div>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>
            </div>

            <div className="p-4 bg-gray-50 dark:bg-gray-900/80 border-t border-gray-100 dark:border-gray-700 shrink-0 backdrop-blur-sm absolute bottom-0 left-0 right-0 z-10">
              <form onSubmit={handleSendMessage} className="flex gap-2">
                <input type="text" value={inputMsg} onChange={e => setInputMsg(e.target.value)} placeholder="Ask a question..." className="flex-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-xl px-4 py-3 outline-none focus:border-[var(--matte-primary)]" />
                <button type="submit" disabled={chatLoading || !inputMsg.trim()} className="bg-[var(--matte-primary)] text-white px-6 rounded-xl font-bold hover:opacity-90 disabled:opacity-50 transition-opacity flex items-center justify-center">
                  <Send size={18} />
                </button>
              </form>
            </div>
          </div>
        );
      }

    if (loading) {
      return (
        <div className="flex flex-col items-center justify-center py-20 text-gray-500 dark:text-gray-400">
          <Loader2 className="w-12 h-12 animate-spin mb-4" style={{ color: 'var(--matte-primary)' }} />
          <p className="text-lg animate-pulse">Generating {tabs.find(t => t.id === activeTab)?.label}...</p>
        </div>
      );
    }

    if (activeTab === 'notes' && content.notes) {
      return (
        <div className="relative">
          <div className="prose dark:prose-invert max-w-none bg-white dark:bg-gray-800 p-8 pb-32 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 max-h-[250px] overflow-hidden">
            <ReactMarkdown components={MarkdownComponents}>{content.notes}</ReactMarkdown>
          </div>
          
          <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-white via-white/80 to-transparent dark:from-gray-800 dark:via-gray-800/80 rounded-b-2xl flex justify-center items-end h-32">
            <button 
              onClick={() => {
                setChatMode(true);
                if(messages.length === 0) setMessages([{ role: 'assistant', content: `I've prepared notes on **${decodedTopic}**. What specific part would you like to discuss?` }]);
              }}
              className="bg-[var(--matte-primary)] text-white px-8 py-4 rounded-xl font-bold shadow-2xl hover:-translate-y-1 hover:shadow-3xl transition-all flex items-center gap-2 text-lg"
            >
              <MessageCircle size={24} /> Enter Full Notes & Chat Mode
            </button>
          </div>
        </div>
      );
    }

    if ((activeTab === 'qa' || activeTab === 'quiz') && !content[activeTab]) {
      return (
        <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 text-center max-w-lg mx-auto mt-10">
          <Settings className="w-12 h-12 mx-auto text-gray-400 mb-4" />
          <h2 className="text-2xl font-bold mb-6">Configure your {activeTab === 'qa' ? 'Q&A' : 'Quiz'}</h2>
          
          <div className="space-y-4 text-left">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Difficulty</label>
              <select value={settings.difficulty} onChange={e => setSettings({...settings, difficulty: e.target.value})} className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 outline-none">
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Number of Questions</label>
              <select value={settings.numQuestions} onChange={e => setSettings({...settings, numQuestions: e.target.value})} className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 outline-none">
                <option value="3">3 Questions</option>
                <option value="5">5 Questions</option>
                <option value="10">10 Questions</option>
              </select>
            </div>
                          <div className="flex gap-2 mt-4">
                <select
                  value={engine}
                  onChange={(e) => setEngine(e.target.value)}
                  className="p-3 border border-gray-200 dark:border-gray-700 rounded-xl outline-none bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white font-medium"
                >
                  <option value="groq">Groq (Fast)</option>
                  <option value="gemini">Gemini</option>
                </select>
                <button onClick={() => generateQAOrQuiz(activeTab)} className="flex-1 bg-[var(--matte-primary)] text-white font-bold py-3 rounded-xl hover:opacity-90 transition-all">
                  Generate Now
                </button>
              </div>
          </div>
        </div>
      );
    }

    if (activeTab === 'qa' && content.qa) {
      if (typeof content.qa === 'string') {
        return (
          <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-red-100 dark:border-red-900/30 text-center max-w-lg mx-auto mt-10">
            <h2 className="text-2xl font-bold mb-2 text-red-600 dark:text-red-400">Error Loading Q&A</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">{content.qa}</p>
            <button onClick={() => { setContent(prev => ({...prev, qa: null})); }} className="bg-[var(--matte-primary)] text-white font-bold py-2 px-6 rounded-xl hover:opacity-90 transition-all">Retry</button>
          </div>
        );
      }
      if (testMode) {
        const q = content.qa[currentTestIndex];
        return (
          <div className="max-w-2xl mx-auto space-y-6 mt-6">
            <div className="flex justify-between items-center mb-4">
              <span className="font-bold text-gray-500">Practice Session Question {currentTestIndex + 1} of {content.qa.length}</span>
              <button onClick={() => setTestMode(false)} className="text-red-500 hover:underline text-sm">Exit Test</button>
            </div>
            
            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
              <h3 className="text-xl font-bold mb-6">{q.question}</h3>
              
              {!testFeedback ? (
                <div className="space-y-4">
                  <textarea value={userAnswer} onChange={e => setUserAnswer(e.target.value)} placeholder="Type your answer here..." className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl p-4 min-h-[120px] outline-none" />
                  <button onClick={submitTestAnswer} disabled={testLoading || !userAnswer.trim()} className="w-full bg-[var(--matte-primary)] text-white py-3 rounded-xl font-bold flex justify-center items-center gap-2 disabled:opacity-50">
                    {testLoading ? <Loader2 className="animate-spin" size={20} /> : <><Send size={20} /> Submit Answer</>}
                  </button>
                </div>
              ) : (
                <div className="space-y-6">
                  <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700">
                    <span className="text-sm font-semibold text-gray-500">Your Answer:</span>
                    <p className="mt-1 text-gray-800 dark:text-gray-200">{userAnswer}</p>
                  </div>
                  <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-xl border border-green-200 dark:border-green-800">
                    <span className="text-sm font-semibold text-green-600 dark:text-green-500">AI Feedback:</span>
                    <div className="mt-1 text-green-800 dark:text-green-300 font-medium"><ReactMarkdown components={MarkdownComponents}>{testFeedback}</ReactMarkdown></div>
                  </div>
                  <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl border border-blue-200 dark:border-blue-800">
                    <span className="text-sm font-semibold text-blue-600 dark:text-blue-500">Correct Answer:</span>
                    <div className="mt-1 text-blue-800 dark:text-blue-300"><ReactMarkdown components={MarkdownComponents}>{q.answer}</ReactMarkdown></div>
                  </div>
                  <button onClick={nextTestQuestion} className="w-full bg-black dark:bg-white text-white dark:text-black py-3 rounded-xl font-bold">
                    {currentTestIndex < content.qa.length - 1 ? 'Next Question' : 'Finish Practice'}
                  </button>
                </div>
              )}
            </div>
          </div>
        );
      }

      return (
        <div>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold">Generated Q&A Flashcards</h2>
            <button onClick={() => { setTestMode(true); setCurrentTestIndex(0); setTestFeedback(null); setUserAnswer(''); }} className="bg-[var(--matte-primary)] text-white px-6 py-2 rounded-lg font-bold flex items-center gap-2 hover:opacity-90">
              <PlayCircle size={18} /> Test Yourself
            </button>
          </div>
          <div className="space-y-6">
            {content.qa.map((qa, i) => (
              <div key={i} className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
                <h3 className="font-bold text-lg mb-3 flex gap-3"><span className="text-blue-500">Q:</span> <span>{qa.question}</span></h3>
                <div className="pl-6 border-l-2 border-green-200 dark:border-green-800/50 pt-1">
                  <span className="font-semibold text-green-600 dark:text-green-500 block mb-1">Answer:</span>
                  <div className="text-gray-700 dark:text-gray-300"><ReactMarkdown components={MarkdownComponents}>{qa.answer}</ReactMarkdown></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    }

    if (activeTab === 'quiz' && content.quiz) {
      if (typeof content.quiz === 'string') {
        return (
          <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-red-100 dark:border-red-900/30 text-center max-w-lg mx-auto mt-10">
            <h2 className="text-2xl font-bold mb-2 text-red-600 dark:text-red-400">Error Loading Quiz</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">{content.quiz}</p>
            <button onClick={() => { setContent(prev => ({...prev, quiz: null})); }} className="bg-[var(--matte-primary)] text-white font-bold py-2 px-6 rounded-xl hover:opacity-90 transition-all">Retry</button>
          </div>
        );
      }
      return (
        <div className="space-y-8">
          <div className="flex justify-between items-center mb-6">
             <h2 className="text-xl font-bold">Practice Quiz</h2>
             <button onClick={() => setContent(prev => ({...prev, quiz: null}))} className="text-sm text-gray-500 hover:underline">Generate New Quiz</button>
          </div>
          {content.quiz.map((q, i) => (
            <QuizQuestion key={i} data={q} index={i} MarkdownComponents={MarkdownComponents} />
          ))}
        </div>
      );
    }

    if (activeTab === 'videos' && content.videos) {
      if (typeof content.videos === 'string') {
        return (
          <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-red-100 dark:border-red-900/30 text-center max-w-lg mx-auto mt-10">
            <Video className="w-12 h-12 mx-auto text-red-400 mb-4" />
            <h2 className="text-2xl font-bold mb-2 text-red-600 dark:text-red-400">Error Loading Videos</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">{content.videos}</p>
            <button onClick={() => { setContent(prev => ({...prev, videos: null})); fetchNotesOrVideos('videos'); }} className="bg-[var(--matte-primary)] text-white font-bold py-2 px-6 rounded-xl hover:opacity-90 transition-all">Retry</button>
          </div>
        );
      }
      if (Array.isArray(content.videos) && content.videos.length === 0) {
        return (
          <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 text-center max-w-lg mx-auto mt-10">
            <h2 className="text-2xl font-bold mb-2">No Videos Found</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">We couldn't find any video tutorials for this topic.</p>
            <button onClick={() => { setContent(prev => ({...prev, videos: null})); fetchNotesOrVideos('videos'); }} className="bg-[var(--matte-primary)] text-white font-bold py-2 px-6 rounded-xl hover:opacity-90 transition-all">Try Again</button>
          </div>
        );
      }
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {content.videos.map((vid, i) => (
            <a key={i} href={vid.video_id?.startsWith('http') ? vid.video_id : `https://www.youtube.com/watch?v=${vid.video_id}`} target="_blank" rel="noopener noreferrer" className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden hover:border-red-300 hover:shadow-md transition-all group flex flex-col">
              <div className="w-full h-40 bg-gray-200 dark:bg-gray-900 relative overflow-hidden">
                {vid.thumbnail_url ? (
                   <img src={vid.thumbnail_url} alt={vid.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                ) : (
                   <div className="absolute inset-0 flex items-center justify-center text-red-500"><Video size={48} className="opacity-20" /></div>
                )}
                <div className="absolute inset-0 bg-black/20 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                   <PlayCircle size={48} className="text-white drop-shadow-lg" />
                </div>
              </div>
              <div className="p-5 flex-1 flex flex-col justify-between">
                <div>
                  <h3 className="font-bold text-sm mb-2 line-clamp-2">{vid.title}</h3>
                  <p className="text-xs text-gray-500 dark:text-gray-400">{vid.channel_title || "YouTube"}</p>
                </div>
                <div className="mt-4 flex items-center gap-1 text-xs font-semibold text-red-600">
                  Watch Video <ExternalLink size={12} />
                </div>
              </div>
            </a>
          ))}
        </div>
      );
    }
    
    if (activeTab === 'doubt') {
      return (
        <div className="max-w-3xl mx-auto bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
          <h2 className="text-2xl font-bold mb-2 flex items-center gap-2"><Brain className="text-[var(--matte-primary)]" /> Doubt Solver</h2>
          <p className="text-gray-500 dark:text-gray-400 mb-8">Stuck on {decodedTopic}? Upload a screenshot or type your question and AI will explain it instantly.</p>
          
          <form onSubmit={handleDoubtSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold mb-2">Upload Image (Optional)</label>
              <div className="flex items-center justify-center w-full">
                  <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl cursor-pointer bg-gray-50 dark:bg-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800">
                      <div className="flex flex-col items-center justify-center pt-5 pb-6">
                          {doubtFile ? <p className="font-medium text-green-600">{doubtFile.name}</p> : <><Upload className="w-8 h-8 mb-3 text-gray-400" /><p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload</span> or drag and drop</p></>}
                      </div>
                      <input type="file" className="hidden" accept="image/*" onChange={(e) => setDoubtFile(e.target.files[0])} />
                  </label>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-semibold mb-2">Your Question</label>
              <textarea value={doubtText} onChange={e => setDoubtText(e.target.value)} placeholder="E.g. What does this diagram mean?" className="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl p-4 min-h-[120px] outline-none focus:border-[var(--matte-primary)]" />
            </div>

            <button type="submit" disabled={doubtLoading || (!doubtText.trim() && !doubtFile)} className="w-full bg-[var(--matte-primary)] text-white py-3 rounded-xl font-bold flex justify-center items-center gap-2 disabled:opacity-50">
              {doubtLoading ? <Loader2 className="animate-spin" /> : <><Sparkles size={20} /> Solve Doubt</>}
            </button>
          </form>

          {doubtAnswer && (
             <div className="mt-10 p-6 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-2xl">
               <h3 className="font-bold text-lg mb-4 text-[var(--matte-primary)]">AI Explanation</h3>
               <div className="prose dark:prose-invert max-w-none prose-sm"><ReactMarkdown components={MarkdownComponents}>{doubtAnswer}</ReactMarkdown></div>
             </div>
          )}
        </div>
      );
    }

    return null;
  };

  return (
    <div className="min-h-screen bg-transparent w-full overflow-y-auto" style={{ scrollbarGutter: 'stable' }}>
      <div className="max-w-5xl mx-auto px-6 py-12">
        <button onClick={() => navigate(`/exam/${id}`)} className="flex items-center gap-2 text-sm font-medium text-gray-500 hover:text-gray-900 dark:hover:text-gray-100 mb-8 transition-colors">
          <ArrowLeft size={16} /> Back to Curriculum
        </button>

        <div className="flex items-center gap-4 mb-10">
          <div className="w-16 h-16 rounded-2xl flex items-center justify-center shadow-lg" style={{ backgroundColor: 'var(--matte-primary)', color: 'white' }}>
            <Sparkles size={32} />
          </div>
          <div>
            <h1 className="text-4xl font-bold tracking-tight mb-2">Prep Mode</h1>
            <p className="text-lg opacity-70 flex items-center gap-2">Deep dive into <span className="font-semibold px-2 py-1 rounded-md bg-black/5 dark:bg-white/10">{decodedTopic}</span></p>
          </div>
        </div>

        {!chatMode && (
          <div className="flex flex-wrap gap-2 mb-8">
            {tabs.map(tab => (
              <button key={tab.id} onClick={() => setActiveTab(tab.id)} className={`flex items-center gap-2 px-5 py-3 rounded-xl font-medium transition-all ${activeTab === tab.id ? 'shadow-md scale-105' : 'bg-black/5 dark:bg-white/5 opacity-70 hover:opacity-100'}`} style={activeTab === tab.id ? { backgroundColor: 'var(--matte-primary)', color: 'white' } : {}}>
                <tab.icon size={18} /> {tab.label}
              </button>
            ))}
          </div>
        )}

        <div className="pb-24">{renderContent()}</div>
      </div>
    </div>
  );
}

function QuizQuestion({ data, index, MarkdownComponents }) {
  const [selected, setSelected] = useState(null);
  const isCorrect = selected === data.answer;

  return (
    <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
      <h3 className="text-xl font-bold mb-6"><span className="opacity-50 mr-2">{index + 1}.</span> {data.question}</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {data.options.map((opt, i) => (
          <button key={i} onClick={() => setSelected(opt)} disabled={selected !== null} className={`p-4 rounded-xl text-left font-medium transition-all border-2 ${selected === null ? 'border-gray-100 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-500 bg-gray-50 dark:bg-gray-900/30' : selected === opt ? (isCorrect ? 'border-green-500 bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-400' : 'border-red-500 bg-red-50 text-red-700 dark:bg-red-900/30 dark:text-red-400') : (opt === data.answer ? 'border-green-500 bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-400' : 'border-gray-100 dark:border-gray-700 opacity-50')}`}>
            {opt}
          </button>
        ))}
      </div>
      
      {selected !== null && (
        <div className={`mt-6 p-4 rounded-xl border ${isCorrect ? 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-900' : 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-900'}`}>
          <p className="font-bold mb-1 flex items-center gap-2">{isCorrect ? '✨ Correct!' : '❌ Incorrect.'}</p>
          <div className="opacity-80"><ReactMarkdown components={MarkdownComponents}>{data.explanation}</ReactMarkdown></div>
        </div>
      )}
    </div>
  );
}

