import { useState, useEffect, useRef } from 'react';
import { BookOpen, Send, Plus, Loader2 } from 'lucide-react';
import { useAI } from '../contexts/AIContext';
import { useAuth } from '../contexts/AuthContext';
import { db } from '../lib/firebase';
import { collection, addDoc, getDocs, doc, updateDoc, query, orderBy, serverTimestamp } from 'firebase/firestore';

export default function NotesView() {
  const [savedNotes, setSavedNotes] = useState([]);
  const [selectedNote, setSelectedNote] = useState(null);
  
  const [topicName, setTopicName] = useState('');
  const [loadingNotes, setLoadingNotes] = useState(false);
  
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  
  const { engine } = useAI();
  const { currentUser } = useAuth();
  
  const messagesEndRef = useRef(null);

  // Fetch saved notes on mount
  useEffect(() => {
    if (currentUser) {
      fetchHistory();
    }
  }, [currentUser]);

  const fetchHistory = async () => {
    try {
      const q = query(collection(db, `users/${currentUser.uid}/notes`), orderBy('createdAt', 'desc'));
      const snap = await getDocs(q);
      const notesList = snap.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      setSavedNotes(notesList);
    } catch (e) {
      console.error(e);
    }
  };

  const createNotes = async () => {
    if (!topicName || !currentUser) return;
    setLoadingNotes(true);
    try {
      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${API_BASE}/api/generate-notes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true' },
        body: JSON.stringify({ topic_name: topicName, engine: engine })
      });
      if (!response.ok) throw new Error("Failed");
      const data = await response.json();
      
      const noteDoc = {
        topic_name: data.topic_name,
        sections: data.sections,
        summary: data.summary,
        chatHistory: [],
        createdAt: serverTimestamp()
      };
      
      const docRef = await addDoc(collection(db, `users/${currentUser.uid}/notes`), noteDoc);
      const fullNote = { id: docRef.id, ...noteDoc, createdAt: new Date() };
      
      setSavedNotes([fullNote, ...savedNotes]);
      setSelectedNote(fullNote);
      setTopicName('');
    } catch (e) {
      console.error("Full Error:", e);
      alert("Error: " + e.message + "\n\nIf it says 'Failed', check localtunnel and backend. If it says 'Missing or insufficient permissions', check Firestore rules.");
    } finally {
      setLoadingNotes(false);
    }
  };

  const handleSendMessage = async () => {
    if (!chatInput.trim() || !selectedNote) return;
    
    const userMsg = { role: 'user', content: chatInput };
    const newHistory = [...(selectedNote.chatHistory || []), userMsg];
    
    // Optimistic UI update
    setSelectedNote({ ...selectedNote, chatHistory: newHistory });
    setChatInput('');
    setChatLoading(true);
    
    try {
      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Bypass-Tunnel-Reminder': 'true' },
        body: JSON.stringify({ 
          messages: newHistory,
          topic_name: selectedNote.topic_name,
          engine: engine
        })
      });
      
      if (!response.ok) throw new Error("Chat failed");
      const data = await response.json();
      
      const aiMsg = { role: 'assistant', content: data.reply };
      const updatedHistory = [...newHistory, aiMsg];
      
      // Update state
      const updatedNote = { ...selectedNote, chatHistory: updatedHistory };
      setSelectedNote(updatedNote);
      
      // Update Firestore
      await updateDoc(doc(db, `users/${currentUser.uid}/notes`, selectedNote.id), {
        chatHistory: updatedHistory
      });
      
    } catch (e) {
      console.error(e);
      alert("Error sending message.");
    } finally {
      setChatLoading(false);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [selectedNote?.chatHistory]);

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col md:flex-row gap-6">
      {/* Left Sidebar - History */}
      <div className="w-full md:w-1/3 lg:w-1/4 bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-xl shadow-sm flex flex-col overflow-hidden shrink-0">
        <div className="p-4 border-b dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 flex justify-between items-center">
          <h2 className="font-bold text-gray-700 dark:text-gray-200">My Notes</h2>
          <button 
            onClick={() => setSelectedNote(null)}
            className="p-1.5 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-200 transition-colors"
            title="New Note"
          >
            <Plus size={18} />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {savedNotes.length === 0 ? (
            <div className="p-4 text-center text-gray-500 text-sm">No saved notes yet.</div>
          ) : (
            savedNotes.map(note => (
              <button
                key={note.id}
                onClick={() => setSelectedNote(note)}
                className={`w-full text-left p-3 rounded-lg transition-colors flex items-center gap-3 ${selectedNote?.id === note.id ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400' : 'hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'}`}
              >
                <BookOpen size={16} className="shrink-0" />
                <span className="truncate text-sm font-medium">{note.topic_name}</span>
              </button>
            ))
          )}
        </div>
      </div>

      {/* Right Area - Main Content */}
      <div className="flex-1 flex flex-col bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-xl shadow-sm overflow-hidden min-w-0">
        {!selectedNote ? (
          <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
            <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-full mb-4">
              <BookOpen size={48} className="text-blue-500" />
            </div>
            <h2 className="text-2xl font-bold mb-2">Create New Notes</h2>
            <p className="text-gray-500 dark:text-gray-400 mb-6 max-w-md">Generate AI-powered revision notes and chat with your tutor to master any topic.</p>
            
            <div className="w-full max-w-md flex flex-col gap-3">
              <input 
                type="text" 
                value={topicName}
                onChange={e => setTopicName(e.target.value)}
                placeholder="Enter a topic (e.g., 'Linear Regression')" 
                className="w-full p-3 border border-gray-200 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
              />
              <button 
                onClick={createNotes}
                disabled={loadingNotes || !topicName}
                className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center gap-2 transition-colors"
              >
                {loadingNotes ? <Loader2 className="animate-spin" size={20} /> : 'Generate Notes'}
              </button>
            </div>
          </div>
        ) : (
          <div className="flex-1 flex flex-col overflow-hidden relative">
            {/* Note Content Scroll Area */}
            <div className="flex-1 overflow-y-auto p-6 lg:p-8 space-y-8">
              <div>
                <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100 border-b dark:border-gray-700 pb-4">{selectedNote.topic_name} - Revision Notes</h2>
                <div className="space-y-6">
                  {selectedNote.sections?.map((sec, i) => (
                    <div key={i}>
                      <h3 className="text-xl font-semibold text-blue-800 dark:text-blue-400 mb-2">{sec.heading}</h3>
                      <p className="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line">{sec.content}</p>
                    </div>
                  ))}
                </div>
                <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
                  <h4 className="font-bold text-gray-900 dark:text-gray-100 mb-2">Summary</h4>
                  <p className="text-gray-600 dark:text-gray-400 italic">{selectedNote.summary}</p>
                </div>
              </div>

              {/* Chat Divider */}
              <div className="relative py-4">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-200 dark:border-gray-700"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">Ask questions about these notes</span>
                </div>
              </div>

              {/* Chat History */}
              <div className="space-y-4 pb-4">
                {selectedNote.chatHistory?.map((msg, idx) => (
                  <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[80%] p-3 rounded-2xl ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-br-sm' : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-sm whitespace-pre-wrap'}`}>
                      {msg.content}
                    </div>
                  </div>
                ))}
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 p-3 rounded-2xl rounded-bl-sm flex gap-2 items-center h-10">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.15s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.3s' }}></div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            </div>

            {/* Chat Input */}
            <div className="p-4 bg-gray-50 dark:bg-gray-900/50 border-t dark:border-gray-700">
              <div className="flex gap-2">
                <input 
                  type="text" 
                  value={chatInput}
                  onChange={e => setChatInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Ask a question..."
                  className="flex-1 p-3 rounded-xl border border-gray-200 dark:border-gray-700 focus:ring-2 focus:ring-blue-500 outline-none bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
                <button 
                  onClick={handleSendMessage}
                  disabled={chatLoading || !chatInput.trim()}
                  className="bg-blue-600 text-white p-3 rounded-xl hover:bg-blue-700 disabled:opacity-50 transition-colors shrink-0"
                >
                  <Send size={20} />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
