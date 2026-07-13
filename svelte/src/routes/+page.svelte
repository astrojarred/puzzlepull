<script lang="ts">
	import type { LayoutProps } from './$types';

	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import * as Alert from '$lib/components/ui/alert/index.js';

	import { validHostnames } from '$lib/validHostnames.json';
	import LoaderCircle from "lucide-svelte/icons/loader-circle";

	let { data, children }: LayoutProps = $props();


	const hostnameList = Object.keys(validHostnames);

	// validation response type
	type ValidationResponse = {
		valid: boolean;
		hostname: string;
		message: string;
	};

	// validate the URL
	let validateURL = (puzzleURL: string): ValidationResponse => {
		// catch empty string
		if (puzzleURL === '') {
			return {
				valid: false,
				hostname: '',
				message: 'Please enter a URL'
			};
		}

		try {
			new URL(puzzleURL);

			let hostname = getURLsite(puzzleURL);

			if (hostnameList.includes(hostname)) {
				return {
					valid: true,
					hostname: hostname,
					message: `Site: ${validHostnames[hostname as keyof typeof validHostnames]}`
				};
			} else {
				return {
					valid: false,
					hostname: hostname,
					message: 'Site not supported'
				};
			}
		} catch (e) {
			return {
				valid: false,
				hostname: '',
				message: 'Invalid URL'
			};
		}
	};

	let getURLsite = (puzzleURL: string) => {
		try {
			let url = new URL(puzzleURL);
			return url.hostname;
		} catch (e) {
			return '';
		}
	};

	let downloadPuzzle = async () => {
		loading = true;
		errorMessage = '';
		console.log('Downloading puzzle', puzzleURL);
		// fetch the puzzle
		const response = await fetch('/getPuzzle', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ url: puzzleURL })
		});

		if (response.ok) {
			const jsonInfo = await response.json();
			// download the puzzle as a file
			const blob = new Blob([JSON.stringify(jsonInfo)], { type: 'application/json' });
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = jsonInfo?.annotation ? `${jsonInfo.annotation}` : 'puzzle.ipuz';
			document.body.appendChild(a);
			a.click();
			URL.revokeObjectURL(url);
			// increment the counter
			const counterResponse = await fetch('/counter');
			const counterData = await counterResponse.json();
			downloadCount = counterData.counter;
			errorMessage = '';
		} else {
			console.error(response);
			try {
				const errBody = await response.json();
				errorMessage = errBody?.message || `Download failed (${response.status})`;
			} catch {
				errorMessage = `Download failed (${response.status})`;
			}
		}
		loading = false;
	};

	let puzzleURL = $state('');
	let downloadCount = $state(data.counter || 0); // Track number of downloads
	let urlInfo = $derived(validateURL(puzzleURL));
	let urlSite = $derived(urlInfo?.hostname);
	let urlValid = $derived(urlInfo?.valid);
	let urlMessage = $derived(urlInfo?.message);
	let loading = $state(false);
	let errorMessage = $state('');
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Download any puzzle into a .ipuz file format</Card.Title>
		<Card.Description>Simply paste the URL below • {downloadCount} puzzles downloaded so far</Card.Description>
	</Card.Header>
	<Card.Content>
		<Alert.Root class="mb-4">
			<Alert.Title>
				<p>{urlMessage}</p>
				{#if urlSite === "observer.co.uk" || urlSite === "www.observer.co.uk"}
					<p class="text-sm mt-1 text-muted-foreground">
						Note: Only the Everyman and Speedy puzzles are currently supported.
					</p>
				{/if}
				{#if errorMessage}
					<p class="text-sm mt-1 text-destructive">{errorMessage}</p>
				{/if}
			</Alert.Title>
		</Alert.Root>
		<form>
			<Input
				placeholder="Puzzle URL"
				bind:value={puzzleURL}
				class={urlValid || puzzleURL === '' ? 'bg-white' : 'bg-destructive bg-opacity-20'}
			/>
		</form>
	</Card.Content>
	<Card.Footer class="flex flex-col items-start border-t px-6 py-4">
		<Button disabled={!urlValid || loading} onclick={downloadPuzzle}>
			{#if loading}
				<LoaderCircle class="mr-2 h-4 w-4 animate-spin" />
				Downloading...
			{:else}
				Download
			{/if}
		</Button>

	</Card.Footer>
</Card.Root>
