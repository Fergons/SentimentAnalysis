<script lang="ts">
    import Button from '@smui/button';
    import {Row, Section, Title, AutoAdjust} from '@smui/top-app-bar';
    import IconButton from '@smui/icon-button';
    import {Label, Icon, Svg} from '@smui/common';
    import {mdiGithub, mdiWeb} from '@mdi/js';

    import LayoutGrid, {Cell} from '@smui/layout-grid';
    import Banner from '@smui/banner';
    import {page} from '$app/stores';
    import Overview from "../../../lib/components/Overview.svelte";
    import Stats from "../../../lib/components/Stats.svelte";

    export let data;
    const {title, subtitle, game, overview, stats} = data;

</script>

<section>
    <div class="overview-container">
        <Overview data={overview.categories}/>
    </div>
    <Banner open autoClose={false}>
        <Label slot="label">{game.name}</Label>
    </Banner>
    <div class="stats-container">
        <Stats data={stats.total}/>
    </div>
</section>

<style>
    .stats-container {
        width:100%;
        height: 300px;
         display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 16px;
    }

    .overview-container {
        width: 100%;
        height: 420px;
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: flex-start;
        gap: 16px;
    }
</style>
