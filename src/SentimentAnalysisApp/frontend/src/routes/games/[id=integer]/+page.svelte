<script lang="ts">
    import {Label} from '@smui/common';
    import Banner from '@smui/banner';
    import Overview from "../../../lib/components/Overview.svelte";
    import Stats from "../../../lib/components/Stats.svelte";

    export let data;
    const {name, subtitle, game, reviewSummary, aspectSummary, sources, aspectWordcloud} = data;

</script>

<section>
    <div class="overview-container">
        <Overview data={{aspectSummary, aspectWordcloud}}/>
    </div>

    <Banner open autoClose={false}>
        <Label slot="label">Stats</Label>
    </Banner>
    <div class="stats-container">
        <Stats data={{
            reviewSummary: reviewSummary,
            aspectSummary: aspectSummary,
            sources: sources}}/>
    </div>
</section>

<style>
    .stats-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        gap: 16px;
    }

    .overview-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-evenly;
        gap: 1rem;
        margin: 0 auto;
        width: 100%;
        min-width: auto;
    }
</style>
