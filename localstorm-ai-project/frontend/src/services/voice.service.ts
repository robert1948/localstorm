import axios from 'axios';

const API_URL = '/api/voice';

class VoiceService {
    async recognizeSpeech(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob);

        const response = await axios.post(`${API_URL}/recognize`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        return response.data;
    }

    async synthesizeSpeech(text) {
        const response = await axios.post(`${API_URL}/synthesize`, { text });

        return response.data;
    }

    async getVoiceProfiles() {
        const response = await axios.get(`${API_URL}/profiles`);

        return response.data;
    }
}

export default new VoiceService();