import { createClient } from 'redis';

const redisClient = createClient({
    url: process.env.REDIS_URL || 'redis://localhost:6379'
});

redisClient.on('error', (err) => {
    console.error('Redis Client Error', err);
});

const connectRedis = async () => {
    await redisClient.connect();
};

const disconnectRedis = async () => {
    await redisClient.quit();
};

const setCache = async (key: string, value: string, expirationInSeconds: number) => {
    await redisClient.set(key, value, {
        EX: expirationInSeconds,
    });
};

const getCache = async (key: string) => {
    return await redisClient.get(key);
};

export { connectRedis, disconnectRedis, setCache, getCache };