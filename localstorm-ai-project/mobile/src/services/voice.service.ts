import { Audio } from 'expo-av';

class VoiceService {
    private audio: Audio.Sound;

    constructor() {
        this.audio = new Audio.Sound();
    }

    async startRecording() {
        try {
            await Audio.requestPermissionsAsync();
            await this.audio.prepareToRecordAsync(Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY);
            await this.audio.startAsync();
        } catch (error) {
            console.error('Error starting recording:', error);
        }
    }

    async stopRecording() {
        try {
            await this.audio.stopAndUnloadAsync();
            const uri = this.audio.getURI(); 
            return uri;
        } catch (error) {
            console.error('Error stopping recording:', error);
        }
    }

    async playSound(uri: string) {
        try {
            const { sound } = await Audio.Sound.createAsync({ uri });
            await sound.playAsync();
        } catch (error) {
            console.error('Error playing sound:', error);
        }
    }

    async dispose() {
        await this.audio.unloadAsync();
    }
}

export default new VoiceService();