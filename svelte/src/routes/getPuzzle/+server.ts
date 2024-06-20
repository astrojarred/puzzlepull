import { env } from '$env/dynamic/private';
import { json } from '@sveltejs/kit';

let API_URL = env?.API_URL;
if (!API_URL) {
	API_URL = "http://localhost:8000";
	console.log("WARNING: API_URL not found in environment variables, using default value: http://localhost:8000")
}

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
	// download puzzle from API
	const { url } = await request.json();
	const response = await fetch(`${env.API_URL}/guardian?url=${url}?download=true`);
	const data = await response.json();
	return json(data);
}
