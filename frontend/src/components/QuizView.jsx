import { useState } from 'react';
import { HelpCircle } from 'lucide-react';
import { useAI } from '../contexts/AIContext';

import CustomSelect from './CustomSelect';

export default function QuizView() {
  const [topicName, setTopicName] = useState('');
  const [difficulty, setDifficulty] = useState('Medium');
  const [numQuestions, setNumQuestions] = useState(3);
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(false);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const { engine } = useAI();

  const difficultyOptions = [
    { value: 'Beginner', label: 'Beginner' },
    { value: 'Medium', label: 'Medium' },
    { value: 'Advanced', label: 'Advanced' }
  ];

  const fetchQuiz = async () => {
    if (!topicName) return;
    setLoading(true);
    setAnswers({});
    setShowResults(false);
    try {
      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${API_BASE}/api/generate-quiz`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Bypass-Tunnel-Reminder': 'true'
        },
        body: JSON.stringify({ 
          topic_name: topicName, 
          engine: engine,
          difficulty: difficulty,
          num_questions: Number(numQuestions)
        })
      });
      if (!response.ok) throw new Error("Failed");
      const data = await response.json();
      setQuiz(data);
    } catch (e) {
      alert("Error generating quiz. Make sure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = (qIndex, label) => {
    if (showResults) return;
    setAnswers(prev => ({ ...prev, [qIndex]: label }));
  };

  const calculateScore = () => {
    let score = 0;
    quiz.questions.forEach((q, i) => {
      if (answers[i] === q.correct_option_label) score++;
    });
    return score;
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex flex-col md:flex-row gap-4 items-center">
        <HelpCircle className="text-purple-500 hidden md:block shrink-0" size={32} />
        <input 
          type="text" 
          value={topicName}
          onChange={e => setTopicName(e.target.value)}
          placeholder="Enter a topic to generate a quiz" 
          className="flex-1 p-3 border rounded-lg focus:ring-2 focus:ring-purple-500 outline-none w-full min-w-0"
        />
        <div className="flex gap-3 w-full md:w-auto">
          <CustomSelect 
            value={difficulty}
            onChange={e => setDifficulty(e.target.value)}
            options={difficultyOptions}
            className="flex-1 md:flex-none md:w-40"
          />
          <input 
            type="number" 
            min="1"
            max="20"
            value={numQuestions}
            onChange={e => setNumQuestions(e.target.value)}
            placeholder="Qty"
            className="w-20 p-3 border rounded-lg focus:ring-2 focus:ring-purple-500 outline-none text-center"
            title="Number of Questions"
          />
        </div>
        <button 
          onClick={fetchQuiz}
          disabled={loading || !topicName}
          className="bg-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-purple-700 disabled:opacity-50 w-full md:w-auto shrink-0"
        >
          {loading ? 'Generating...' : 'Generate Quiz'}
        </button>
      </div>

      {quiz && (
        <div className="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 animate-in fade-in">
          <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-gray-100 border-b pb-4">Quiz: {quiz.topic_name}</h2>
          
          <div className="space-y-8">
            {quiz.questions?.map((q, qIndex) => (
              <div key={qIndex} className="p-6 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-100 dark:border-gray-700">
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4">{qIndex + 1}. {q.question}</h3>
                <div className="space-y-3">
                  {q.options.map((opt) => {
                    const isSelected = answers[qIndex] === opt.label;
                    const isCorrect = opt.label === q.correct_option_label;
                    
                    let bgClass = "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-600 hover:border-purple-300";
                    if (isSelected) bgClass = "bg-purple-50 border-purple-500";
                    
                    if (showResults) {
                      if (isCorrect) bgClass = "bg-green-50 border-green-500 text-green-900";
                      else if (isSelected && !isCorrect) bgClass = "bg-red-50 border-red-500 text-red-900";
                      else bgClass = "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-600 opacity-50";
                    }

                    return (
                      <div 
                        key={opt.label} 
                        onClick={() => handleSelect(qIndex, opt.label)}
                        className={`p-4 border rounded-lg cursor-pointer transition-colors flex items-center gap-3 ${bgClass}`}
                      >
                        <div className={`w-6 h-6 rounded flex items-center justify-center font-bold text-sm ${showResults && isCorrect ? 'bg-green-200 text-green-800' : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'}`}>
                          {opt.label}
                        </div>
                        <span className="flex-1">{opt.text}</span>
                      </div>
                    );
                  })}
                </div>
                {showResults && (
                  <div className="mt-4 p-4 bg-blue-50 text-blue-900 rounded-lg text-sm">
                    <strong>Explanation:</strong> {q.explanation}
                  </div>
                )}
              </div>
            ))}
          </div>

          {!showResults ? (
            <button 
              onClick={() => setShowResults(true)}
              disabled={Object.keys(answers).length < quiz.questions.length}
              className="mt-8 w-full bg-gray-900 text-white py-3 rounded-lg font-medium hover:bg-gray-800 disabled:opacity-50 transition-colors"
            >
              Submit Quiz
            </button>
          ) : (
            <div className="mt-8 p-6 bg-purple-50 border border-purple-200 rounded-xl text-center">
              <h3 className="text-2xl font-bold text-purple-900 mb-2">
                Your Score: {calculateScore()} / {quiz.questions.length}
              </h3>
              <p className="text-purple-700">
                {calculateScore() === quiz.questions.length ? 'Perfect! You mastered this topic.' : 'Keep reviewing the notes!'}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
