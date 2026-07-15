<script lang="ts">
	import '../app.css';
	import { page } from '$app/state';

	let { children } = $props();
</script>

<svelte:head>
	<title>PuzzlePull</title>
</svelte:head>

<div class="relative min-h-screen overflow-hidden">
	<div class="pointer-events-none absolute inset-0 grid-atmosphere" aria-hidden="true"></div>

	<div class="relative mx-auto flex min-h-screen max-w-3xl flex-col px-5 sm:px-8">
		<header class="flex items-center justify-between gap-4 py-5 rise">
			<a href="/" class="brand text-xl font-semibold text-ink sm:text-2xl">PuzzlePull</a>
			<nav class="flex items-center gap-1">
				<a href="/" class="btn-ghost" aria-current={page.route.id === '/' ? 'page' : undefined}
					>Download</a
				>
				<a
					href="/compatibility"
					class="btn-ghost"
					aria-current={page.route.id === '/compatibility' ? 'page' : undefined}>Sites</a
				>
				<a
					href="https://github.com/astrojarred/puzzlepull"
					class="btn-ghost"
					target="_blank"
					rel="noopener noreferrer">GitHub</a
				>
			</nav>
		</header>

		<main class="flex flex-1 flex-col justify-center pb-16 pt-6 sm:pt-10">
			{@render children()}
		</main>

		<footer class="pb-6 text-center text-sm text-ink-soft rise rise-delay-3">
			Converts web crosswords to
			<a class="underline decoration-line underline-offset-2 hover:text-ink" href="http://www.ipuz.org/"
				>.ipuz</a
			>
			for solvers like
			<a class="underline decoration-line underline-offset-2 hover:text-ink" href="http://squares.io/"
				>squares.io</a
			>
		</footer>
	</div>
</div>
