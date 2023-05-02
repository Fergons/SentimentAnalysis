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
    import List, {Item, Graphic, Text} from '@smui/list';
    import Radio from '@smui/radio';
    import chips, {Set} from '@smui/chips';
    import Textfield from "@smui/textfield";
    import Banner, {CloseReason} from '@smui/banner';
    import {
        gameFilter,
        gameSort,
        gameDataStore,
        gamePage,
        perPageLimit,
        initialGameFilterValue
    } from "../../lib/stores/game";
    import Accordion, {Panel, Header, Content} from "@smui-extra/accordion";

    export let data: PageData;


    let autocomplete: any;
    let dialog: any;

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


    const categories = data.categories;
    let loading = true;
    $: loading = $gameDataStore.loading;

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
        searchName = '';
        gameFilter.set({...initialGameFilterValue})
        filterTemp = {...initialGameFilterValue};
    }

    function applyFilter() {
        gameFilter.set({...filterTemp});
    }

    let filterSettingsOpen = true;

    function toggleFilterSettings() {
        filterSettingsOpen = !filterSettingsOpen;
    }

</script>


<section class="game-page">
    <div class="grid-container">
        <div class="filter-settings">
            <Accordion>
                <Panel bind:open={filterSettingsOpen}>
                    <Header ripple={false}>Filter</Header>
                    <Content>
                        <Button on:click={filterReset}
                                color="secondary">
                            <Label>Reset</Label>
                            <Icon class="material-icons">reset</Icon>
                        </Button>
                        <Button on:click={applyFilter}
                                color="secondary">
                            <Label>Apply</Label>
                            <Icon class="material-icons">apply</Icon>
                        </Button>
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
                    </Content>
                </Panel>
            </Accordion>
        </div>
        <div class="settings-bar">
            <div class="settings-bar-row">
                <div class="settings-bar-item">
                    <div class="search-fab">
                        <Autocomplete this={autocomplete}
                                      search={searchNames}
                                      bind:value={searchName}
                                      on:focusout={e => {
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
                </div>
                <div>
                    <Button on:click={()=> $gameSort = {score: cycleThrough($gameSort.score, ['asc', 'desc', undefined])}}
                            color="secondary">
                        <Label>Score</Label>
                        {#if $gameSort.score === 'desc'}
                            <Icon class="material-icons">arrow_drop_down</Icon>
                        {:else if $gameSort.score === 'asc'}
                            <Icon class="material-icons">arrow_drop_up</Icon>
                        {:else}
                            <Icon class="material-icons">remove</Icon>
                        {/if}
                    </Button>

                    <Button on:click={()=> $gameSort = {releaseDate: cycleThrough($gameSort.releaseDate, ['asc', 'desc', null])}}
                            color="secondary">
                        <Label>Release</Label>
                        {#if $gameSort.releaseDate === 'desc'}
                            <Icon class="material-icons">arrow_drop_down</Icon>
                        {:else if $gameSort.releaseDate === 'asc'}
                            <Icon class="material-icons">arrow_drop_up</Icon>
                        {:else}
                            <Icon class="material-icons">remove</Icon>
                        {/if}
                    </Button>
                    <Button
                            on:click={()=> $gameSort = {numReviews: cycleThrough($gameSort.numReviews, ['asc', 'desc', undefined])}}
                            color="secondary">
                        <Label>Reviews</Label>
                        {#if $gameSort.numReviews === 'desc'}
                            <Icon class="material-icons">arrow_drop_down</Icon>
                        {:else if $gameSort.numReviews === 'asc'}
                            <Icon class="material-icons">arrow_drop_up</Icon>
                        {:else}
                            <Icon class="material-icons">remove</Icon>
                        {/if}
                    </Button>
                </div>
            </div>
            <div class="settings-bar-row">
                <div class="filter-toggle-container">
                    <Button style="flex-grow:1" on:click={toggleFilterSettings} color="secondary" variant="unelevated">
                        <Icon class="material-icons">filter_list</Icon>
                    </Button>
                </div>
            </div>
        </div>

        <div class="game-list">
            {#if $gameDataStore.games.length === 0}
                <div class="loading-container">
                    <CircularProgress indeterminate/>
                </div>
            {/if}
            {#each $gameDataStore.games as game}
                <GameCard {game}/>
            {/each}
        </div>
        {#if $gameDataStore.moreContent}
            <div class="page-buttons-container" style="display:none">
                <Button on:click={()=> $gamePage = 0} disabled={$gamePage <= 0} padded>
                    <Icon class="material-icons">keyboard_double_arrow_left</Icon>
                </Button>
                <Button on:click={()=> $gamePage = $gamePage - 1} disabled={$gamePage <= 0} padded>
                    <Icon class="material-icons">keyboard_arrow_left</Icon>
                </Button>
                <div class="mdc-typography--button">
                    Page {$gamePage ? $gamePage + 1 : 1}/{Math.ceil($gameDataStore.total / perPageLimit)}
                </div>
                <Button on:click={()=> $gamePage = $gamePage + 1} disabled={!$gameDataStore.moreContent} padded>
                    <Icon class="material-icons">keyboard_arrow_right</Icon>
                </Button>
                <Button on:click={()=> $gamePage = Math.ceil($gameDataStore.total/ perPageLimit)-1}
                        disabled={$gamePage === Math.floor($gameDataStore.total / perPageLimit)} padded>
                    <Icon class="material-icons">keyboard_double_arrow_right</Icon>
                </Button>
            </div>
        {/if}
    </div>
</section>

<style>
    .filter-toggle-container {
        grid-area: toggle-filter;
        display: none;
        width: 100%;
    }

    .settings-bar {
        grid-area: settings-bar;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 0.6rem;
        padding: 12px 1rem 12px 1rem;
        box-sizing: border-box;
        position: sticky;
        z-index: 3;
        top: 0;
    }

    .settings-bar-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .filter-settings {
        grid-area: filter-settings;
        padding-right: 0.8rem;
        position: sticky;
        align-self: start;
        top: 104px;
        z-index: 3;
    }


    .game-list {
        grid-area: game-list;
        display: flex;
        min-height: 800px;
        flex-direction: column;
        box-sizing: border-box;
    }

    .page-buttons-container {
        grid-area: page-buttons-container;
        display: flex;
        flex-direction: row;
        justify-content: center;
        margin-bottom: 1rem;
    }

    .game-page {
        display: flex;
        flex-direction: row;
        width: 100%;
    }

    .grid-container {
        display: grid;
        grid-template-columns: 1fr 3fr;
        grid-template-rows: auto auto auto;
        grid-template-areas:
              "settings-bar settings-bar"
              "filter-settings game-list"
              ". page-buttons-container";
    }

    .game-list, .page-buttons-container {
        max-width: 960px;
    }

    * :global(.game-list>*) {
        margin-bottom: 8px;
    }

    @media (max-width: 960px) {
        .filter-settings {
            top: 132px;
        }
    }

    @media (max-width: 900px) {
        .settings-bar {
            margin-bottom: 0;
        }

        .filter-toggle-container {
            display: flex;
        }

        * :global(.grid-container) {
            grid-template-columns: 1fr;
            grid-template-areas:
              "settings-bar"
              "filter-settings"
              "game-list"
              "page-buttons-container";
        }

        * :global(.filter-settings) {
            position: sticky;
            padding-right: 0;
            padding-bottom: 1rem;
            top: 132px;
        }

        * :global(.smui-accordion__header__title) {
            display: none;
        }
        .game-page{
            margin: 0;
        }
    }

    .search-fab {
        display: flex;
        gap: 1rem;
        flex-direction: row;
        justify-content: center;
    }

    .filter-field {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        justify-content: center;
    }


</style>
