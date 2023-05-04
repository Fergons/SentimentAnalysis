<script>
    import {LayerCake, Html, groupLonger, ScaledSvg} from 'layercake';

    import Multiline from './Multiline.svelte';
    import AxisX from './AxisX.svelte';
    import AxisY from './AxisY.svelte';
    import Brush from './Brush.svelte';
    import MultiArea from "./MultiArea.svelte";
    import {scaleOrdinal} from "d3-scale";
    import {timeFormat} from "d3-time-format";
    import SharedTooltip from "$lib/components/SharedTooltipPolarities.svelte";

    export let min = null;
    export let max = null;
    export let xKey = 'x';
    export let yKey = 'y';
    export let rKey = 'r';
    export let zKey = 'z';
    export let zColorMap = new Map([
        ['positive', '#00e047'],
        ['negative', '#ff0000'],
        ['neutral', '#0000ff'],
    ]);
    export let data = [];
    export let stroke = '#00e047';

    export let chartTitle = '';

    export let selectedPolarities = ['positive', 'negative', 'neutral'];
    export let formatTickX = (d) => d;
    export let formatTickY = (d) => d;


    let brushedData;
    let groupedData;
    // not altered range for brush view
    let brushGroupedData;
    let yDomainMax = 5;
    $: {
        yDomainMax=5;
        data.forEach(
            d => {
                d[xKey] = new Date(d[xKey]);
                d['positive'] = +d['positive'];
                d['negative'] = +d['negative'];
                d['neutral'] = +d['neutral'];
                yDomainMax = Math.max(yDomainMax, d['positive'], d['negative'], d['neutral']);
            }
        )
        brushedData = data.slice((min || 0) * data.length, (max || 1) * data.length);
        if (brushedData.length < 2) {
            brushedData = data.slice(min * data.length, min * data.length + 2)
        }

        groupedData = groupLonger(brushedData, selectedPolarities, {
            groupTo: zKey,
            valueTo: yKey,
        });
        // brush not altered range
        brushGroupedData = groupLonger(data, selectedPolarities, {
            groupTo: zKey,
            valueTo: yKey,
        });
    }
</script>

<div class="chart-wrapper">
    <span style="padding-bottom: 1rem; text-transform: capitalize" class="mdc-typography--headline5">{chartTitle.split("_").join(" & ")}</span>
    <div class="chart-container">
        <LayerCake
                ssr={true}
                percentRange={true}
                x={xKey}
                y={yKey}
                r={rKey}
                z={zKey}
                yDomain={[0, yDomainMax]}
                rScale={scaleOrdinal()}
                rDomain={selectedPolarities}
                rRange={selectedPolarities.map(name => zColorMap.get(name))}
                zScale={scaleOrdinal()}
                zDomain={selectedPolarities}
                zRange={selectedPolarities.map(name => zColorMap.get(name))}
                flatData={brushedData}
                data={groupedData}
        >
            <ScaledSvg>
                <Multiline/>
                <MultiArea/>
            </ScaledSvg>
            <Html>
            <AxisX
                    ticks={2}
                    gridlines={false}
                    formatTick={formatTickX}
                    snapTicks={true}
                    tickMarks={true}
            />
            <AxisY
                    ticks={2}
                    formatTick={formatTickY}
            />
            <SharedTooltip
                    formatTitle={timeFormat('%b. %e, %Y')}
                    dataset={brushedData}
            />
            </Html>
        </LayerCake>
    </div>

    <div class="brush-container">
        <LayerCake
                ssr={true}
                percentRange={true}
                padding={{ top: 5 }}
                x={xKey}
                y={yKey}
                r={rKey}
                z={zKey}
                rScale={scaleOrdinal()}
                rDomain={selectedPolarities}
                rRange={selectedPolarities.map(name => zColorMap.get(name))}
                zScale={scaleOrdinal()}
                zDomain={selectedPolarities}
                zRange={selectedPolarities.map(name => zColorMap.get(name))}
                yDomain={[0, yDomainMax]}
                flatData={data}
                data={brushGroupedData}
        >
            <ScaledSvg>
                <Multiline/>
                <MultiArea/>
            </ScaledSvg>
            <Html>
            <Brush bind:min={min}
                   bind:max={max}
            />
            </Html>
        </LayerCake>
    </div>
</div>

<style>
    .chart-wrapper {
        display: flex;
        flex-direction: column;
        width: 45%;
        height: 300px;
        gap: 1rem;
        margin-bottom: 4rem;
    }

    .chart-container {
        width: 100%;
        height: 80%;
    }

    .brush-container {
        width: 100%;
        height: 20%;
    }
</style>