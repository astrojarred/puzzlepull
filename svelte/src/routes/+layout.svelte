<script lang="ts">
	import '../app.css';

	import { goto } from '$app/navigation';
	import { page } from '$app/state';

	import HardDriveDownload from 'lucide-svelte/icons/hard-drive-download';
	import Share from 'lucide-svelte/icons/share';
	import Puzzle from 'lucide-svelte/icons/puzzle';
	import Cog from 'lucide-svelte/icons/cog';

	import { Button } from '$lib/components/ui/button/index.js';
	import * as Tooltip from '$lib/components/ui/tooltip/index.js';
	import { GithubIcon } from 'lucide-svelte';

</script>

<svelte:head>
	<title>PuzzlePull</title>
</svelte:head>

<div class="grid h-screen w-full pl-[53px]">
	<aside class="inset-y fixed left-0 z-20 flex h-full flex-col border-r">
		<div class="border-b p-2">
			<Button variant="outline" size="icon" aria-label="Home" on:click={() => goto('/')}>
				<Puzzle class="size-5" strokeWidth={3} />
			</Button>
		</div>
		<nav class="grid gap-1 p-2">
			<Tooltip.Root>
				<Tooltip.Trigger asChild let:builder>
					<Button
						variant="ghost"
						size="icon"
						class={page.route.id === '/' ? 'bg-muted rounded-lg' : 'rounded-lg'}
						aria-label="PuzzlePull"
						builders={[builder]}
						on:click={() => goto('/')}
					>
						<HardDriveDownload class="size-5" />
					</Button>
				</Tooltip.Trigger>
				<Tooltip.Content side="right" sideOffset={5}>Download a Puzzle</Tooltip.Content>
			</Tooltip.Root>
		</nav>
		<nav class="grid gap-1 p-2">
			<Tooltip.Root>
				<Tooltip.Trigger asChild let:builder>
					<Button
						variant="ghost"
						size="icon"
						class={page.route.id === '/compatibility' ? 'bg-muted rounded-lg' : 'rounded-lg'}
						aria-label="Compatibility"
						builders={[builder]}
						on:click={() => goto('/compatibility')}
					>
						<Cog class="size-5" />
					</Button>
				</Tooltip.Trigger>
				<Tooltip.Content side="right" sideOffset={5}>Website Compatibility</Tooltip.Content>
			</Tooltip.Root>
		</nav>
		<nav class="mt-auto grid gap-1 p-2">
			<Tooltip.Root>
				<Tooltip.Trigger asChild let:builder>
					<Button
						variant="ghost"
						size="icon"
						class="mt-auto rounded-lg"
						aria-label="Account"
						builders={[builder]}
						on:click={() => {
							window.location = 'https://github.com/astrojarred/puzzlepull';
						}}
					>
						<GithubIcon class="size-5" />
					</Button>
				</Tooltip.Trigger>
				<Tooltip.Content side="right" sideOffset={5}>GitHub</Tooltip.Content>
			</Tooltip.Root>
		</nav>
	</aside>
	<div class="flex flex-col">
		<header class="bg-background sticky top-0 z-10 flex h-[57px] items-center gap-1 border-b px-4">
			<h1 class="text-xl font-semibold">PuzzlePull</h1>
			<Button variant="outline" size="sm" class="ml-auto gap-1.5 text-sm">
				<Share class="size-3.5" />
				Share
			</Button>
		</header>
		<main class="grid flex-1 gap-4 overflow-auto p-4">
			<slot></slot>
		</main>
	</div>
</div>
