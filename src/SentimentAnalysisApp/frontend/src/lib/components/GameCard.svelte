<script lang="ts">
    import type {Game} from '../server/api/types';
    import Card, {
        Media,
        MediaContent,
        Content,
        PrimaryAction,
        Actions,
        ActionButtons,
        ActionIcons
    } from '@smui/card';
    import Button, {Label, Icon} from '@smui/button';
    import IconButton from '@smui/icon-button';
    import {goto} from '$app/navigation';

    export let game: Game;
    let options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
</script>

<div class="card-container">
    <Card>
        <PrimaryAction on:click={() => goto('/games/' + game.id)}>
            <Media class="card-media-219x102"
                   aspectRatio="219x102"
            >

                <img src={game.image_url} loading="lazy" width="460" height="215" alt={game.name}>

                <MediaContent class="mdc-typography--body2 card-media-content">
                    <h2 class="mdc-typography--headline6" style="margin: 0; text-transform: uppercase">
                        {game.name}
                    </h2>
                    <h3 class="mdc-typography--subtitle2" style="margin: 0 0 10px; color: #888;">
                        {new Intl.DateTimeFormat("default", options).format(new Date(game.release_date))}
                    </h3>
                </MediaContent>
                <MediaContent class="card-media-content">
                    <h2 class="mdc-typography--headline6" style="margin: 0; text-transform: uppercase">
                        10/10
                    </h2>
                    <h2 class="mdc-typography--subtitle2" style="margin: 0 0 10px; color: #888;">
                        1000 reviews
                    </h2>
                </MediaContent>
            </Media>
        </PrimaryAction>
    </Card>
</div>

<style>
    * :global(.card-media-219x102) {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        margin: 16px;
    }

    * :global(.card-media-219x102>img) {
        width: 219px;
        height: 102px;
        margin-left: auto;
        border-radius: 6px;
        margin-right: 8px;
        background-image: radial-gradient(circle, rgba(255, 255, 255, 0), rgba(0, 0, 0, 0.7));
        line-height: 102px;
        text-align: center;
        font-family: 'Roboto', monospace;
        font-size: 24px;
        font-weight: bold;
        text-transform: uppercase;
    }

    * :global(.card-media-content) {
        position: relative;
    }

    * :global(.card-media-219x102 :last-child) {
        margin-left: auto;
    }
    * :global(.card-media-219x102 :first-child) {
        margin-left: 0;
    }

</style>
