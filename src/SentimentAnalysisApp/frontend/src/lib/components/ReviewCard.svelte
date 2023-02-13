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
    import type {ReviewWithAspects} from "../client";
    import {writable} from "svelte/store";

    let annotate = false;
    export let review: ReviewWithAspects;

    import {onMount} from "svelte";
    import {string} from "zod";

    interface Token {
        text: string;
        isSelected: boolean;
        isFocused: boolean;
        group: number | null;
    }

    let text = review.text;
    let tokens: Token[] = [];
    let groups = new Map<number, Token[]>();
    let isMouseDown = false;
    let isEnterPressed = false;
    let groupIdxCounter = 0;
    tokens = text.split(" ").map((t) => (
        {
            text: t,
            isSelected: false,
            isFocused: false,
            group: null
        }
    ));

    function getToken(event) {
        const target = event.target as HTMLAnchorElement;
        const idx = Number(target.dataset.idx);
        return tokens[idx];
    }

    function handleMouseDown() {
        isMouseDown = true;
    }

    function handleMouseUp() {
        isMouseDown = false;
    }

    function handleKeyDown(event: KeyboardEvent) {
        if (event.key === "Enter") {
            isEnterPressed = true;
            const selectedTokens = tokens.filter((t) => t.isSelected);
            if (selectedTokens.length > 0) {
                const group = groupIdxCounter++;
                selectedTokens.forEach((t) => (t.group = group));
                groups.set(group, selectedTokens);
            }
        } else if (event.key === "Escape") {
            console.log("clearing tokens..")
            const selectedTokens = tokens.filter((t) => t.isSelected);
            if (selectedTokens.length > 0) {
                selectedTokens.forEach((t) => {
                    t.isSelected = false;
                    t.isFocused = false;
                    t.group = null;
                });
            }
        }
    }

    function handleKeyUp(event: KeyboardEvent) {
        const target = event.target as HTMLAnchorElement;
        const idx = Number(target.dataset.idx);
        if (event.key === "Enter") {
            isEnterPressed = false;
        }
    }

    function handleMouseOver(event: MouseEvent) {
        const token = getToken(event);
        if (isMouseDown || isEnterPressed) {
            token.isSelected = true;
        }
    }

    function handleClick(event: MouseEvent) {
        const token = getToken(event);
        if (token.group !== null) {
            const selectedInGroup = groups.get(token.group);
            const otherTokens = tokens.filter((t) => t.group && t.group !== token.group);
            selectedInGroup.forEach((t) => (t.isSelected = true));
            otherTokens.forEach((t) => (t.isSelected = false));
        } else {
            console.log("clicked", token)
            token.isSelected = !token.isSelected;
        }
        console.log("clicked", tokens)
    }

    function handleFocus(event: FocusEvent) {
        const token = getToken(event);
        // token.isSelected = true;
        // if (token.group !== null) {
        //     const selectedInGroup = groups.get(token.group);
        //     if (selectedInGroup) {
        //         selectedInGroup.forEach((t) => (t.isFocused = true));
        //     }
        // } else {
        //     tokens.forEach((t) => (t.isFocused = false));
        // }
    }

    function handleBlur(event: FocusEvent) {
        const token = getToken(event);
        token.isFocused = false;
    }


</script>


<div class="review-container">
    <Card>
        <Content class="review-card-maincontent">
            <div class="review-card__left">
                <div style="user-select: none; height: 150px; box-sizing: border-box; padding: 16px; overflow: auto;"
                     on:keydown={handleKeyDown}
                     on:keyup={handleKeyUp}
                >
                    {#each tokens as token, idx}
                        <a tabindex="0"
                           class="token"
                           data-idx={idx}
                           class:selected={token.isSelected}
                           on:mousedown={handleMouseDown}
                           on:mouseup={handleMouseUp}
                           on:mouseover={handleMouseOver}
                           on:focus={handleFocus}
                           on:click={handleClick}
                        >
                            {token.text}
                        </a>
                    {/each}
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

    * :global(.token) {
        padding: 0.5em;
        margin: 0.25em;
        background-color: white;
        border: 1px solid lightgray;
        border-radius: 0.25em;
        text-decoration: none;
        color: black;
    }

    * :global(.token.selected) {
        border: 2px solid dodgerblue;
    }

    * :global(.token.focused) {
        background-color: rgba(30, 144, 255, 0.91);
    }

    * :global(.token.negative) {
        background-color: #b62929;
    }

    * :global(.token.positive) {
        background-color: #29b629;
    }

    * :global(.token.neutral) {
        background-color: #b6b629;
    }

</style>