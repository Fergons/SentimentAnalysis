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

    import MultiArea from './MultiArea.svelte';
    import Line from './Line.svelte';
    import Multiline from './Multiline.svelte';
    import AxisX from './AxisX.svelte';
    import AxisY from './AxisY.svelte';
    import SharedTooltip from './SharedTooltip.svelte';
    import {transformSummary, generateColorMap} from '../utils/dataTransformer';
    import type {ReviewsSummaryDataPoint, ReviewsSummaryV2} from '../client';
    import type {Source} from '../client';
    import FormField from '@smui/form-field';
    import ChartSettingsGroup from './ChartSettingsGroup.svelte';
    import Brush from './Brush.svelte';
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

    const zColorMap = generateColorMap(sourceNames, typesNames);
    const rColorMap = new Map<string, string>([
            ['positive', '#00b300'],
            ['negative', '#ff0000'],
            ['neutral', '#007bff']
        ]
    );

    const onLast = (last, list) => [list[(list.indexOf(last) + 1) % list.length]]


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
    let brushedData;
    let brushExtents = [0, 0]
    let groupedData;
    let groupedBrushedData;
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

    const formatTickX = timeFormat('%b. %e');
    const formatTickY = d => {
        // format 1000 to 1K and 1000000 to 1M
        const formatter = format(`.${d}~s`);
        return formatter(d);
    };

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
                            gridlines={false}
                            ticks={brushedData.filter(d => Object.keys(d).some(key => key !== xKey && d[key] !== 0))
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
                    x={xKey}
                    y={yKey}
                    z={zKey}
                    r={zKey}
                    xNice={true}
                    yNice={true}
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
                <Svg>
                    <Multiline/>
                    <MultiArea/>
                </Svg>
                <Html>
                <Brush bind:min={brushExtents[0]} bind:max={brushExtents[1]}/>
                </Html>
            </LayerCake>
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
    .chart {
        padding: 1rem;
        height: 300px;
    }
    .brush-container {
        padding: 1rem;
        height: 50px;
    }

</style>