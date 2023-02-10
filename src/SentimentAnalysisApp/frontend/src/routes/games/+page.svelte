<script lang="ts">
    import type {Game} from '../../lib/shared/types';
    // import GameCard from '$lib/components/GameCard.svelte';
    import {goto} from "$app/navigation";
    import List, {Item, PrimaryText, SecondaryText, Graphic, Meta, Text} from '@smui/list';
    import * as http from "http";
    import GameCard from '../../lib/components/GameCard.svelte';
    import Button from '@smui/button';
    export let data;
</script>

<section class="game-page">
    <div class="game-list">
        {#each data.games as game}
            <GameCard {game} />
        {/each}
        {#each data.games as game}
            <GameCard {game} />
        {/each}
        <Button padded>See More</Button>
    </div>

</section>

<style>
    .game-page {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }
    .game-list {
        width: 60vw;
        display: flex;
        flex-direction: column;
        margin-bottom: 48px;
    }
    * :global(.game-list>*){
        margin-bottom: 8px;
    }
    @media (max-width: 460px) {
        * :global(.game-list) {
            width: 100%;
        }
    }
</style>
