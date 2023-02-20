<script lang="ts">
    import Button from '@smui/button';
    import {Row, Section, Title, AutoAdjust} from '@smui/top-app-bar';
    import IconButton from '@smui/icon-button';
    import {Label, Icon, Svg} from '@smui/common';
    import {mdiGithub, mdiWeb} from '@mdi/js';
    import LayoutGrid, {Cell} from '@smui/layout-grid';
    import Banner from '@smui/banner';
    import {page} from '$app/stores';
    import {Game} from '../../../lib/client';
    import RadarGraph from "../../../lib/components/RadarGraph.svelte";

    export let data: {
        title: string;
        game: Game;
        category_scores: Map<string, number>;
    };

    console.log(data);
    let radar: RadarGraph;

</script>

<section>
    <div class="overview-container">
            <RadarGraph data={data.category_scores}/>
    </div>
    <Banner open autoClose={false}>
        <Label slot="label">{data.game.name}</Label>
    </Banner>
    <div class="stats-container">
        <slot/>
    </div>
</section>

<style>
    .stats-container {
        height: 300px;
        background-color: #f00;
    }

    .overview-container {
        height: 300px;
        background-color: #0f0;
    }
</style>
