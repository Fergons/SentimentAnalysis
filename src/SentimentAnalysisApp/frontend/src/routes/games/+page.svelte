<script lang="ts">
    import {onMount, onDestroy} from "svelte";
    import {initialValue, makeGameStore} from "../../lib/stores/game";
    import GameCard from '../../lib/components/GameCard.svelte';
    import Button from '@smui/button';
    import {navigating} from "$app/stores";
    import type {PageServerData} from "./$types";
    import type {Game} from "../../lib/client";

    export let data: PageServerData;
    let games = data?.games; // initialValue();
    // let gameStore = makeGameStore("possible limit in the future");
    //
    // let unsubscribe;

    // <!--onMount(() => {-->
    // <!--    unsubscribe = gameStore.subscribe((value) => {-->
    // <!--        games = value;-->
    // <!--    });-->
    // <!--});-->
    //
    // <!--onDestroy(() => {-->
    // <!--    if (unsubscribe) {-->
    // <!--        unsubscribe();-->
    // <!--        unsubscribe = null;-->
    // <!--    }-->
    // // });

</script>

<section class="game-page">
    <div class="game-list">
        {#if $navigating}
            <div>Loading...</div>
        {:else}
            {#each [...games.entries()] as [id, game] }
                <GameCard {game}/>
            {/each}
            <Button padded>See More</Button>
        {/if}
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

    * :global(.game-list>*) {
        margin-bottom: 8px;
    }

    @media (max-width: 460px) {
        * :global(.game-list) {
            width: 100%;
        }
    }
</style>
