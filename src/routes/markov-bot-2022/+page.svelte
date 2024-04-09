<script>
	import { Field, Input, Lazy } from 'svelte-ux';
	import { onMount } from 'svelte';
	import { base } from '$app/paths';

	// sample item
	// {
	//     "avatar_url": "https://cdn.discordapp.com/avatars/959116994614022145/5360e8d21595c9841cdfe2a6a0fa9294.png?size=1024",
	//     "content_html": "<div class=\"chatlog__message-group\">\n<div class=\"chatlog__author-avatar-container\">\n<img alt=\"Avatar\" class=\"chatlog__author-avatar\" loading=\"lazy\" src=\"https://cdn.discordapp.com/avatars/959116994614022145/5360e8d21595c9841cdfe2a6a0fa9294.png?size=128\"/>\n</div>\n<div class=\"chatlog__messages\">\n<span class=\"chatlog__author-name\" data-user-id=\"959116994614022145\" style=\"\" title=\"ProleArch#0000\">ProleArch</span>\n<span class=\"chatlog__bot-tag\">BOT</span>\n<span class=\"chatlog__timestamp\">31-Mar-22 07:00 PM</span>\n<div class=\"chatlog__message\" data-message-id=\"959225613426753566\" id=\"message-959225613426753566\" title=\"Message sent: 31-Mar-22 07:00 PM\">\n<div class=\"chatlog__content\">\n<div class=\"markdown\">\n<span class=\"preserve-whitespace\"><span class=\"pre pre--inline\">▌║▌║█  KING HAS FEWER CONNOTATIONS BECAUSE IT WOULD BE </span></span>\n</div>\n</div>\n</div>\n</div>\n</div>",
	//     "message_content": "`▌║▌║█  KING HAS FEWER CONNOTATIONS BECAUSE IT WOULD BE `",
	//     "message_id": 959225613426753566,
	//     "reaction_count": 0,
	//     "user_name": "ProleArch"
	// },

	/**
	 * @type {any[]}
	 */
	let data = [];
	onMount(async () => {
		const res = await fetch(`${base}/2022/markov_2022.json`);
		data = await res.json();
	});

	let filter_user = '';
	let filter_message = '';

	let order_bys = [
		{ label: 'Reaction Count', value: ['reaction_count', -1] },
		{ label: 'Message Date', value: ['message_id', 1] }
	];

	let order_by = order_bys[0].value;

	$: filtered_data = data.filter((item) => {
		if (filter_user && !item.user_name.toLowerCase().includes(filter_user.toLowerCase())) {
			return false;
		}

		if (
			filter_message &&
			!item.message_content.toLowerCase().includes(filter_message.toLowerCase())
		) {
			return false;
		}

		return true;
	});

	// @ts-ignore
	$: final_data = filtered_data.sort((a, b) => {
		const [key, order] = order_by;
		return a[key] > b[key] ? order : -order;
	});
</script>

<div class="ml-2">
	<h1 class="text-2xl font-semibold mb-2">Markov Bot 2024</h1>
	<div class="grid grid-cols-6 md:grid-cols-12">
		<Field label="Order by" let:id class="col-start-1 col-end-2">
			<select
				bind:value={order_by}
				class="text-sm w-full outline-none appearance-none cursor-pointer bg-surface-100"
			>
				{#each order_bys as option}
					<option value={option.value}>{option.label}</option>
				{/each}
			</select>
		</Field>

		<Field label="User filter" class="col-start-2 col-end-4">
			<Input placeholder="Type something to filter by user" bind:value={filter_user} />
		</Field>
		<Field label="Message filter" class="col-start-4 col-end-6">
			<Input placeholder="Type something to filter by message" bind:value={filter_message} />
		</Field>
	</div>

	<div class="h-[700px] p-1 overflow-auto discordwrapper mt-2">
		{#each final_data as item}
			<Lazy height="100px" class="group" unmount>
				{@html item.content_html}
			</Lazy>
		{/each}
	</div>
</div>
