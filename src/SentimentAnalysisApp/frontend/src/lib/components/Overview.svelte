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

    const enoughData = data && Object.keys(data.sources).length > 0;
    const categoryScores = [calculateCategoryScores(data)];
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

    function calculateCategoryScoresPerSource(summary: AspectsSummary): { [key: string]: { [key: string]: number } } {
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
        const categoryScores = {
            gameplay: 5,
            performance_bugs: 5,
            price: 5,
            audio_visuals: 5,
            community: 5,
            overall: 5
        };
        const aggregatedPolarityCounts = {};
        console.log("summary: ", summary)

        for (const sourceId in summary.sources) {
            const sourcePolarityCounts = summary.sources[sourceId];

            for (const category in sourcePolarityCounts.categories) {
                const polarityCounts = sourcePolarityCounts.categories[category];

                if (!aggregatedPolarityCounts[category]) {
                    aggregatedPolarityCounts[category] = {positive: 0, negative: 0, neutral: 0};
                }

                aggregatedPolarityCounts[category].positive += polarityCounts.positive;
                aggregatedPolarityCounts[category].negative += polarityCounts.negative;
                aggregatedPolarityCounts[category].neutral += polarityCounts.neutral;
            }
        }

        for (const category in aggregatedPolarityCounts) {
            const polarityCounts = aggregatedPolarityCounts[category];
            const totalPolarityCount = polarityCounts.positive + polarityCounts.negative + polarityCounts.neutral;

            if (totalPolarityCount === 0) {
                categoryScores[category] = 5.0;
            } else {
                const positivePercentage = polarityCounts.positive / totalPolarityCount;
                const negativePercentage = polarityCounts.negative / totalPolarityCount;

                // Calculate weighted score based on the difference between positive and negative percentages
                const weightedScore = 10 * (0.4 * positivePercentage - 0.2 * negativePercentage);
                console.log("weightedScore: ", weightedScore)
                // Scaling factor based on the total number of counts, using a square root function
                const scalingFactor = Math.sqrt(totalPolarityCount);
                console.log("scalingFactor: ", scalingFactor)


                // Calculate the final score with the scaling factor, ensuring it stays within the range 0-10
                const finalScore = Math.max(0, Math.min(10, 5 + (weightedScore * scalingFactor) / 10));

                categoryScores[category] = Math.round(finalScore * 100) / 100;
            }
        }

        return categoryScores;
    }

</script>

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
        <Wordcloud bind:selectedCategory={activeCategory}/>
    {/if}
</div>


<style>
    .chart-container {
        display: flex;
        flex: 1;
        margin: 0 auto;
        width: 500px;
        height: 400px;
        padding: 1rem;
        justify-content: center;
    }

    .wordcloud {
        display: flex;
        flex-direction: column;
        flex: 1;
        padding: 1rem;
    }
</style>





