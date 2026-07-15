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
			plus native Guardian/Observer fallbacks. NYT and other subscription-only sources are not included.
			If a site is missing, open an issue on GitHub.
		</Card.Description>
	</Card.Header>
	<Card.Content>
		<ul class="list-disc pl-5 space-y-1">
			{#each sites as site}
				<li>{site}</li>
			{/each}
		</ul>
		<p class="text-sm text-muted-foreground mt-4">
			Paste a puzzle page URL when possible. For some outlets (USA Today, WaPo, Daily Pop, etc.),
			the publisher homepage is enough and puzzlepull will fetch the latest puzzle.
			AmuseLabs-backed sites can fail when upstream scrapers break.
		</p>
	</Card.Content>
	<Card.Footer class="border-t px-6 py-4">
		<Button
			onclick={() => (window.location.href = 'https://github.com/astrojarred/puzzlepull/issues')}
			>Request</Button
		>
	</Card.Footer>
</Card.Root>
