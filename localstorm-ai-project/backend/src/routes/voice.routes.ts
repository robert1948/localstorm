import { Router } from 'express';
import { VoiceController } from '../controllers/voice.controller';

const router = Router();

// Route for speech recognition
router.post('/recognize', VoiceController.recognizeSpeech);

// Route for speech synthesis
router.post('/synthesize', VoiceController.synthesizeSpeech);

// Route for getting voice profiles
router.get('/profiles', VoiceController.getVoiceProfiles);

// Route for adding a new voice profile
router.post('/profiles', VoiceController.addVoiceProfile);

// Route for updating a voice profile
router.put('/profiles/:id', VoiceController.updateVoiceProfile);

// Route for deleting a voice profile
router.delete('/profiles/:id', VoiceController.deleteVoiceProfile);

export default router;