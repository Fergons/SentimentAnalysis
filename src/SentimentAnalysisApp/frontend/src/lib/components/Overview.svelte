<script lang="ts">
    import type {AspectsSummary} from '../client';
    import {LayerCake, Svg} from 'layercake';
    import {scaleLinear} from 'd3-scale';
    import RadarChart from "./RadarChart.svelte";
    import AxisRadial from './AxisRadial.svelte';
    import {onMount} from 'svelte';

    let Wordcloud;

    onMount(async () => {
        const module = await import('./Wordcloud.svelte');
        Wordcloud = module.default;
    });

    export let data;
    const enoughData = data.aspectSummary && Object.keys(data.aspectSummary.sources).length > 0;
    const categoryScores = [calculateCategoryScores(data.aspectSummary)];
    const seriesKey = '';
    const xKey = ['overall', 'gameplay', 'audio_visuals', 'performance_bugs', 'community', 'price'];

    const seriesNames = Object.keys(categoryScores[0]).filter(d => d !== seriesKey);
    categoryScores.forEach(d => {
        seriesNames.forEach(name => {
            d[name] = +d[name];
        });
    });

    let activeCategory = 'overall';

    function setActiveCategory(event) {
        activeCategory = event.detail.category;
    }
    // Calculate the score for each category based on the polarity counts and source
    function calculateCategoryScoresPerSource(summary: AspectsSummary): { [key: string]: { [key: string]: number } } {
        // If there's no data for the category, set the score to 5.0
        const initialValues = {
            gameplay: 5,
            performance_bugs: 5,
            price: 5,
            audio_visuals: 5,
            community: 5,
            overall: 5
        };
        const categoryScores = {};

        for (const sourceId in summary.sources) {
            categoryScores[sourceId] = {...initialValues};
            const sourcePolarityCounts = summary.sources[sourceId];

            for (const category in sourcePolarityCounts.categories) {
                const polarityCounts = sourcePolarityCounts.categories[category];
                const totalPolarityCount = polarityCounts.positive + polarityCounts.negative + polarityCounts.neutral;
                // If there's no data for the category, set the score to 5.0

                if (totalPolarityCount === 0) {
                    categoryScores[sourceId][category] = 5.0;
                } else {
                    const positivePercentage = polarityCounts.positive / totalPolarityCount;
                    const negativePercentage = polarityCounts.negative / totalPolarityCount;
                    const neutralPercentage = polarityCounts.neutral / totalPolarityCount;

                    const weightedScore = 4.0 * positivePercentage + (-2.0) * negativePercentage + 1.0 * neutralPercentage;

                    // Normalize the weighted score to a range of 0.0 to 10.0
                    const normalizedScore = (weightedScore + 1) * 5;

                    categoryScores[sourceId][category] = Math.round(normalizedScore * 100) / 100;
                }
            }
        }

        return categoryScores;
    }

    function calculateCategoryScores(summary) {
        // If there's no data for the category, set the score to 5.0
        const categoryScores = {
            gameplay: 5,
            performance_bugs: 5,
            price: 5,
            audio_visuals: 5,
            community: 5,
            overall: 5
        };
        const aggregatedPolarityCounts = {};
        // Aggregate the polarity counts for each category across all sources
        for (const sourceId in summary.sources) {
            const sourcePolarityCounts = summary.sources[sourceId];

            for (const category in sourcePolarityCounts.categories) {
                const polarityCounts = sourcePolarityCounts.categories[category];
                // If first time seeing this category, initialize the counts
                if (!aggregatedPolarityCounts[category]) {
                    aggregatedPolarityCounts[category] = {positive: 0, negative: 0, neutral: 0};
                }
                aggregatedPolarityCounts[category].positive += polarityCounts.positive;
                aggregatedPolarityCounts[category].negative += polarityCounts.negative;
                aggregatedPolarityCounts[category].neutral += polarityCounts.neutral;
            }
        }
        // Calculate the final score for each category
        for (const category in aggregatedPolarityCounts) {
            const polarityCounts = aggregatedPolarityCounts[category];
            const totalPolarityCount = polarityCounts.positive + polarityCounts.negative + polarityCounts.neutral;

            if (totalPolarityCount === 0) {
                categoryScores[category] = 5.0;
            } else {
                const positivePercentage = polarityCounts.positive / totalPolarityCount;
                const negativePercentage = polarityCounts.negative / totalPolarityCount;

                // Calculate weighted score based on the difference between positive and negative percentages
                const weightedScore = (4 * positivePercentage - 2.1 * negativePercentage) / 3.2;

                // Scaling factor
                const scalingFactor = 5; //(-5 to 5 range and then add -5)


                // Calculate the final score with the scaling factor, ensuring it stays within the range 0-10
                const finalScore = Math.max(0, Math.min(10, 5 + weightedScore * scalingFactor));

                categoryScores[category] = Math.round(finalScore * 100) / 100;
            }
        }

        return categoryScores;
    }

</script>
<div class="overview-container">
    <div class="chart-container">
        <LayerCake
                ssr={true}
                percentageRange={true}
                width={100}
                height={100}
                padding={{ top: 16, right: 16, bottom: 16, left: 16 }}
                x={xKey}
                xDomain={[0, 10]}
                xScale={scaleLinear}
                xRange={[0, 150]}
                data={categoryScores}
        >
            <Svg>
                <AxisRadial textColor="#fff" textFont="roboto-mono" on:categorySelected={setActiveCategory}/>
                {#if enoughData}
                    <RadarChart/>
                {:else}
                    <text x="49%" y="48%" text-anchor="middle" fill="#fff" font-family="roboto-mono">
                        NO DATA
                    </text>
                {/if}
            </Svg>
        </LayerCake>
    </div>

    <div class="wordcloud">
        {#if Wordcloud}
            <svelte:component this={Wordcloud} data={data.aspectWordcloud} bind:selectedCategory={activeCategory}/>
        {/if}
    </div>
</div>


<style>
    .overview-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-evenly;
        gap: 1rem;
        margin: auto auto 1rem auto;
        width: 100%;
        min-width: auto;
    }

    .chart-container {
        display: flex;
        width: 500px;
        height: 400px;
        padding: 1rem;
        justify-content: center;
    }

    .wordcloud {
        display: flex;
        flex-direction: column;
        padding: 1rem;
    }
</style>





