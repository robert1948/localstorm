import { Schema, model } from 'mongoose';

const analyticsSchema = new Schema({
    userId: {
        type: String,
        required: true,
    },
    engagementMetrics: {
        sessionDuration: {
            type: Number,
            required: true,
        },
        pageViews: {
            type: Number,
            required: true,
        },
        interactions: {
            type: Number,
            required: true,
        },
    },
    createdAt: {
        type: Date,
        default: Date.now,
    },
    updatedAt: {
        type: Date,
        default: Date.now,
    },
});

const Analytics = model('Analytics', analyticsSchema);

export default Analytics;