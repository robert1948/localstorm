import { Request, Response, NextFunction } from 'express';

const monitoringMiddleware = (req: Request, res: Response, next: NextFunction) => {
    const start = Date.now();

    res.on('finish', () => {
        const duration = Date.now() - start;
        console.log(`Request to ${req.method} ${req.originalUrl} took ${duration}ms`);
        // Here you can also log other metrics like status code, request size, etc.
    });

    next();
};

export default monitoringMiddleware;