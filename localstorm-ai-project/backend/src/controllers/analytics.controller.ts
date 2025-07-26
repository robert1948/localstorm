import { Request, Response } from 'express';
import AnalyticsService from '../services/analytics.service';

class AnalyticsController {
    private analyticsService: AnalyticsService;

    constructor() {
        this.analyticsService = new AnalyticsService();
    }

    public async getUserEngagementMetrics(req: Request, res: Response): Promise<void> {
        try {
            const metrics = await this.analyticsService.getUserEngagementMetrics();
            res.status(200).json(metrics);
        } catch (error) {
            res.status(500).json({ message: 'Error retrieving engagement metrics', error });
        }
    }

    public async getFeatureUsageData(req: Request, res: Response): Promise<void> {
        try {
            const usageData = await this.analyticsService.getFeatureUsageData();
            res.status(200).json(usageData);
        } catch (error) {
            res.status(500).json({ message: 'Error retrieving feature usage data', error });
        }
    }

    public async getAnalyticsOverview(req: Request, res: Response): Promise<void> {
        try {
            const overview = await this.analyticsService.getAnalyticsOverview();
            res.status(200).json(overview);
        } catch (error) {
            res.status(500).json({ message: 'Error retrieving analytics overview', error });
        }
    }
}

export default new AnalyticsController();