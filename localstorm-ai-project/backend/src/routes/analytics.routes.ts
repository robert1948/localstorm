import { Router } from 'express';
import { getAnalyticsData, postAnalyticsData } from '../controllers/analytics.controller';

const router = Router();

// Route to get analytics data
router.get('/analytics', getAnalyticsData);

// Route to post analytics data
router.post('/analytics', postAnalyticsData);

export default router;