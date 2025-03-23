<script lang="ts">
	import type { LayoutProps } from './$types';

	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import * as Alert from '$lib/components/ui/alert/index.js';

	import { validHostnames } from '$lib/validHostnames.json';

	let { data, children }: LayoutProps = $props();

	const hostnameList = Object.keys(validHostnames);

	// validate the URL
	let validateURL = (puzzleURL: string) => {
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
					message: `Site: ${validHostnames[hostname]}`
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
			const clonedResponse = response.clone();
			const downloadData = await response.blob();
			const jsonInfo = await clonedResponse.json();
			// download the puzzle as a file
			const url = URL.createObjectURL(downloadData);
			const a = document.createElement('a');
			a.href = url;
			a.download = jsonInfo?.annotation ? `${jsonInfo.annotation}` : 'puzzle.ipuz';
			document.body.appendChild(a);
			a.click();
			URL.revokeObjectURL(url);
			// increment the counter
			downloadCount++;
		} else {
			console.error(response);
		}
	};

	let puzzleURL = $state('');
	let downloadCount = $state(data.counter || 0); // Track number of downloads
	let urlInfo = $derived(validateURL(puzzleURL));
	let urlSite = $derived(urlInfo?.hostname);
	let urlValid = $derived(urlInfo?.valid);
	let urlMessage = $derived(urlInfo?.message);
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Download any puzzle into a .puz file format</Card.Title>
		<Card.Description>Simply paste the URL below • {downloadCount} puzzles downloaded so far</Card.Description>
	</Card.Header>
	<Card.Content>
		<Alert.Root class="mb-4">
			<Alert.Title>
				<p>{urlMessage}</p>
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
		<Button disabled={!urlValid} on:click={downloadPuzzle}>Download</Button>
	</Card.Footer>
</Card.Root>
