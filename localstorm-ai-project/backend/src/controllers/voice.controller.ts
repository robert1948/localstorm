import { Request, Response } from 'express';
import VoiceService from '../services/voice.service';

class VoiceController {
    private voiceService: VoiceService;

    constructor() {
        this.voiceService = new VoiceService();
    }

    public async recognizeSpeech(req: Request, res: Response): Promise<void> {
        try {
            const audioData = req.body.audioData;
            const result = await this.voiceService.recognizeSpeech(audioData);
            res.status(200).json(result);
        } catch (error) {
            res.status(500).json({ message: 'Error recognizing speech', error });
        }
    }

    public async synthesizeSpeech(req: Request, res: Response): Promise<void> {
        try {
            const text = req.body.text;
            const audioData = await this.voiceService.synthesizeSpeech(text);
            res.status(200).send(audioData);
        } catch (error) {
            res.status(500).json({ message: 'Error synthesizing speech', error });
        }
    }
}

export default new VoiceController();