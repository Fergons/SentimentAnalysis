<script lang="ts">
	import type { Game } from '../../lib/server/api/types';
	// import GameCard from '$lib/components/GameCard.svelte';
	import {goto} from "$app/navigation";
	import List, { Item, PrimaryText, SecondaryText, Graphic, Meta, Text} from '@smui/list';

	export let data;
</script>

<section>
	<List
	threeline
	avatarList
	class="game-list"
	>
		{#each data.games as game}
			<Item

				on:SMUI:action={() => {goto("/games/" + game.id)}} >
				<Graphic
						rect
						style="background-image: url({game.image_url})"
				>
				</Graphic>
				<Text>
					<PrimaryText>{game.name}</PrimaryText>
					{#if game.release_date}
						<SecondaryText>{game.release_date}</SecondaryText>
					{/if}
				</Text>
				<Meta class="material-icons">score</Meta>
			</Item>

		{/each}
	</List>
</section>

<style>
	.game-list {
		width: 30vw;
	}
</style>
