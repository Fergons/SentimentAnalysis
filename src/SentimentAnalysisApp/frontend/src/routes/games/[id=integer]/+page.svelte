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

    export let data;


</script>

<section>
    <div class="overview-container">
        <Overview data={data.category_scores}/>

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
    }

    .overview-container {
        height: 420px;
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: flex-start;
    }
</style>
