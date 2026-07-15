<script lang="ts">
	const github = 'https://github.com/astrojarred/puzzlepull';
	const issues = `${github}/issues`;
</script>

<svelte:head>
	<title>Help · PuzzlePull</title>
</svelte:head>

<section class="relative mx-auto w-full max-w-xl">
	<div
		class="empty-cell pointer-events-none absolute -right-4 top-2 hidden size-24 opacity-70 sm:block"
		aria-hidden="true"
	></div>

	<p class="brand rise text-[clamp(2rem,8vw,3rem)] font-extrabold tracking-tight text-ink">
		Help & contact
	</p>
	<p class="rise rise-delay-1 mt-4 max-w-md text-base text-ink-soft sm:text-lg">
		PuzzlePull turns supported crossword pages into <span class="text-ink">.ipuz</span> files you
		can open in solvers like
		<a class="link-quiet text-ink" href="http://squares.io/">squares.io</a>.
	</p>

	<div class="rise rise-delay-2 mt-8 space-y-8 sm:mt-10">
		<section>
			<h2 class="text-lg font-semibold text-ink">How to use it</h2>
			<ol class="mt-3 list-decimal space-y-2 pl-5 text-ink-soft">
				<li>Open a puzzle on a <a class="link-quiet text-ink" href="/compatibility">compatible site</a>.</li>
				<li>Copy the puzzle page URL.</li>
				<li>Paste it on the <a class="link-quiet text-ink" href="/">download page</a> and hit Download.</li>
			</ol>
		</section>

		<section>
			<h2 class="text-lg font-semibold text-ink">Something broken?</h2>
			<p class="mt-3 text-ink-soft">
				If a download fails, the site isn’t listed, or a formerly working puzzle stops converting,
				please open a GitHub issue. Include the puzzle URL when you can.
			</p>
		</section>

		<section>
			<h2 class="text-lg font-semibold text-ink">Contact</h2>
			<ul class="mt-3 space-y-2 text-ink-soft">
				<li>
					Bugs & feature requests:
					<a class="link-quiet text-ink" href={issues} target="_blank" rel="noopener noreferrer"
						>GitHub issues</a
					>
				</li>
				<li>
					Source & docs:
					<a class="link-quiet text-ink" href={github} target="_blank" rel="noopener noreferrer"
						>github.com/astrojarred/puzzlepull</a
					>
				</li>
			</ul>
		</section>
	</div>

	<div class="rise rise-delay-3 mt-8 flex flex-col gap-3 sm:flex-row">
		<a class="btn-primary w-full sm:w-auto" href={issues} target="_blank" rel="noopener noreferrer">
			Open an issue
		</a>
		<a
			class="btn-ghost w-full justify-center border border-line bg-white sm:w-auto"
			href={github}
			target="_blank"
			rel="noopener noreferrer"
		>
			View on GitHub
		</a>
	</div>
</section>
