<script>
    import {onMount, onDestroy} from 'svelte';
    import {writable} from 'svelte/store';
    import {scaleOrdinal} from 'd3-scale';
    import layout from 'd3-cloud';
    import {schemeCategory10} from 'd3-scale-chromatic';
    import {LayerCake, Svg} from 'layercake';

    let data = {
        "categories": {
            "gameplay": {
                "positive": ["foes", "OP loot", "quest doing", "gameplay", "rogue-like RPG/Settlement building game", "settlement"],
                "negative": [],
                "neutral": ["farm resources", "achievements", "Strength ramping of hero"]
            }, "overall": {"positive": [], "negative": [], "neutral": ["game time"]}
        }
    }
    export let categories = Object.keys(data.categories);
    export let selectedCategory = Object.keys(data.categories)[0];
    let selectedPolarity = 'positive';
    const words = writable([]);
    let width = 600;
    let height = 400;

    function updateWordcloud(category, polarity) {

        const inputData = data.categories[category] ? data.categories[category][polarity] : [];
        const fill = scaleOrdinal(schemeCategory10);
        layout()
            .size([width, height])
            .words(inputData.map((d, i) => ({text: d, size: 10 + Math.random() * 50, index: i})))
            .padding(5)
            .rotate(() => 0)
            .font('Impact')
            .fontSize(d => d.size)
            .on('end', draw)
            .start();

        function draw(outputData) {
            words.set(
                outputData.map(d => ({
                    ...d,
                    fill: fill(d.index),
                    transform: `translate(${[d.x, d.y]})rotate(${d.rotate})`
                }))
            );
        }
    }

    onMount(() => {
        updateWordcloud(selectedCategory, selectedPolarity);
    });


    $: updateWordcloud(selectedCategory, selectedPolarity);
</script>

<div class="wordcloud-settings">

</div>
<div class="wordcloud-container">
    <LayerCake>
        <Svg {width} {height} viewBox="0 0 {width} {height}">
            <g transform="translate({width / 2}, {height / 2})">
                {#each $words as {text, size, fill, transform}}
                    <text
                            style="font-size: {size}px; font-family: Impact; fill: {fill}"
                            text-anchor="middle"
                            transform="{transform}">
                        {text}
                    </text>
                {/each}
            </g>
        </Svg>
    </LayerCake>
</div>
<style>
    .wordcloud-settings {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }

    .wordcloud-container {
        display: flex;
        max-width: 600px;
        height: 400px;
        overflow: hidden;
    }
</style>