<script lang="ts">
	import '../app.css';
	import { page } from '$app/state';

	let { children } = $props();

	let menuOpen = $state(false);

	type NavLink = {
		href: string;
		label: string;
		match?: string;
		external?: boolean;
	};

	const links: NavLink[] = [
		{ href: '/', label: 'Download', match: '/' },
		{ href: '/compatibility', label: 'Sites', match: '/compatibility' },
		{ href: '/help', label: 'Help', match: '/help' },
		{
			href: 'https://github.com/astrojarred/puzzlepull',
			label: 'GitHub',
			external: true
		}
	];

	const isCurrent = (match?: string) => (match ? page.route.id === match : false);

	const closeMenu = () => {
		menuOpen = false;
	};
</script>

<svelte:head>
	<title>PuzzlePull</title>
</svelte:head>

<div class="relative min-h-screen min-h-[100dvh] overflow-x-hidden">
	<div class="relative mx-auto flex min-h-screen min-h-[100dvh] max-w-3xl flex-col px-4 sm:px-6 md:px-8">
		<header class="rise flex items-center justify-between gap-3 py-4 sm:py-5">
			<a href="/" class="brand text-xl font-extrabold text-ink sm:text-2xl" onclick={closeMenu}
				>PuzzlePull</a
			>

			<nav class="hidden items-center gap-0.5 sm:flex" aria-label="Primary">
				{#each links as link}
					{#if link.external}
						<a
							href={link.href}
							class="btn-ghost"
							target="_blank"
							rel="noopener noreferrer">{link.label}</a
						>
					{:else}
						<a
							href={link.href}
							class="btn-ghost"
							aria-current={isCurrent(link.match) ? 'page' : undefined}>{link.label}</a
						>
					{/if}
				{/each}
			</nav>

			<button
				type="button"
				class="btn-ghost sm:hidden"
				aria-expanded={menuOpen}
				aria-controls="mobile-nav"
				onclick={() => (menuOpen = !menuOpen)}
			>
				{menuOpen ? 'Close' : 'Menu'}
			</button>
		</header>

		{#if menuOpen}
			<nav
				id="mobile-nav"
				class="mb-2 flex flex-col gap-1 rounded-md border border-line bg-white p-2 sm:hidden"
				aria-label="Mobile"
			>
				{#each links as link}
					{#if link.external}
						<a
							href={link.href}
							class="btn-ghost justify-start"
							target="_blank"
							rel="noopener noreferrer"
							onclick={closeMenu}>{link.label}</a
						>
					{:else}
						<a
							href={link.href}
							class="btn-ghost justify-start"
							aria-current={isCurrent(link.match) ? 'page' : undefined}
							onclick={closeMenu}>{link.label}</a
						>
					{/if}
				{/each}
			</nav>
		{/if}

		<main class="flex flex-1 flex-col justify-center pb-12 pt-4 sm:pb-16 sm:pt-8">
			{@render children()}
		</main>

		<footer
			class="rise rise-delay-3 flex flex-col gap-3 border-t border-line/80 py-5 text-sm text-ink-soft sm:flex-row sm:items-center sm:justify-between"
		>
			<p>
				Web crosswords →
				<a class="link-quiet" href="http://www.ipuz.org/">.ipuz</a>
				for
				<a class="link-quiet" href="http://squares.io/">squares.io</a>
			</p>
			<div class="flex flex-wrap gap-x-4 gap-y-2">
				<a class="link-quiet" href="/compatibility">Compatible sites</a>
				<a class="link-quiet" href="/help">Help</a>
				<a
					class="link-quiet"
					href="https://github.com/astrojarred/puzzlepull"
					target="_blank"
					rel="noopener noreferrer">GitHub</a
				>
			</div>
		</footer>
	</div>
</div>
