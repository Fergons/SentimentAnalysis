<script lang="ts">
    import ReviewCard from '../../../../lib/components/ReviewCard.svelte';
    import {writable, derived} from "svelte/store";
    import type {ReviewWithAspects} from "../../../../lib/client";
    import {ReviewsService} from "../../../../lib/client";
    import Button, {Icon, Label} from "@smui/button";
    import Fab from "@smui/fab";
    import type {PageData} from "./$types";
    import {goto} from '$app/navigation';
    import {browser} from '$app/environment';
    import {page} from '$app/stores';
    import Textfield, {Input} from '@smui/textfield';
    import HelperText from '@smui/textfield/helper-text';
    import Select, {Option} from '@smui/select'
    import Accordion, {Header, Content, Panel} from '@smui-extra/accordion';
    import Chip, {Set, TrailingAction, Text} from '@smui/chips';
    import List, {Meta, Item} from "@smui/list";
    import Checkbox from "@smui/checkbox";

    export let data: PageData;

    let source = $page.url.searchParams.get('source') || '';
    let aspect = $page.url.searchParams.get('aspect') || '';
    let polarity = $page.url.searchParams.get('polarity') || '';
    let selectedPage = $page.url.searchParams.get('page') || 1;
    let selectedSources = [source.split(',')].filter(s => s !== '');
    let selectedAspects = [aspect.split(',')].filter(s => s !== '');
    let selectedPolarity = [source.split(',')].filter(s => s !== '');
    let appliedFilters = [];

    $: {
       selectedSources.length > 0 ? source = selectedSources.join(',') : source = '';
       selectedAspects.length > 0 ? aspect = selectedAspects.join(',') : aspect = '';
       selectedPolarity.length > 0 ? polarity = selectedPolarity.join(',') : polarity = '';
       updateFilters();
    }

    const pageSize = 20;
    const reviews = writable<ReviewWithAspects[]>(data?.reviews.reviews || []);

    async function updateFilters() {
        const queryParams = new URLSearchParams({});
        if(source !== '')
            queryParams.set('source', source);
        if(aspect !== '')
            queryParams.set('aspect', aspect);
        if(polarity !== '')
            queryParams.set('polarity', polarity);
        if(selectedPage !== 1)
            queryParams.set('page', selectedPage.toString());
        if (browser) {
            goto(`?${queryParams.toString()}`)
        }
    }

    function updateSelectedSource(value: string) {
        updateFilters();
    }

    function updateSelectedAspect(value: string) {
        updateFilters();
    }

    function updateSelectedPage(value: number) {
        updateFilters();
    }

    function onReset() {
        selectedSources = [];
        selectedAspects = [];
        selectedPolarity = [];
        updateFilters();
    }

</script>

<section class="review-page">
    <div class="filters-bar">
<!--        <Textfield-->
<!--                label="Search"-->
<!--                variant="filled"-->
<!--                bind:value={searchValue}-->
<!--        >-->
<!--            <HelperText slot="helper">...graphics are amazing</HelperText>-->
<!--        </Textfield>-->
        <Button on:click={onReset}><Label>Reset</Label></Button>
        <div class="accordion-container">
            <Accordion>
                <Panel>
                    <Header>Source</Header>
                    <Content>
                        <List
                                checkList
                        >
                            {#each data.sources as source}
                                <Item>
                                    <Label>{source.name}</Label>
                                    <Meta>
                                        <Checkbox bind:group={selectedSources} value="{source.name}"/>
                                    </Meta>
                                </Item>
                            {/each}
                        </List>
                    </Content>
                </Panel>
                <Panel>
                    <Header>Aspect</Header>
                    <Content>
                        <List
                                checkList
                        >
                            {#each data.aspects as aspect}
                                <Item>
                                    <Label>{aspect}</Label>
                                    <Meta>
                                        <Checkbox bind:group={selectedAspects} value="{aspect}"/>
                                    </Meta>
                                </Item>

                            {/each}
                        </List>
                    </Content>
                </Panel>
                <Panel>
                    <Header>Polarity</Header>
                    <Content>
                        <List
                                checkList
                        >
                            {#each  data.polarities as polarity}
                                <Item>
                                    <Label>{polarity}</Label>
                                    <Meta>
                                        <Checkbox bind:group={selectedPolarity} value="{polarity}"/>
                                    </Meta>
                                </Item>
                            {/each}

                        </List>
                    </Content>
                </Panel>
            </Accordion>
        </div>
    </div>
    <div class="main-list">
        <div class="review-list">
            {#each $reviews as review}
                <ReviewCard {review}/>
            {/each}
        </div>
        <div class="page-buttons-container">
            <Button on:click={() => goto(`?page=${1}`)} disabled={selectedPage === 1} padded>
                <Icon class="material-icons">keyboard_double_arrow_left</Icon>
            </Button>
            <Button on:click={() => goto(`?page=${Math.ceil(data.total/pageSize)}`)} disabled={selectedPage === 1}
                    padded>
                <Icon class="material-icons">keyboard_double_arrow_right</Icon>
            </Button>
        </div>
    </div>

</section>

<style>
    .review-page {
        display: flex;
        flex-direction: row;
    }

    .main-list {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        margin-left: 1rem;
    }

    .review-list {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        margin-bottom: 1rem;
    }

    .filters-bar {
        width: 200px;
        display: flex;
        flex-direction: column;
        padding: 0.5rem;
    }

    .applied-filters {
        display: flex;
        flex-direction: row;
        flex: 1;
        flex-wrap: wrap;
    }
</style>