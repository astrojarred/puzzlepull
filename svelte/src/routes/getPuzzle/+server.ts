import { building } from '$app/environment';
import { env } from '$env/dynamic/private';
import { json, error } from '@sveltejs/kit';

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
	const { url } = await request.json();

	if (!url) {
		throw error(400, "url not found in request");
	}

	const endpoint = `${API_URL}/pull?url=${encodeURIComponent(url)}&download=true`;
	console.log("Fetching puzzle from", endpoint);
	const response = await fetch(endpoint);

	if (!response.ok) {
		let detail = `Upstream error ${response.status}`;
		try {
			const body = await response.json();
			detail = body?.detail || detail;
		} catch {
			// ignore parse errors
		}
		throw error(response.status, detail);
	}

	const data = await response.json();
	return json(data);
}
