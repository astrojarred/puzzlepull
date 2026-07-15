<script lang="ts">
	import { validHostnames } from '$lib/validHostnames.json';

	const notes: Record<string, string> = {
		'observer.co.uk': 'Everyman & Speedy only'
	};

	const sites = Object.entries(validHostnames).filter(([host]) => host !== 'localhost');
</script>

<section class="mx-auto w-full max-w-xl">
	<p class="brand rise text-4xl font-semibold tracking-tight text-ink sm:text-5xl">Sites</p>
	<p class="rise rise-delay-1 mt-4 max-w-md text-lg text-ink-soft">
		These hosts work today. Need another? Open a GitHub issue.
	</p>

	<ul class="rise rise-delay-2 mt-10 divide-y divide-line/70 border-y border-line/70">
		{#each sites as [hostname, label]}
			<li class="flex flex-col gap-1 py-4 sm:flex-row sm:items-baseline sm:justify-between">
				<div>
					<span class="font-medium text-ink">{label}</span>
					{#if notes[hostname]}
						<span class="mt-1 block text-sm text-ink-soft">{notes[hostname]}</span>
					{/if}
				</div>
				<span class="font-mono text-sm text-ink-soft">{hostname}</span>
			</li>
		{/each}
	</ul>

	<div class="rise rise-delay-3 mt-8">
		<a
			class="btn-primary"
			href="https://github.com/astrojarred/puzzlepull/issues"
			target="_blank"
			rel="noopener noreferrer"
		>
			Request a site
		</a>
	</div>
</section>
