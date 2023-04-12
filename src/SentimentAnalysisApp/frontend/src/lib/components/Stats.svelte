<script lang='ts'>
    import {LayerCake, Svg, Html, flatten, groupLonger, ScaledSvg} from 'layercake';
    import {writable} from 'svelte/store';
    import Checkbox from '@smui/checkbox';
    import {scaleOrdinal} from 'd3-scale';
    import {stack} from 'd3-shape';
    import {timeParse, timeFormat} from 'd3-time-format';
    import {format, precisionFixed} from 'd3-format';
    import {max} from 'd3-array';

    import Multiline from './Multiline.svelte';
    import AxisX from './AxisX.svelte';
    import AxisY from './AxisY.svelte';
    import SharedTooltip from './SharedTooltip.svelte';
    import {transformSummary, generateColorMap} from '../utils/dataTransformer';
    import type {ReviewsSummaryDataPoint, ReviewsSummaryV2} from '../client';
    import type {Source} from '../client';
    import FormField from '@smui/form-field';
    import ChartSettingsGroup from './ChartSettingsGroup.svelte';
    import {timeDay, timeWeek, timeMonth, timeYear} from "d3-time";

    export let data: {
        sources: Map<number, Source>,
        summary: ReviewsSummaryV2
    };
    const sources = data.sources;
    const sourceNameMap = new Map<string, number>();
    sources.forEach((s, id) => sourceNameMap.set(s.name, id));
    const summary = data.summary;

    const xKey = 'date';
    const yKey = 'count';
    const zKey = 'source_type';

    let sourceNames: string[] = sources.size > 1 ? Array.from([...sourceNameMap.keys(), 'all']) : [sourceNameMap.keys().next().value];
    const defaultSourceSelection = sources.size > 1 ? ['all'] : [sourceNames[0]];
    let selectedSources: string[] = [...defaultSourceSelection];



    const sentimentNames = ['positive', 'negative', 'neutral'];
    const defaultSentimentSelection = [];
    let selectedSentiments = [...defaultSentimentSelection];

    const categoryTypeNames = ['gameplay', 'audio_visuals', 'performance_bugs', 'overall', 'price', 'community'];
    const defaultCategorySelection = [];
    let selectedCategories = [...defaultCategorySelection];

    const reviewTypeNames = ['total', 'processed'];
    const defaultReviewTypeSelection = ['total'];
    let selectedReviewTypes = [...defaultReviewTypeSelection];


    const typesNames = [...reviewTypeNames, ...sentimentNames, ...categoryTypeNames];
    //blue and dark blue for others green for positive, red for negative, grey for neutral
    let selectedTypes: string[] = ['total'];

    const colorMap = generateColorMap(sourceNames, typesNames);
    const onLast = (last, list) => [list[(list.indexOf(last)+1)%list.length]]


    const parseDate = timeParse("%Y-%m-%dT%H:%M:%S%Z");
    const timeBuckets = ['day', 'week', 'month', 'year'];
    const mapTimeBucketToTime = {
        day: timeDay,
        week: timeWeek,
        month: timeMonth,
        year: timeYear
    };
    let selectedTimeBucket: string = 'month';

    const countNames = sourceNames.flatMap(source => typesNames.map(type => `${source}_${type}`));
    let flatData;
    let groupedData;
    let selectedCounts: string[] = [];
    let yDomainMax = 10;


    $: {
        selectedTypes = [...selectedSentiments, ...selectedCategories, ...selectedReviewTypes];
        selectedCounts = [...selectedSources.flatMap(source => selectedTypes.map(type => `${source}_${type}`))];
        if (selectedCounts.length === 0) {
            selectedCounts = ["all_total"]
        }
        flatData = transformSummary(summary, selectedSources, selectedTypes, sourceNameMap, mapTimeBucketToTime[selectedTimeBucket]);
        flatData.forEach(d => {
            d[xKey] = typeof d[xKey] === 'string' ? parseDate(d[xKey]) : d[xKey];
            selectedCounts.forEach(name => {
                d[name] = +d[name] || 0;
                if(d[name]> yDomainMax) {
                    yDomainMax = d[name];
                }
            });
        });

        groupedData = groupLonger(flatData, selectedCounts, {
            groupTo: zKey,
            valueTo: yKey,
        });


    }

    const formatTickX = timeFormat('%b. %e');
    const formatTickY = d => {
        // format 1000 to 1K and 1000000 to 1M
        const formatter = format(`.${d}~s`);
        return formatter(d);
    };

