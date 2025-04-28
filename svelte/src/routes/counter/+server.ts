import { building } from "$app/environment";
import { env } from "$env/dynamic/private";

//** @type {import('./$types').RequestHandler} */
export async function GET({ request, fetch }) {
    // pull the counter from the API
    let API_URL = env?.API_URL;

    if (!API_URL || building) {
        API_URL = "http://localhost:8000";
        console.log("WARNING: API_URL not found in environment variables, using default value: http://localhost:8000")
    } else {
        if (!API_URL) {
            throw new Error("API_URL not found in environment variables");
        }
    }

    try {
        const response = await fetch(`${API_URL}/counter`);
        const data = await response.json();
        return Response.json({ counter: data.counter });
    } catch (error) {
        console.error('Error fetching counter:', error);
        return Response.json({ counter: '0' });
    }
}
