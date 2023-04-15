<script lang="ts">
    import GameCard from '../../lib/components/GameCard.svelte';
    import Button, {Label} from '@smui/button';
    import {navigating} from "$app/stores";
    import type {PageServerData, PageData} from "./$types";
    import {derived, writable} from "svelte/store";
    import type {GameListItem} from "../../lib/client";
    import {GamesService} from "../../lib/client";
    import Autocomplete from '@smui-extra/autocomplete';
    import type {GameListSort, GameListFilter} from "../../lib/stores/game";
    import IconButton, {Icon} from '@smui/icon-button';
    import CircularProgress from '@smui/circular-progress';
    import Fab from "@smui/fab";
    import Dialog, {Title, Content, Actions, InitialFocus} from '@smui/dialog';
    import List, {Item, Graphic, Text} from '@smui/list';
    import Radio from '@smui/radio';
    import chips, {Set} from '@smui/chips';
    import Textfield from "@smui/textfield";
    import Banner, {CloseReason} from '@smui/banner';

    export let data: PageData;


    let autocomplete: any;
    let dialog: any;

    const initialGameFilterValue = {
        name: null,
        minNumReviews: null,
        maxNumReviews: null,
        minScore: null,
        maxScore: null,
        minReleaseDate: null,
        maxReleaseDate: null,
        categories: null,
        developers: null,
    };

    const perPageLimit = 20;
    const gamePage = writable(0);
    const gameFilter = writable<GameListFilter>({...initialGameFilterValue})
    const gameSort = writable<GameListSort>({numReviews: 'desc'});
    const games = writable<GameListItem[]>();
    let prevSort: GameListSort = {};
    let loadingContent = false;
    let moreContent = false;
    let filterOpen = false;
    let open = false;
    let selection = 'Radishes';
    let selected = 'Nothing yet.';

    function closeHandler(e: CustomEvent<{ action: string }>) {
        if (e.detail.action === 'accept') {
            selected = selection;
        }
        selection = 'Radishes';
    }

    const gameDataStore = derived(
        [gamePage, gameFilter, gameSort],
        async ([$gamePage, $gameFilter, $gameSort], set) => {
            if ($gameSort !== prevSort) {
                gamePage.set(0);
                prevSort = $gameSort;
            }
            loadingContent = true;
            const fetchedData = await getGames($gamePage, $gameFilter, $gameSort);
            if (fetchedData) {
                moreContent = fetchedData.total > ($gamePage + 1) * perPageLimit;
                set({
                    games: fetchedData.games,
                    total: fetchedData.total,
                });
            }
            loadingContent = false;
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

    let searchName = '';
    let filterTemp = {...initialGameFilterValue};

    function filterReset() {
        gameFilter.set({...initialGameFilterValue})
        filterTemp = {...initialGameFilterValue};
    }
</script>


<section class="game-page">
    <div class="main-list">
        <div class="settings-bar">
            <div class="settings-bar-row">
                <div class="search-fab">
                    <Autocomplete this={autocomplete}
                                  search={searchNames}
                                  bind:value={searchName}
                                  on:select={e => {
                                      $gameFilter.name = searchName;
                                  }}
                                  showMenuWithNoInput={false}
                                  label="Search"
                    >
                        <Textfield label="Search" bind:value={searchName} variant="outlined"/>
                        <Text
                                slot="loading"
                                style="display: flex; width: 100%; justify-content: center; align-items: center;"
                        >
                            Searching...
                        </Text>

                    </Autocomplete>
                    <Fab
                            on:click={() => {$gameFilter.name = searchName}}
                            disabled={searchName === ''}
                            color="primary"
                            mini
                            style="margin-top: auto; margin-bottom: auto;"
                    >
                        <Icon class="material-icons">arrow_forward</Icon>
                    </Fab>
                </div>
                <div class="sorting-settings">
                    <Button on:click={()=> $gameSort = {score: cycleThrough($gameSort.score, ['asc', 'desc', undefined])}}
                            padded>
                        <Label>Sort by Score</Label>
                        {#if $gameSort.score === 'desc'}
                            <Icon class="material-icons">arrow_drop_down</Icon>
                        {:else if $gameSort.score === 'asc'}
                            <Icon class="material-icons">arrow_drop_up</Icon>
                        {:else}
                            <Icon class="material-icons">exit</Icon>
                        {/if}
                    </Button>

                    <Button on:click={()=> $gameSort = {releaseDate: cycleThrough($gameSort.releaseDate, ['asc', 'desc', null])}}
                            padded>
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
            <div class="settings-bar-row">
                <div class="filter-settings">
                    <div class="filter-field">
                        <Textfield
                                type="number"
                                bind:value={filterTemp.minScore}
                                label="Min Score"
                                suffix="/10.0"
                                input$pattern="\d+"
                                input$min="0.0"
                                input$max="10.0"
                                input$step="0.1"
                        />
                        <Textfield
                                type="number"
                                max="10.0"
                                bind:value={filterTemp.maxScore}
                                label="Max Score"
                                suffix="/10.0"
                                input$pattern="\d+"
                                input$min="0.0"
                                input$max="10.0"
                                input$step="0.1"
                        />
                    </div>
                    <div class="filter-field">
                        <Textfield
                                type="number"
                                bind:value={filterTemp.minNumReviews}
                                label="Min Reviews"
                        />
                        <Textfield
                                type="number"
                                bind:value={filterTemp.maxNumReviews}
                                label="Max Reviews"
                        />
                    </div>
                    <div class="filter-field">
                        <Textfield
                                type="datetime-local"
                                bind:value={filterTemp.minReleaseDate}
                                label="Min Release Date"

                        />
                        <Textfield
                                type="datetime-local"
                                bind:value={filterTemp.maxReleaseDate}
                                label="Max Release Date"
                        />
                    </div>
                    <Button on:click={() => filterReset()}>
                        <Label>Reset</Label>
                    </Button>
                    <Button on:click={() => gameFilter.set({...filterTemp})}>
                        <Label>Apply</Label>
                    </Button>
                </div>
            </div>
        </div>
        <div class="game-list">
            {#if $gameDataStore.games.length === 0 && loadingContent}
                <div class="loading-container">
                    <CircularProgress indeterminate/>
                </div>
            {/if}
            {#each $gameDataStore.games as game}
                <GameCard {game}/>
            {/each}
        </div>
        <div class="page-buttons-container">
            <Button on:click={()=> $gamePage = 0} disabled={$gamePage <= 0} padded>
                <Icon class="material-icons">keyboard_double_arrow_left</Icon>
            </Button>
            <Button on:click={()=> $gamePage = $gamePage - 1} disabled={$gamePage <= 0} padded>
                <Icon class="material-icons">keyboard_arrow_left</Icon>
            </Button>
            <div class="mdc-typography--button">
                Page {$gamePage ? $gamePage + 1 : 1}/{Math.ceil($gameDataStore.total / perPageLimit)}
            </div>
            <Button on:click={()=> $gamePage = $gamePage + 1} disabled={!moreContent} padded>
                <Icon class="material-icons">keyboard_arrow_right</Icon>
            </Button>
            <Button on:click={()=> $gamePage = Math.ceil($gameDataStore.total/ perPageLimit)-1}
                    disabled={$gamePage === Math.floor($gameDataStore.total / perPageLimit)} padded>
                <Icon class="material-icons">keyboard_double_arrow_right</Icon>
            </Button>
        </div>
    </div>
</section>

<style>
    .settings-bar {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 1rem;
        padding: 12px 1rem 12px 1rem;
        box-sizing: border-box;
        position: sticky;
        z-index: 3;
        top: 0;
    }

    .settings-bar-row {
        display: flex;
        flex-direction: row;
        justify-content: space-between;

    }

    .filter-settings {
        display: flex;
        flex-direction: row;
        width: 100%;
        gap: 1rem;
        align-items: center;
    }

    .page-buttons-container {
        display: flex;
        flex-direction: row;
        justify-content: center;
    }

    .game-page {
        display: flex;
        flex-direction: row;
    }

    .main-list {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        margin-left: 1rem;
    }

    .game-list {
        display: flex;
        flex-direction: column;
        margin-bottom: 1rem;
    }

    .game-list, .settings-bar, .page-buttons-container {
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

    .search-fab {
        display: flex;
        gap: 1rem;
        flex-direction: row;
        justify-content: center;
    }


</style>
