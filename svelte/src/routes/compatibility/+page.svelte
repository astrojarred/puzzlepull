<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';

	import { validHostnames } from '$lib/validHostnames.json';

	const sites = [...new Set(Object.values(validHostnames).filter((name) => name !== 'localhost'))].sort();
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Compatibility List</Card.Title>
		<Card.Description>
			Supported via <a class="underline" href="https://github.com/thisisparker/xword-dl">xword-dl</a>
			plus native Guardian/Observer fallbacks. If a site is missing, open an issue on GitHub.
		</Card.Description>
	</Card.Header>
	<Card.Content>
		<ul class="list-disc pl-5 space-y-1">
			{#each sites as site}
				<li>{site}</li>
			{/each}
		</ul>
		<p class="text-sm text-muted-foreground mt-4">
			Some AmuseLabs-backed outlets may fail when upstream scrapers break. NYT and other
			subscription-only puzzles are intentionally not supported.
		</p>
	</Card.Content>
	<Card.Footer class="border-t px-6 py-4">
		<Button
			onclick={() => (window.location.href = 'https://github.com/astrojarred/puzzlepull/issues')}
			>Request</Button
		>
	</Card.Footer>
</Card.Root>
