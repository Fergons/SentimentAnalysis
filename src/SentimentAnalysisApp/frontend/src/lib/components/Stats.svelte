<script lang='ts'>
    import {LayerCake, Svg, Html, flatten, groupLonger, ScaledSvg} from 'layercake';
    import {writable} from 'svelte/store';
    import Checkbox from '@smui/checkbox';
    import {scaleOrdinal} from 'd3-scale';
    import {stack} from 'd3-shape';
    import {timeParse, timeFormat} from 'd3-time-format';
    import {format, precisionFixed} from 'd3-format';
    import {max} from 'd3-array';
    import IconButton from '@smui/icon-button';
    import SegmentedButton, {Segment} from '@smui/segmented-button';
    import {Label} from '@smui/common';

    import MultiArea from './MultiArea.svelte';
    import Line from './Line.svelte';
    import Multiline from './Multiline.svelte';
    import AxisX from './AxisX.svelte';
    import AxisY from './AxisY.svelte';
    import SharedTooltip from './SharedTooltip.svelte';
    import {transformSummary, generateColorMap, transformAspectSummary} from '../utils/dataTransformer';
    import type {ReviewsSummaryDataPoint, ReviewsSummaryV2, AspectsSummary} from '../client';
    import type {Source} from '../client';
    import FormField from '@smui/form-field';
    import ChartSettingsGroup from './ChartSettingsGroup.svelte';
    import Brush from './Brush.svelte';
    import {timeDay, timeWeek, timeMonth, timeYear} from "d3-time";
    import SyncedBrush from "./SyncedBrush.svelte";

    export let data: {
        sources: Map<number, Source>,
        reviewSummary: ReviewsSummaryV2,
        aspectSummary: AspectsSummary
    };
    let categoryDatasets = [];
    const sources = data.sources;
    const sourceNameMap = new Map<string, number>();
    sources.forEach((s, id) => sourceNameMap.set(s.name, id));
    const summary = data.reviewSummary;

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
    const defaultTypeSelection = [...defaultSentimentSelection, ...defaultCategorySelection, ...defaultReviewTypeSelection];
    let selectedTypes: string[] = [...defaultTypeSelection];

    const onLast = (last, list) => [list[(list.indexOf(last) + 1) % list.length]]
    let sourceColorMap = new Map<string, string>(
        [
            ['steam', '#007bff'],
            ['epic', '#8400f5'],
            ['gog', '#00ff2a'],
            ['metacritic', '#ffdb00'],
            ['gamespot', '#ff0000']
        ]
    );
    const zColorMap = generateColorMap(sourceNames, typesNames, sourceColorMap, null);
    const rColorMap = new Map<string, string>([
            ['positive', '#00ff00'],
            ['negative', '#ff0000'],
            ['neutral', '#007bff']
        ]
    );

    //don't include rColorMap colors here
    const categoryColorMap = new Map<string, string>([
            ['gameplay', '#00ff00'],
            ['audio_visuals', '#ff0000'],
            ['performance_bugs', '#007bff'],
            ['overall', '#8400f5'],
            ['price', '#00ff2a'],
            ['community', '#ffdb00']
        ]
    );

    const parseDate = timeParse("%Y-%m-%dT%H:%M:%S%Z");
    const timeBuckets = ['day', 'week', 'month', 'year'];
    const mapTimeBucketToTime = {
        day: timeDay,
        week: timeWeek,
        month: timeMonth,
        year: timeYear
    };
    let selectedTimeBucket: string = 'week';

    const countNames = sourceNames.flatMap(source => typesNames.map(type => `${source}_${type}`));
    let flatData;
    let brushedData;
    let brushExtents = [null, null]
    let brushedExtentsCategory = [null, null]
    let groupedData;
    let groupedBrushedData;
    let selectedCounts: string[] = [];
    let yDomainMax = 10;

    $: {
        categoryDatasets = transformAspectSummary(data.aspectSummary.dates, mapTimeBucketToTime[selectedTimeBucket]);
    }

    $: {
        selectedTypes = [...selectedSentiments, ...selectedReviewTypes];
        selectedCounts = [...selectedSources.flatMap(source => selectedTypes.map(type => `${source}_${type}`))];
        if (selectedCounts.length === 0) {
            selectedCounts = ["all_total"]
        }
        flatData = transformSummary(summary, selectedSources, selectedTypes, sourceNameMap, mapTimeBucketToTime[selectedTimeBucket]);
        yDomainMax = 5;
        flatData.forEach(d => {
            d[xKey] = typeof d[xKey] === 'string' ? parseDate(d[xKey]) : d[xKey];
            selectedCounts.forEach(name => {
                d[name] = +d[name] || 0;
                if (d[name] > yDomainMax) {
                    yDomainMax = d[name];
                }
            });
        });

        groupedData = groupLonger(flatData, selectedCounts, {
            groupTo: zKey,
            valueTo: yKey,
        });
    }
    $: {
        brushedData = flatData.slice((brushExtents[0] || 0) * flatData.length, (brushExtents[1] || 1) * flatData.length);
        if (brushedData.length < 2) {
            brushedData = flatData.slice(brushExtents[0] * flatData.length, brushExtents[0] * flatData.length + 2)
        }

        groupedBrushedData = groupLonger(brushedData, selectedCounts, {
            groupTo: zKey,
            valueTo: yKey,
        });
    }

    const formatTickX = timeFormat('%b. %e, %Y');
    const formatTickY = d => {
        // format 1000 to 1K and 1000000 to 1M
        const formatter = format(`.${d}~s`);
        return formatter(d);
    };

     function sortResult(result) {
        if (Object.keys(result).length === 0) return [];

        const rows = Object.keys(result)
            .filter(d => d !== xKey)
            .map(key => {
                const [source, type] = key.split('_');
                return {
                    source,
                    type,
                    value: result[key]
                };
            })
            .reduce((acc, row) => {
                if (!acc[row.source]) {
                    acc[row.source] = {
                        source: row.source,
                        types: []
                    };
                }
                acc[row.source].types.push({type: row.type, value: row.value});
                return acc;
            }, {});

        const sortedRows = Object.values(rows).sort((a, b) => {
            return b.types.reduce((total, row) => total + row.value, 0) - a.types.reduce((total, row) => total + row.value, 0);
        });

        return sortedRows;
    }

