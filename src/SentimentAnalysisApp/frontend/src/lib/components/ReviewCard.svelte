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
    import IconButton from '@smui/icon-button';
    import {goto} from '$app/navigation';
    import type {ReviewWithAspects} from "../client";

    let annotate = false;
    export let review: ReviewWithAspects;
</script>


<div class="review-container">
    <Card>
        <Content class="review-card-maincontent">
            <div class="review-card__left">
                <div style="user-select: none; height: 150px; box-sizing: border-box; padding: 16px; overflow: auto;">
                    <p>{review.text || 'no'}</p>
                </div>
            </div>
            <div class="review-card__right">
                <h2 class="mdc-typography--headline3">0.5</h2>
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

    * :global(.review-card__left) {
        display: flex;
        flex-direction: row;
        flex-grow: 1;
        width: 100%;
        height: 100%;
    }

</style>