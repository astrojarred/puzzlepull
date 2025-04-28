import { REDIS_URL } from '$env/static/private';
import { createClient } from 'redis';

export const load = async () => {
    const client = createClient({
        url: REDIS_URL
    });

    try {
        await client.connect();
        const counter = await client.get('puzzlepull_counter');
        await client.quit(); // Clean up the connection
        console.log("COUNTER", counter);
        return { counter };
    } catch (error) {
        console.error('Redis connection error:', error);
        return { counter: '0' }; // Provide a fallback value
    }
}
