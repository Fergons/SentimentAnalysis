<script lang="ts">
    import {navigating} from "$app/stores";
    import type {PageData} from "./$types";
    import type {ReviewWithAspects} from "../../lib/client";

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
                <div class="review-body">
                    <div class="review-body__left">
                        <h3>{review.id}</h3>
                        <p style="width: 400px">{review.text}</p>
                    </div>
                    <div class="review-body__right">
                        <p>Language: {review.language}</p>
                        <div class="review-aspects">
                            <ul>
                                {#each review.aspects as aspect}
                                    <li>{aspect.term}: {aspect.polarity}</li>
                                {/each}
                            </ul>

                        </div>
                    </div>
                </div>
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
    }

    .review-body {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        margin-bottom: 24px;
    }

    .review-body__left {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .review-body__right {
        display: flex;
        flex-direction: column;
    }


</style>