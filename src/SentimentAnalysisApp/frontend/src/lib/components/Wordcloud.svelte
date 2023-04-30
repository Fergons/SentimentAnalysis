<script>
    import {onMount, onDestroy} from 'svelte';
    import {writable} from 'svelte/store';
    import {scaleLinear, scaleLog} from 'd3-scale';
    import layout from 'd3-cloud';
    import {schemeCategory10} from 'd3-scale-chromatic';
    import {LayerCake, Svg} from 'layercake';
    import Button from '@smui/button';
    import IconButton from '@smui/icon-button';
    import Fab, {Icon} from '@smui/fab';

    export let data;
    const categories = Object.keys(data.categories);
    console.log(data)
    export let selectedCategory = data.categories && Object.keys(data.categories).length > 0 ?  Object.keys(data.categories)[0] : 'overall';
    let polarities = selectedCategory && data.categories[selectedCategory] ? Object.keys(data.categories[selectedCategory]) : [];
    let selectedPolarity = polarities?.length > 0 ? polarities[0] : undefined;
    const polarityColorMap = new Map([
        ["positive", "#28a745"],
        ["negative", "#dc3545"],
        ["neutral", "#007bff"]
    ]);
    const words = writable([]);
    let width = 500;
    let height = 300;

    function updateWordcloud(category, polarity) {
        let inputData = [];
        if (!category || !polarity) {
            return;
        } else {
            inputData = data.categories[category] ? data.categories[category][polarity] ? data.categories[category][polarity] : [] : [];
        }

        const fill = scaleLinear([`dark${polarityColorMap.get(polarity)}`, polarityColorMap.get(polarity)]).domain([1, inputData.length]);
        const minCount = Math.min(...inputData.map(d => d.count));
        const maxCount = Math.max(...inputData.map(d => d.count));

        // Create a logarithmic scale for word sizes
        const sizeScale = scaleLog()
            .domain([minCount, maxCount])
            .range([14, 100]);

        layout()
            .size([width, height])
            .words(inputData.map((d, i) => ({text: d.term, size: sizeScale(d.count), index: i})))
            .padding(5)
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

    function previousCategory() {
        const index = categories.indexOf(selectedCategory);
        selectedCategory = categories[(index - 1 + categories.length) % categories.length];
    }

    function nextCategory() {
        const index = categories.indexOf(selectedCategory);
        selectedCategory = categories[(index + 1) % categories.length];
    }

    function previousPolarity() {
        const index = polarities.indexOf(selectedPolarity);
        selectedPolarity = polarities[(index - 1 + polarities.length) % polarities.length];
    }

    function nextPolarity() {
        const index = polarities.indexOf(selectedPolarity);
        selectedPolarity = polarities[(index + 1) % polarities.length];
    }

    onMount(() => {
        updateWordcloud(selectedCategory, selectedPolarity);
    });


    $: {
        if (selectedCategory !== undefined && categories.includes(selectedCategory) && selectedPolarity !== undefined && polarities.includes(selectedPolarity)) {
            const asArray = Object.entries(data.categories[selectedCategory]).filter(([key, value]) => value.length > 0);
            polarities = asArray.map(([key, value]) => key);

            if (!polarities.includes(selectedPolarity))
                selectedPolarity = polarities[0];
            updateWordcloud(selectedCategory, selectedPolarity);
        } else {
            updateWordcloud(undefined, undefined)

        }
    }
</script>

<div class="wordcloud-settings">
    <div class="bar">
        <div class="flexy">

            <Fab on:click={previousCategory} disabled={categories.length < 2} mini color="primary">
               <Icon class="material-icons">arrow_back</Icon>
            </Fab>

        </div>
        <span class="selection mdc-typography--headline4">{selectedCategory.split('_').join(" & ")}</span>
        <div class="flexy">

            <Fab on:click={nextCategory} disabled={categories.length < 2} mini color="primary">
                  <Icon class="material-icons">arrow_forward</Icon>
            </Fab>

        </div>
    </div>
    <div class="bar">
        <div class="flexy">

            <Fab on:click={previousPolarity} mini color="primary">
              <Icon class="material-icons">arrow_back</Icon>
            </Fab>

        </div>
        <span class="selection mdc-typography--headline5">{selectedPolarity}</span>
        <div class="flexy">

            <Fab on:click={nextPolarity} disabled={polarities.length < 2} mini color="primary">
                <Icon class="material-icons">arrow_forward</Icon>
            </Fab>
        </div>
    </div>
</div>
<div class="wordcloud-container" style=" width: {width}px; height: {height}px;">
    <LayerCake>
        <Svg viewBox="0 0 {width} {height}">
            <g transform="translate({width / 2}, {height / 2})">
                {#if $words.length === 0}
                    <text text-anchor="middle" class="mdc-typography--headline2">No data!</text>
                {/if}
                {#each $words as {text, size, fill, transform}}
                    <text
                            on:click="{() => console.log(text)}"
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

    .wordcloud-container {
        display: flex;
        margin: 0 auto;
        padding: 2rem 1rem 1rem;
    }

    .wordcloud-settings {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 1rem;
    }

    .bar {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        margin: 0 auto;
        flex: 1;
        gap: 10px;
        width: 480px;
    }

    .selection {
        font-weight: bold;
        text-transform: capitalize;
        text-align: center;
        border-radius: 4px;
        padding: 6px 12px;
        margin: 0 4px;
    }

    .flexy {
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>