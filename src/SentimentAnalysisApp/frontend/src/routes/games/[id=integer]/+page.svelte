<script lang="ts">
    import Overview from "../../../lib/components/Overview.svelte";
    import Stats from "../../../lib/components/Stats.svelte";
    import GameCard from "../../../lib/components/GameCard.svelte";

    export let data;
    const {name, subtitle, game, reviewSummary, aspectSummary, sources, aspectWordcloud} = data;
</script>

<section>
    <div class="game-banner">
        <GameCard {game} nonInteractive={true}></GameCard>
    </div>
    <div class="overview-section">
         <h5 class="mdc-typography--headline5" style="padding: 1.5rem 0 1rem 2rem; margin: 0;">
            Score of aspect categories
        </h5>
        <Overview data={{aspectSummary, aspectWordcloud}}/>
    </div>

    <div class="stats-section">
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
    .stats-section {
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 100%;
    }
    .game-banner {
        margin-bottom: 1rem;
    }
</style>
