<script lang="ts">
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
    import GroupLabels from './GroupLabels.svelte';
    import SharedTooltip from './SharedTooltip.svelte';
    import {getTotal} from "../utils/dataTransformer";
    import type {ReviewsSummaryDataPoint} from '../client';
    import type {Source} from '../client';
    import FormField from "@smui/form-field";

    export let data: {
        sources: Map<number, Source>,
        summary: ReviewsSummaryDataPoint[]
    };
    const sources = data.sources;
    const summary = data.summary;
    const total = getTotal(summary, sources, 30);

    const xKey = 'date';
    const yKey = 'total';
    const zKey = 'source';

    // if data is not undefined, then we have data
    const seriesNames: string[] = sources.size > 0 ? Array.from(sources.values()).map(s => s.name) : [];
    // colors in contrasting blue shades
    const seriesColors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78'];

    const parseDate = timeParse("%Y-%m-%dT%H:%M:%S%Z");

    if (total && total.length > 0) {
        total.forEach(d => {
            d[xKey] = typeof d[xKey] === 'string'
                ? parseDate(d[xKey])
                : d[xKey];

            seriesNames.forEach(name => {
                d[name] = +d[name];
            });
        });
    }

    let selectedSeries = [...seriesNames];
    let selectedYKey = yKey;

    let groupedData = [];
    $: if (selectedSeries.length > 0) {
        groupedData =  groupLonger(total, selectedSeries, {
            groupTo: zKey,
            valueTo: yKey
        });
    }

    const formatTickX = timeFormat('%b. %e');
    const formatTickY = d => {
        // format 1000 to 1K and 1000000 to 1M
        const formatter = format(`.${d}~s`);
        return formatter(d);
    };

</script>
<div class="chart-container">
    <div class="chart-settings">
        {#each seriesNames as name}
            <div class="checkbox-container">
                <FormField>
                    <Checkbox
                            bind:group={selectedSeries}
                            value={name}
                            disabled={selectedSeries.length === 1 && selectedSeries.includes(name)}
                    />
                    <span slot="label">{name}</span>
                </FormField>
            </div>
        {/each}
    </div>
    <div class="chart">
        {#if groupedData && groupedData.length > 0}
            <LayerCake
                    ssr={true}
                    percentRange={true}
                    x={xKey}
                    y={yKey}
                    z={zKey}
                    zScale={scaleOrdinal()}
                    xNice={true}
                    yNice={true}
                    yDomain={[0, 10]}
                    zDomain={seriesNames}
                    zRange={seriesColors}
                    flatData={flatten(groupedData, 'values')}
                    data={groupedData}
            >
                <ScaledSvg>
                    <Multiline/>
                </ScaledSvg>

                <Html>
                <AxisX
                        gridlines={false}
                        ticks={total.map(d => d[xKey]).sort((a, b) => a - b)}
                        formatTick={formatTickX}
                        snapTicks={true}
                        tickMarks={true}
                />
                <AxisY
                        formatTick={formatTickY}
                />
                <SharedTooltip
                        formatTitle={formatTickX}
                        dataset={total}
                />
                </Html>
            </LayerCake>
        {:else}
            <Svg>
                <text x="50%" y="50%" text-anchor="middle" dominant-baseline="central" font-size="24px">
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
        display: flex;
        flex-direction: column;
        position: relative;
         padding: 2rem;
    }

    .checkbox-container {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .checkbox-container label {
        margin-left: 0.5rem;
    }
</style>