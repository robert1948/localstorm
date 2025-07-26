import { useEffect, useState } from 'react';
import { voiceService } from '../services/voice.service';

const useVoice = () => {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState('');

    const startListening = () => {
        setIsListening(true);
        voiceService.startRecognition((result) => {
            setTranscript(result);
        });
    };

    const stopListening = () => {
        setIsListening(false);
        voiceService.stopRecognition();
    };

    useEffect(() => {
        if (isListening) {
            startListening();
        } else {
            stopListening();
        }

        return () => {
            stopListening();
        };
    }, [isListening]);

    return { isListening, transcript, startListening, stopListening };
};

export default useVoice;