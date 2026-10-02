import { createContext, useContext, useState, useEffect } from 'react';

const AIContext = createContext();

export function useAI() {
    return useContext(AIContext);
}

export function AIProvider({ children }) {
    // Default to groq but load from localStorage if available
    const [engine, setEngineState] = useState(() => {
        const saved = localStorage.getItem('exammind_ai_engine');
        return saved || 'groq';
    });
    const [syllabusData, setSyllabusData] = useState(null);

    const setEngine = (newEngine) => {
        setEngineState(newEngine);
        localStorage.setItem('exammind_ai_engine', newEngine);
    };

    return (
        <AIContext.Provider value={{ engine, setEngine, syllabusData, setSyllabusData }}>
            {children}
        </AIContext.Provider>
    );
}