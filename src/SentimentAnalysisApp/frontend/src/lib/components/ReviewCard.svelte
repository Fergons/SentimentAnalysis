<script lang="ts">
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
    import Fab from '@smui/fab';
    import FormField from '@smui/form-field';
    import IconButton from '@smui/icon-button';
    import {goto} from '$app/navigation';
    import type {ReviewWithAspects} from "../../lib/client";
    import {writable} from "svelte/store";

    let annotate = false;
    let token = writable("");
    export let _review: ReviewWithAspects;
    let review = {
        id: 1,
        language: 'czech',
        text: 'This is a review about a game. Because of Aspect_1 I think the game is bad.',
        score: "0.5",
        aspects: [
            {
                id: 1,
                term: 'Aspect_1',
                polarity: 'negative',
                category: 'gameplay',
                confidence: "0.4"
            },
            {
                id: 2,
                term: 'Aspect_2',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4"
            },
            {
                id: 3,
                term: 'Aspect_3',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4"
            },
            {
                id: 4,
                term: 'Aspect_4',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4"
            },
            {
                id: 5,
                term: 'Aspect_5',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4"
            },
            {
                id: 6,
                term: 'Aspect_6',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4"
            },
            {
                id: 7,
                term: 'Aspect_7',
                polarity: 'positive',
                category: 'audio_visual',
                confidence: "0.4"
            },
            {
                id: 8,
                term: 'Aspect_8',
                polarity: 'positive',
                category: 'price',
                confidence: "0.4"
            },
            {
                id: 9,
                term: 'Aspect_9',
                polarity: 'positive',
                category: 'story',
                confidence: "0.4"
            },
            {
                id: 10,
                term: 'Aspect_10',
                polarity: 'positive',
                category: 'community',
                confidence: "0.4"
            },
            {
                id: 11,
                term: 'Aspect_11',
                polarity: 'positive',
                category: 'community',
                confidence: "0.4"
            },
            {
                id: 12,
                term: 'Aspect_12',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4"
            },
            {
                id: 13,
                term: 'Aspect_13',
                polarity: 'positive',
                category: 'gameplay',
                confidence: "0.4"
            }
        ]
    };
</script>


<div class="review-container">
    <Card>
        <Content class="review-card-maincontent">
            <div class="review-card__left">
                <h2 class="mdc-typography--headline6">
                    {#each review.text.split(' ') as word}
                        <span>{word} </span>
                    {/each}
                </h2>
            </div>
            <div class="review-card__right">
                <h2 class="mdc-typography--headline3">{review.score}</h2>
                <p>Score</p>
            </div>
        </Content>
        <Actions>
            <ActionButtons>
                <Button disabled on:click={() => {}}>
                    <Label>View</Label>
                </Button>
                <form action="/reviews/{review.id}/annotation">
                    <Button bind:disabled={annotate} type="submit">
                        <Label>Submit Annotation</Label>
                    </Button>
                </form>
                 <IconButton toggle bind:pressed={annotate}>
                    <Icon class="material-icons" on>mode_edit</Icon>
                    <Icon class="material-icons">edit_off</Icon>
                </IconButton>
            </ActionButtons>
        </Actions>

    </Card>
</div>

<style>
    * :global(.review-card-maincontent) {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        box-sizing: border-box;
        width: 100%;
        height: 100%;
    }


</style>