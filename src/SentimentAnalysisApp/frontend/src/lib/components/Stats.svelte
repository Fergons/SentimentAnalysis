<script>
    import {LayerCake, Svg, Html, flatten, groupLonger, ScaledSvg} from 'layercake';
    import {scaleOrdinal} from 'd3-scale';
    import {stack} from 'd3-shape';
    import {timeParse, timeFormat} from 'd3-time-format';
    import {format, precisionFixed} from 'd3-format';


    import Multiline from './Multiline.svelte';
    import AxisX from './AxisX.svelte';
    import AxisY from './AxisY.svelte';
    import GroupLabels from './GroupLabels.svelte';
    import SharedTooltip from './SharedTooltip.svelte';

    export let data;

    const xKey = 'date';
    const yKey = 'total';
    const zKey = 'source';

    const seriesNames = Object.keys(data[0]).filter(key => key !== xKey);
    const seriesColors = ['#ffe4b8', '#ffb3c0', '#ff7ac7', '#ff00cc'];

    const parseDate = timeParse("%Y-%m-%dT%H:%M:%S%Z");

    data.forEach(d => {
        d[xKey] = typeof d[xKey] === 'string'
            ? parseDate(d[xKey])
            : d[xKey];

        seriesNames.forEach(name => {
            d[name] = +d[name];
        });
    });

    const groupedData = groupLonger(data, seriesNames, {
        groupTo: zKey,
        valueTo: yKey
    });

    const formatTickX = timeFormat('%b. %e');
    const formatTickY = d => format(`.${precisionFixed(d)}`)(d);
</script>


<div class="chart-container">
    <LayerCake
            ssr={true}
            percentRange={true}
            x={xKey}
            y={yKey}
            z={zKey}
            zScale={scaleOrdinal()}
            zDomain={seriesNames}
            zRange={seriesColors}
            flatData={flatten(groupedData, 'values')}
            yDomain={[0, 4]}
            data={groupedData}
    >
        <ScaledSvg>

            <Multiline/>
        </ScaledSvg>

        <Html>
         <AxisX
                    gridlines={false}
                    ticks={data.map(d => d[xKey]).sort((a, b) => a - b)}
                    formatTick={formatTickX}
                    snapTicks={true}
                    tickMarks={true}
            />
            <AxisY
                    formatTick={formatTickY}
            />
        <SharedTooltip
                formatTitle={formatTickX}
                dataset={data}
        />
        </Html>
    </LayerCake>
</div>

<style>
    /*
      The wrapper div needs to have an explicit width and height in CSS.
      It can also be a flexbox child or CSS grid element.
      The point being it needs dimensions since the <LayerCake> element will
      expand to fill it.
    */
    .chart-container {
        width: 60%;
        height: 60%;
    }
</style>