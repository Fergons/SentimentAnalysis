<!-- Created by Frantisek Sabol
    @component GameCard
-->
<script lang="ts">
    import Card, {
        Media,
        MediaContent,
        PrimaryAction,
    } from '@smui/card';
    import {goto} from '$app/navigation';
    import type {GameListItem} from '../client';
    import {selectedGame} from "../stores/game";

    export let game: GameListItem;
    let options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };

    function selectGame() {
        goto('/games/' + game.id)
        $selectedGame = game;
    }

</script>


<div class="card-container">
    <Card>
        <PrimaryAction on:click={() => selectGame()}>
            <Media class="card-media-219x102"
                   aspectRatio="219x102"
            >
                <img src={game.image_url} loading="lazy" width="460" height="215" alt={game.name}>

                <MediaContent class="mdc-typography--body2 card-media-content">
                    <h2 class="mdc-typography--headline6" style="margin: 0; text-transform: uppercase">
                        {game.name}
                    </h2>
                    <h3 class="mdc-typography--subtitle2" style="margin: 0 0 10px; color: #888;">
                        {new Intl.DateTimeFormat("default", options).format(new Date(game.release_date))}
                    </h3>
                </MediaContent>
                <MediaContent class="card-media-content">
                    <h2 class="mdc-typography--headline6" style="margin: 0; text-transform: uppercase">
                        {game.score}/10.0
                    </h2>
                    <h2 class="mdc-typography--subtitle2" style="margin: 0 0 10px; color: #888;">
                        {#if game.num_reviews === 1}
                            1 review
                        {:else}
                            {game.num_reviews} reviews
                        {/if}
                    </h2>
                </MediaContent>
            </Media>
        </PrimaryAction>
    </Card>
</div>

<style>
    .mdc-typography--headline6{
            line-height: 1.3rem;
    }

    * :global(.card-media-219x102) {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        margin: 16px;
    }

    * :global(.card-media-219x102>img) {
        width: 219px;
        height: 102px;
        margin-left: auto;
        border-radius: 6px;
        margin-right: 8px;
        background-image: radial-gradient(circle, rgba(255, 255, 255, 0), rgba(0, 0, 0, 0.7));
        line-height: 102px;
        text-align: center;
        font-family: 'Roboto', monospace;
        font-size: 24px;
        font-weight: bold;
        text-transform: uppercase;
    }

    * :global(.card-media-content) {
        position: relative;
    }

    * :global(.card-media-219x102 :last-child) {
        margin-left: auto;
    }

    * :global(.card-media-219x102 :first-child) {
        margin-left: 0;
    }

    @media (max-width: 680px) {
        .card-container{
            width: 100%
        }

        * :global(.card-media-219x102>img) {
            width: 110px;
            height: 51px;
        }
        .mdc-typography--headline6{
            font-size: 1rem;
            line-height: 1rem;
        }
        .mdc-typography--subtitle2{
            font-size: 0.8rem;
            line-height: 0.8rem;
        }

    }


    @media (max-width: 420px) {
        .mdc-typography--headline6{
            font-size: 0.8rem;
        }
    }

</style>
