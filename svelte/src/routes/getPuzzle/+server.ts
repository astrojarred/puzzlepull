import { env } from '$env/dynamic/private';
import { json } from '@sveltejs/kit';
import { building } from '$app/environment';

let API_URL = env?.API_URL;
if (!API_URL || building) {
	API_URL = "http://localhost:8000";
	console.log("WARNING: API_URL not found in environment variables, using default value: http://localhost:8000")
} else {
	if (!API_URL) {
		throw new Error("API_URL not found in environment variables");
	}
}

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
	// download puzzle from API
	const { url } = await request.json();
	console.log("Fetching puzzle from", `${API_URL}/guardian?url=${url}?download=true`);
	const response = await fetch(`${API_URL}/guardian?url=${url}?download=true`);
	const data = await response.json();
	return json(data);
}
