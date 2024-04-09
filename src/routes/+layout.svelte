<script lang="ts">
	import { AppBar, AppLayout, Card, Button, NavItem, Tooltip, settings } from 'svelte-ux';

	import { page } from '$app/stores';
	import '../app.postcss';

	settings({
		components: {
			AppBar: {
				classes: 'bg-primary text-white shadow-md'
			},
			AppLayout: {
				classes: {
					nav: 'bg-neutral-800'
				}
			},
			NavItem: {
				classes: {
					root: 'text-sm text-gray-400 pl-6 py-2 hover:text-white hover:bg-gray-300/10 [&:where(.is-active)]:text-sky-400 [&:where(.is-active)]:bg-gray-500/10'
				}
			}
		}
	});
	let nav_items = [
		// { path: '/joe-bot-2024', text: 'Joe Bot 2024' },
		{ path: '/markov-bot-2024', text: 'Markov Bot 2024' },
		{ path: '/markov-bot-2023', text: 'Markov Bot 2023' },
		{ path: '/markov-bot-2022', text: 'Markov Bot 2022' }
	];
</script>

<AppLayout>
	<nav slot="nav" class="nav h-full">
		{#each nav_items as item}
			<NavItem path={item.path} text={item.text} currentUrl={$page.url} />
		{/each}
	</nav>

	<AppBar title="Markov Bot Archive"></AppBar>

	<slot />
</AppLayout>
