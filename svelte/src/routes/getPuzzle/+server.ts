import { API_URL } from '$env/static/private';
import { json } from '@sveltejs/kit';

if (!API_URL) {
	throw new Error('API_URL is not defined');
}

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
	// download puzzle from API
	const { url } = await request.json();
	const response = await fetch(`${API_URL}/guardian?url=${url}?download=true`);
	const data = await response.json();
	return json(data);
}
