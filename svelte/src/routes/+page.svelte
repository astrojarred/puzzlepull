<script lang="ts">
	import type { PageProps } from './$types';
	import { untrack } from 'svelte';
	import { validHostnames } from '$lib/validHostnames.json';

	let { data }: PageProps = $props();

	const hostnameList = Object.keys(validHostnames);

	type ValidationResponse = {
		valid: boolean;
		hostname: string;
		message: string;
	};

	const getURLsite = (puzzleURL: string) => {
		try {
			return new URL(puzzleURL).hostname;
		} catch {
			return '';
		}
	};

	const validateURL = (puzzleURL: string): ValidationResponse => {
		if (puzzleURL === '') {
			return {
				valid: false,
				hostname: '',
				message: 'Paste a puzzle URL to get started'
			};
		}

		try {
			new URL(puzzleURL);
			const hostname = getURLsite(puzzleURL);

			if (hostnameList.includes(hostname)) {
				return {
					valid: true,
					hostname,
					message: `Ready · ${validHostnames[hostname as keyof typeof validHostnames]}`
				};
			}

			return {
				valid: false,
				hostname,
				message: 'Site not supported yet — check Compatible sites'
			};
		} catch {
			return {
				valid: false,
				hostname: '',
				message: 'That doesn’t look like a valid URL'
			};
		}
	};

	let puzzleURL = $state('');
	// Seed once from layout load (Redis counter); refresh after each download
	let downloadCount = $state(untrack(() => Number(data.counter) || 0));
	let loading = $state(false);
	let errorMessage = $state('');

	let urlInfo = $derived(validateURL(puzzleURL));
	let urlSite = $derived(urlInfo.hostname);
	let urlValid = $derived(urlInfo.valid);
	let urlMessage = $derived(urlInfo.message);

	const downloadPuzzle = async () => {
		if (!urlValid || loading) return;

		loading = true;
		errorMessage = '';

		try {
			const response = await fetch('/getPuzzle', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ url: puzzleURL, urlSite })
			});

			if (!response.ok) {
				errorMessage = 'Download failed. Check the URL and try again.';
				return;
			}

			const clonedResponse = response.clone();
			const downloadData = await response.blob();
			const jsonInfo = await clonedResponse.json();
			const url = URL.createObjectURL(downloadData);
			const a = document.createElement('a');
			a.href = url;
			a.download = jsonInfo?.annotation ? `${jsonInfo.annotation}` : 'puzzle.ipuz';
			document.body.appendChild(a);
			a.click();
			URL.revokeObjectURL(url);
			a.remove();

			const counterResponse = await fetch('/counter');
			if (counterResponse.ok) {
				const counterData = await counterResponse.json();
				downloadCount = Number(counterData.counter) || downloadCount;
			}
		} catch {
			errorMessage = 'Something went wrong. Please try again.';
		} finally {
			loading = false;
		}
	};

	const onSubmit = (event: Event) => {
		event.preventDefault();
		downloadPuzzle();
	};
</script>

<section class="relative mx-auto w-full max-w-xl">
	<div
		class="empty-cell pointer-events-none absolute -right-6 top-8 hidden size-36 sm:block md:-right-10 md:size-44"
		aria-hidden="true"
	></div>

	<p class="brand rise text-[clamp(2.5rem,10vw,4.25rem)] font-extrabold leading-[0.95] text-ink">
		PuzzlePull
	</p>
	<p class="rise rise-delay-1 mt-4 max-w-md text-base text-ink-soft sm:text-lg">
		Paste a crossword URL. Get an <span class="text-ink">.ipuz</span> file back.
	</p>

	<p class="mono-meta rise rise-delay-1 mt-5 text-ink-soft">
		{downloadCount.toLocaleString()}
		{downloadCount === 1 ? 'puzzle' : 'puzzles'} downloaded
	</p>

	<form class="rise rise-delay-2 relative mt-8 space-y-4 sm:mt-10" onsubmit={onSubmit}>
		<label class="block">
			<span class="mb-2 block text-sm font-semibold text-ink">Puzzle URL</span>
			<input
				class="field {puzzleURL !== '' && !urlValid ? 'is-invalid' : ''}"
				type="url"
				name="puzzleURL"
				placeholder="https://www.theguardian.com/crosswords/…"
				autocomplete="off"
				spellcheck="false"
				bind:value={puzzleURL}
			/>
		</label>

		<div
			class="mono-meta min-h-[1.5rem] {urlValid
				? 'status-ok'
				: puzzleURL === ''
					? 'status-muted'
					: 'status-bad'}"
			role="status"
			aria-live="polite"
		>
			{urlMessage}
			{#if urlSite === 'observer.co.uk'}
				<span class="mt-1 block status-muted">
					Only Everyman and Speedy puzzles are supported.
				</span>
			{/if}
			{#if errorMessage}
				<span class="mt-1 block status-bad">{errorMessage}</span>
			{/if}
		</div>

		<div class="flex flex-col gap-3 pt-1 sm:flex-row sm:flex-wrap sm:items-center">
			<button
				class="btn-primary w-full sm:w-auto {loading ? 'is-loading' : ''}"
				type="submit"
				disabled={!urlValid || loading}
			>
				{#if loading}
					<span class="relative z-10 inline-flex items-center gap-2">
						<svg class="spin size-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
							<circle
								cx="12"
								cy="12"
								r="9"
								stroke="currentColor"
								stroke-opacity="0.25"
								stroke-width="3"
							/>
							<path
								d="M21 12a9 9 0 0 0-9-9"
								stroke="currentColor"
								stroke-width="3"
								stroke-linecap="round"
							/>
						</svg>
						Downloading…
					</span>
				{:else}
					Download .ipuz
				{/if}
			</button>
			<a class="link-quiet text-center text-sm text-ink-soft sm:text-left" href="/compatibility"
				>See compatible sites</a
			>
		</div>
	</form>
</section>
