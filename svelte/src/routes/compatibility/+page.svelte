<script lang="ts">
	import { validHostnames } from '$lib/validHostnames.json';

	const notes: Record<string, string> = {
		'observer.co.uk': 'Everyman & Speedy only'
	};

	const sites = Object.entries(validHostnames).filter(([host]) => host !== 'localhost');
</script>

<svelte:head>
	<title>Compatible sites · PuzzlePull</title>
</svelte:head>

<section class="relative mx-auto w-full max-w-xl">
	<div
		class="empty-cell pointer-events-none absolute -right-4 top-2 hidden size-24 opacity-70 sm:block"
		aria-hidden="true"
	></div>

	<p class="brand rise text-[clamp(2rem,8vw,3rem)] font-extrabold tracking-tight text-ink">
		Compatible sites
	</p>
	<p class="rise rise-delay-1 mt-4 max-w-md text-base text-ink-soft sm:text-lg">
		These hosts work today. Need another source? Open an issue on GitHub.
	</p>

	<ul class="rise rise-delay-2 mt-8 divide-y divide-line border-y border-line sm:mt-10">
		{#each sites as [hostname, label]}
			<li class="flex flex-col gap-1 py-4 sm:flex-row sm:items-baseline sm:justify-between sm:gap-6">
				<div class="min-w-0">
					<span class="font-semibold text-ink">{label}</span>
					{#if notes[hostname]}
						<span class="mt-1 block text-sm text-ink-soft">{notes[hostname]}</span>
					{/if}
				</div>
				<span class="mono-meta break-all text-ink-soft">{hostname}</span>
			</li>
		{/each}
	</ul>

	<div class="rise rise-delay-3 mt-8 flex flex-col gap-3 sm:flex-row sm:items-center">
		<a
			class="btn-primary w-full sm:w-auto"
			href="https://github.com/astrojarred/puzzlepull/issues"
			target="_blank"
			rel="noopener noreferrer"
		>
			Request a site
		</a>
		<a class="link-quiet text-center text-sm text-ink-soft sm:text-left" href="/help">Need help?</a>
	</div>
</section>
