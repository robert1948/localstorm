import { useState, useEffect } from 'react';
import { fetchAIResponse } from '../services/ai.service';

const useAI = (input) => {
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (input) {
            setLoading(true);
            fetchAIResponse(input)
                .then((data) => {
                    setResponse(data);
                    setLoading(false);
                })
                .catch((err) => {
                    setError(err);
                    setLoading(false);
                });
        }
    }, [input]);

    return { response, loading, error };
};

export default useAI;