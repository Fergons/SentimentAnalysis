<script lang="ts">
    import GameCard from '../../lib/components/GameCard.svelte';
    import Button, {Label} from '@smui/button';
    import {navigating} from "$app/stores";
    import type {PageServerData, PageData} from "./$types";
    import {derived, writable} from "svelte/store";
    import type {GameListItem} from "../../lib/client";
    import {GamesService} from "../../lib/client";
    import Autocomplete from '@smui-extra/autocomplete';
    import {Text} from '@smui/list';
    import type {GameListSort, GameListFilter} from "../../lib/stores/game";
    import IconButton, {Icon} from '@smui/icon-button';

    export let data: PageData;

    let autocomplete: any;


    const perPageLimit = 20;
    const gamePage = writable(0);
    const gameFilter = writable<GameListFilter>({});
    const gameSort = writable<GameListSort>({numReviews: 'desc'});
    const games = writable<GameListItem[]>();
    let prevSort: GameListSort = {};
    let moreContent = false;
    const gameDataStore = derived(
        [gamePage, gameFilter, gameSort],
        async ([$gamePage, $gameFilter, $gameSort], set) => {
            if ($gameSort !== prevSort) {
                gamePage.set(0);
                prevSort = $gameSort;
            }
            const fetchedData = await getGames($gamePage, $gameFilter, $gameSort);
            if (fetchedData) {
                moreContent = fetchedData.total > ($gamePage + 1) * perPageLimit;
                set({
                    games: fetchedData.games,
                    total: fetchedData.total,
                });
            }
        },
        {games: [], total: 0}
    );


    const categories = data.categories;

    async function getGames(page: number, filter: GameListFilter, sort: GameListSort) {
        try {
            const offset = page * perPageLimit;
            if (filter.name === '') {
                filter.name = undefined;
            }
            const response = await GamesService.readGamesGamesGet(perPageLimit, offset,
                sort.numReviews, sort.score, sort.releaseDate,
                filter.name,
                filter.minNumReviews, filter.maxNumReviews, filter.minScore, filter.maxScore,
                filter.minReleaseDate, filter.maxReleaseDate,
                filter.categories ? filter.categories.join() : undefined,
                filter.developers ? filter.developers.join() : undefined);
            return {games: response.games, total: response.query_summary?.total || 0};
        } catch (e) {
            console.log(e);
            return {games: [], total: 0};
        }
    }

    let searchRequestCounter = 0;

    async function searchNames(input: string) {
        if (!input || input === '') {
            return [];
        }
        const counter = ++searchRequestCounter;
        await new Promise(resolve => setTimeout(resolve, 500));
        // This means the function was called again, so we should cancel.
        if (counter !== searchRequestCounter) {
            // `return false` (or, more accurately, resolving the Promise object to
            // `false`) is how you tell Autocomplete to cancel this search. It won't
            // replace the results of any subsequent search that has already finished.
            return false;
        }
        // Return a list of matsches.
        return GamesService.getNameMatchesGamesSearchGet(input);
    }

    function cycleThrough(value: string, options: string[]) {
        const index = options.indexOf(value);
        if (index === -1) {
            return options[0];
        }
        return options[(index + 1) % options.length];
    }
</script>

<section class="game-page">

    <div class="settings-bar">
        <Autocomplete this={autocomplete}
                      search={searchNames}
                      bind:value={$gameFilter.name}
                      showMenuWithNoInput={false}
                      label="Search"
        >
            <Text
                    slot="loading"
                    style="display: flex; width: 100%; justify-content: center; align-items: center;"
            >

            </Text>
        </Autocomplete>
        <div>

            <Button on:click={()=> $gameSort = {score: cycleThrough($gameSort.score, ['asc', 'desc', undefined])}} padded>
                <Label>Sort by Score</Label>
                {#if $gameSort.score === 'desc'}
                    <Icon class="material-icons">arrow_drop_down</Icon>
                {:else if $gameSort.score === 'asc'}
                    <Icon class="material-icons">arrow_drop_up</Icon>
                {:else}
                   <Icon class="material-icons">exit</Icon>
                {/if}
            </Button>

            <Button on:click={()=> $gameSort = {releaseDate: cycleThrough($gameSort.releaseDate, ['asc', 'desc', null])}} padded>
                <Label>Sort by Release</Label>
                {#if $gameSort.releaseDate === 'desc'}
                    <Icon class="material-icons">arrow_drop_down</Icon>
                {:else if $gameSort.releaseDate === 'asc'}
                    <Icon class="material-icons">arrow_drop_up</Icon>
                {:else}
                    <Icon class="material-icons">exit</Icon>
                {/if}
            </Button>
            <Button
                    on:click={()=> $gameSort = {numReviews: cycleThrough($gameSort.numReviews, ['asc', 'desc', undefined])}}
                    padded
            >
                <Label>Sort by Reviews</Label>
                {#if $gameSort.numReviews === 'desc'}
                    <Icon class="material-icons">arrow_drop_down</Icon>
                {:else if $gameSort.numReviews === 'asc'}
                    <Icon class="material-icons">arrow_drop_up</Icon>
                {:else}
                    <Icon class="material-icons">exit</Icon>
                {/if}
            </Button>
        </div>
    </div>
    <div class="game-list">

        {#each $gameDataStore.games as game}
            <GameCard {game}/>
        {/each}
    </div>
    <div class="page-buttons-container settings-bar">
        <Button on:click={()=> $gamePage = $gamePage - 1} disabled={$gamePage <= 0} padded>Previous Page</Button>
        {#each Array.from({length: Math.ceil($gameDataStore.total / perPageLimit)}, (x, i) => i) as page}
            <Button on:click={()=> $gamePage = page} disabled={$gamePage === page} padded>{page + 1}</Button>
        {/each}
        <Button on:click={()=> $gamePage = $gamePage + 1} disabled={!moreContent} padded>Next Page</Button>
    </div>


</section>

<style>
    .settings-bar {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding: 12px 1rem 12px 1rem;
        box-sizing: border-box;
        position: sticky;
        top: 0;
        z-index: 10;
    }

    .game-page {
        display: flex;
        flex-direction: column;

    }

    .game-list {
        display: flex;
        flex-direction: column;
        margin-bottom: 1rem;
    }

    .game-list, .settings-bar {
        max-width: 960px;
    }


    * :global(.game-list>*) {
        margin-bottom: 8px;
    }


    @media (max-width: 1200px) {
        * :global(.game-list) {
            width: 100%;
        }
    }

</style>
