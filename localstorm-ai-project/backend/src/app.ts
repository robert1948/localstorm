import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import { authRoutes } from './routes/auth.routes';
import { aiRoutes } from './routes/ai.routes';
import { conversationRoutes } from './routes/conversation.routes';
import { analyticsRoutes } from './routes/analytics.routes';
import { voiceRoutes } from './routes/voice.routes';
import { projectRoutes } from './routes/project.routes';
import { monitoringMiddleware } from './middleware/monitoring.middleware';
import { securityMiddleware } from './middleware/security.middleware';

const app = express();

// Middleware setup
app.use(cors());
app.use(bodyParser.json());
app.use(monitoringMiddleware);
app.use(securityMiddleware);

// Route setup
app.use('/api/auth', authRoutes);
app.use('/api/ai', aiRoutes);
app.use('/api/conversation', conversationRoutes);
app.use('/api/analytics', analyticsRoutes);
app.use('/api/voice', voiceRoutes);
app.use('/api/project', projectRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});

export default app;