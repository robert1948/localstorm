import { Request, Response, NextFunction } from 'express';
import { body, validationResult } from 'express-validator';

// Middleware for enhancing security through input validation
const securityMiddleware = [
    body('username').isString().isLength({ min: 3 }).withMessage('Username must be at least 3 characters long'),
    body('password').isString().isLength({ min: 6 }).withMessage('Password must be at least 6 characters long'),
    body('email').isEmail().withMessage('Invalid email format'),

    (req: Request, res: Response, next: NextFunction) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }
        next();
    }
];

export default securityMiddleware;