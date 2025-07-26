import { Injectable } from 'nestjs/common';
import { VoiceRecognitionService } from '../utils/voiceRecognition';
import { VoiceSynthesisService } from '../utils/voiceSynthesis';

@Injectable()
export class VoiceService {
    private recognitionService: VoiceRecognitionService;
    private synthesisService: VoiceSynthesisService;

    constructor() {
        this.recognitionService = new VoiceRecognitionService();
        this.synthesisService = new VoiceSynthesisService();
    }

    async recognizeSpeech(audioInput: Buffer): Promise<string> {
        return await this.recognitionService.recognize(audioInput);
    }

    async synthesizeSpeech(text: string): Promise<Buffer> {
        return await this.synthesisService.synthesize(text);
    }
}