<script lang="ts">
    import {navigating} from "$app/stores";
    import type {PageData} from "./$types";
    import type {ReviewWithAspects} from "../../lib/client";
    import ReviewCard from "../../lib/components/ReviewCard.svelte";
    export let data: PageData;
    let reviews: Map<number, ReviewWithAspects> = data?.reviews;
    console.log(reviews);
</script>

<section class="review-page">
    <div class="review-list">
        {#if $navigating}
            <div class="loading">Loading...</div>
        {:else}
            {#each [...reviews.entries()] as [id, review] }
                <ReviewCard {review}>
                </ReviewCard>
            {/each}
        {/if}
    </div>
</section>

<style>
    .review-page {
        display: flex;
        flex-direction: column;
        flex-grow: 1;

    }

    .review-list {
        width: 60vw;
        display: flex;
        flex-direction: column;
        margin-bottom: 48px;
        gap: 8px;
    }

</style>