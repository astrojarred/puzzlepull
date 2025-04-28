import { building } from '$app/environment';
import { env } from '$env/dynamic/private';
import { json } from '@sveltejs/kit';

let API_URL = env?.API_URL;
if (!API_URL || building) {
	API_URL = "http://localhost:8000";
	console.log("WARNING: API_URL not found in environment variables, using default value: http://localhost:8000")
} else {
	if (!API_URL) {
		throw new Error("API_URL not found in environment variables");
	}
}

const ENDPOINT_MAP = {
	"www.theguardian.com": "guardian",
	"observer.co.uk": "observer"
}

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
	// download puzzle from API
	const { url, urlSite } = await request.json();

	if (!urlSite) {
		throw new Error("urlSite not found in request");
	}

	if (!ENDPOINT_MAP[urlSite as keyof typeof ENDPOINT_MAP]) {
		throw new Error(`${urlSite} not implemented.`);
	}

	const endpoint = ENDPOINT_MAP[urlSite as keyof typeof ENDPOINT_MAP];
	console.log("Fetching puzzle from", `${API_URL}/${endpoint}?url=${url}&download=true`);
	const response = await fetch(`${API_URL}/${endpoint}?url=${url}&download=true`);
	const data = await response.json();
	return json(data);
}
