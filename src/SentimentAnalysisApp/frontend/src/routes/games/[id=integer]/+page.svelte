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

    const stats = data.stats.reviews_summary.data.reduce((acc, cur) => {
        const sourceId = cur.source_id;
        const total = cur.total;
        const date = cur.date;

        if (!acc[date]) {
            acc[date] = {[sourceId]: total, date};
        } else {
            acc[date][sourceId] = total;
        }
        return acc;
    }, {});

</script>

<section>
    <div class="overview-container">
        <Overview data={data.overview.category_scores}/>
    </div>
    <Banner open autoClose={false}>
        <Label slot="label">{data.game.name}</Label>
    </Banner>
    <div class="stats-container">
        <Stats data={Object.values(stats)}/>
    </div>
</section>

<style>
    .stats-container {
        width: 100%;
        height: 300px;
    }

    .overview-container {
        height: 420px;
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: flex-start;
    }
</style>
