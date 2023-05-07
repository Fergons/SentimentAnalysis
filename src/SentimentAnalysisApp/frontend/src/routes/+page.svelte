<!-- Created by Frantisek Sabol -->
<script lang="ts">
    import Button, {Label, Icon} from '@smui/button';
    import Card, {Content, Actions} from '@smui/card';
    import {page} from '$app/stores';
    import userStore from "../lib/stores/user";
</script>

<section class="about-section">
    <div class="about-text-container">
        <p class="mdc-typography--body1">
            Welcome to our project on Aspect Based Sentiment Analysis! Our goal is to analyze
            user-generated reviews and gain insights into specific aspects of the individual games and
            game genres. Using state-of-the-art natural language processing techniques, we aim to
            accurately identify and categorize the sentiments expressed in each aspect of the reviews.
        </p>
    </div>
</section>

<section class="features-section">
    <div class="about-features-text">
    </div>
</section>

<style>
    .about-section {
        display: flex;
        flex-direction: column;
        max-width: 720px;
    }

    .features-section {
        display: flex;
        flex-direction: column;
        width: 720px;
    }
</style>
