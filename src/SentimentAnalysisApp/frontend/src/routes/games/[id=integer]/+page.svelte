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

    <div class="stats-container">
        <h5 class="mdc-typography--headline5" style="margin: 1.5rem 0 0 2rem;">
            Visualization of sentiment and reviews in time
        </h5>
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
        width: 100%;
    }

    .overview-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-evenly;
        gap: 1rem;
        margin: auto auto 1rem auto;
        width: 100%;
        min-width: auto;
    }
</style>