</script>

<div class='stats-container'>
    <div class='chart-settings'>
        <IconButton class="material-icons" on:click={() => {}}>
            tune
        </IconButton>
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
    <div class="chart-container">
        <div class="zoom-settings">
            <SegmentedButton segments={timeBuckets} let:segment singleSelect bind:selected={selectedTimeBucket}>
                <Segment {segment}>
                    <Label>{segment}</Label>
                </Segment>
            </SegmentedButton>
        </div>
        <div class='chart'>
            {#if groupedData && groupedData.length > 0}
                <LayerCake
                        padding={20}
                        ssr={true}
                        percentRange={true}
                        x={xKey}
                        y={yKey}
                        z={zKey}
                        r={zKey}
                        yDomain={[0, yDomainMax]}
                        zScale={scaleOrdinal()}
                        zDomain={selectedCounts}
                        zRange={selectedCounts.map(name => zColorMap.get(name))}
                        rDomain={selectedTypes}
                        rScale={scaleOrdinal()}
                        rRange={selectedTypes.map(type => rColorMap.get(type))}
                        flatData={brushedData}
                        data={groupedBrushedData}
                >
                    <ScaledSvg>
                        <Multiline/>
                        <MultiArea/>
                    </ScaledSvg>

                    <Html>
                    <AxisX
                            ticks={10}
                            gridlines={false}
                            formatTick={formatTickX}
                            snapTicks={true}
                            tickMarks={true}
                    />
                    <AxisY
                            ticks={4}
                            formatTick={formatTickY}
                    />
                    <SharedTooltip
                            sortResult={sortResult}
                            formatTitle={timeFormat('%b. %e, %Y')}
                            dataset={brushedData}
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
        <div class="brush-container">
            <LayerCake
                    ssr={true}
                    percentRange={true}
                    x={xKey}
                    y={yKey}
                    z={zKey}
                    r={zKey}
                    yDomain={[0, yDomainMax]}
                    zScale={scaleOrdinal()}
                    zDomain={selectedCounts}
                    zRange={selectedCounts.map(name => zColorMap.get(name))}
                    rDomain={selectedTypes}
                    rScale={scaleOrdinal()}
                    rRange={selectedTypes.map(type => rColorMap.get(type))}
                    flatData={flatData}
                    data={groupedData}
            >
                <ScaledSvg>
                    <Multiline opacity={0.9}/>
                    <MultiArea opacity={0.9}/>
                </ScaledSvg>
                <Html>
                <Brush bind:min={brushExtents[0]} bind:max={brushExtents[1]}/>
                </Html>
            </LayerCake>
        </div>
        <div class="synced-brush-container">
            {#each Object.entries(categoryDatasets).filter(d => selectedCategories.includes(d[0])) as [category, dataset]}
                <SyncedBrush
                        data={dataset}
                        bind:selectedPolarities={selectedSentiments}
                        xKey="date"
                        yKey="count"
                        zKey="polarity"
                        rKey="polarity"
                        zColorMap={rColorMap}
                        formatTickX={formatTickX}
                        formatTickY={formatTickY}
                        chartTitle={category}
                        bind:min={brushedExtentsCategory[0]}
                        bind:max={brushedExtentsCategory[1]}
                        stroke={categoryColorMap.get(category)}>
                </SyncedBrush>
            {/each}
        </div>
    </div>

</div>


<style>
    /*
      The wrapper div needs to have an explicit width and height in CSS.
      It can also be a flexbox child or CSS grid element.
      The point being it needs dimensions since the <LayerCake> element will
      expand to fill it.
    */
    .stats-container {
        display: flex;
        width: 100%;
        height: 100%;
        flex-direction: row;
    }

    .chart-container {
        display: flex;
        width: 100%;
        flex-direction: column;
        padding: 1rem;
    }

    .chart-settings {
        display: flex;
        flex-direction: column;
        padding: 1rem;
    }

    .zoom-settings {
        display: flex;
        flex-direction: row;
        padding: 1rem;
    }

    .chart {
        padding: 1rem;
        height: 300px;
    }

    .brush-container {
        padding: 1rem;
        height: 50px;
    }

    .synced-brush-container {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 1rem;
        padding: 1rem;
        width: 100%;
    }

</style>