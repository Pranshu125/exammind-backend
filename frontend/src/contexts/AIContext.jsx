import { createContext, useContext, useState } from 'react';

const AIContext = createContext();

export function useAI() {
    return useContext(AIContext);
}

export function AIProvider({ children }) {
    // Default to groq because OpenAI account has no credits
    const [engine, setEngine] = useState('groq');
    const [syllabusData, setSyllabusData] = useState(null);

    return (
        <AIContext.Provider value={{ engine, setEngine, syllabusData, setSyllabusData }}>
            {children}
        </AIContext.Provider>
    );
}
