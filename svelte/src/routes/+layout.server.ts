import { REDIS_URL } from '$env/static/private';
// grab the counter from the api
import { createClient } from 'redis';

const client = createClient({
    url: REDIS_URL
});

client.connect();

const counter = await client.get('puzzlepull_counter');

export const load = async () => {
    return { counter };
}