</script>
<div class='chart-container'>
    <div class='chart-settings'>
        <ChartSettingsGroup
                seriesNames={sourceNames}
                bind:selectedSeries={selectedSources}
                onReset={() => selectedSources = [...defaultSourceSelection]}
                onLast={(last) => selectedSources = onLast(last, sourceNames)}
        >
        </ChartSettingsGroup>
        <ChartSettingsGroup
                seriesNames={reviewTypeNames}
                bind:selectedSeries={selectedReviewTypes}
                onReset={() => selectedReviewTypes = [...defaultReviewTypeSelection]}

        >
        </ChartSettingsGroup>
        <ChartSettingsGroup
                seriesNames={sentimentNames}
                bind:selectedSeries={selectedSentiments}
                onReset={() => selectedSentiments = [...defaultSentimentSelection]}
                onLast={(last) => selectedSentiments = onLast(last, sentimentNames)}
        >
        </ChartSettingsGroup>
        <ChartSettingsGroup
                seriesNames={categoryTypeNames}
                bind:selectedSeries={selectedCategories}
                onReset={() => selectedCategories = [...defaultCategorySelection]}
                onLast={(last) => selectedCategories = onLast(last, categoryTypeNames)}
        >
        </ChartSettingsGroup>
    </div>

    <div class='chart'>
        {#if groupedData && groupedData.length > 0}
            <LayerCake
                    ssr={true}
                    percentRange={true}
                    x={xKey}
                    y={yKey}
                    z={zKey}
                    xNice={true}
                    yNice={true}
                    yDomain={[0, yDomainMax]}
                    zScale={scaleOrdinal()}
                    zDomain={selectedCounts}
                    zRange={selectedCounts.map(name => colorMap.get(name))}
                    flatData={flatData}
                    data={groupedData}
            >
                <ScaledSvg>
                    <Multiline/>
                </ScaledSvg>

                <Html>
                <AxisX
                        gridlines={false}
                        ticks={flatData.filter(d => Object.keys(d).some(key => key !== xKey && d[key] !== 0))
                        .map(d => d[xKey])
                        .sort((a, b) => a - b)}
                        formatTick={formatTickX}
                        snapTicks={true}
                        tickMarks={true}
                />
                <AxisY
                        ticks={4}
                        formatTick={formatTickY}
                />
                <SharedTooltip

                        formatTitle={formatTickX}
                        dataset={flatData}
                />
                </Html>
            </LayerCake>
        {:else}
            <Svg>
                <text x='50%' y='50%' text-anchor='middle' dominant-baseline='central' font-size='24px'>
                    NO DATA
                </text>
            </Svg>
        {/if}
    </div>
</div>

<style>
    /*
      The wrapper div needs to have an explicit width and height in CSS.
      It can also be a flexbox child or CSS grid element.
      The point being it needs dimensions since the <LayerCake> element will
      expand to fill it.
    */
    .chart-container {
        display: flex;
        width: 100%;
        height: 100%;
        flex-direction: row;
    }

    .chart-settings {
        display: flex;
        flex-direction: column;
        padding: 1rem;
    }


    .chart {
        flex: 1;
        width: 400px;
        height: 300px;
        position: relative;
        padding: 2rem;

    }


    .checkbox-container label {
        margin-left: 0.5rem;
    }
</style>