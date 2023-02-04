<script lang="ts">
    import Button from '@smui/button';
    import {Row, Section, Title, AutoAdjust} from '@smui/top-app-bar';
    import IconButton from '@smui/icon-button';
    import {Label, Icon, Svg} from '@smui/common';
    import {mdiGithub, mdiWeb} from '@mdi/js';
    import LayoutGrid, {Cell} from '@smui/layout-grid'
    import Banner from "@smui/banner";
    import {page} from '$app/stores';

    /** @type {import('./$types').PageData} */
    type Game = {
        name: string,
        description: string,
        url: string,
        image: string,
        categories: string[],
        date: string
    }
    export let data: {
        title: string,
        game: Game
    };
</script>

<div class="game-page">
    <div class="overview container">
        <slot/>
    </div>
    <Banner
            open
            autoClose={false}
    >
        <Label slot="label">{data.game.description}</Label>
    </Banner>
    <div class="stats container">
        <slot/>
    </div>
</div>


<style>

    /*# style game-page with flex align content in center*/
    .game-page {
        display: flex;
        align-content: center;
        justify-content: center;
        max-width: 1200px;
        margin: var(--mdc-layout-grid-margin-desktop);
    }


    .stats {
        height: 300px;
        background-color: #f00;
    }

    .overview {
        height: 300px;
        background-color: #0f0;
    }
</style>