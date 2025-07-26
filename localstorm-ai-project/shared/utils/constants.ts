export const API_BASE_URL = 'https://api.localstorm-ai.com';
export const TIMEOUT = 5000; // 5 seconds
export const MAX_RETRIES = 3;

export const DEFAULT_LANGUAGE = 'en';
export const SUPPORTED_LANGUAGES = ['en', 'es', 'fr', 'de', 'zh'];

export const USER_ROLES = {
    ADMIN: 'admin',
    DEVELOPER: 'developer',
    ANALYST: 'analyst',
    USER: 'user',
};

export const ANALYTICS_METRICS = {
    ENGAGEMENT: 'engagement',
    RETENTION: 'retention',
    CONVERSION: 'conversion',
};

export const VOICE_PROVIDERS = {
    GOOGLE: 'Google Cloud',
    OPENAI: 'OpenAI Whisper',
    ELEVENLABS: 'ElevenLabs',
    SYSTEM_TTS: 'System TTS',
};