<script>
  import { LayerCake, ScaledSvg, Html, flatten } from 'layercake';
  import { scaleOrdinal } from 'd3-scale';
  import { timeParse, timeFormat } from 'd3-time-format';
  import { format, precisionFixed } from 'd3-format';

  import MultiLine from './AreaStacked.svelte';
  import AxisX from './AxisX.svelte';
  import AxisY from './AxisY.svelte';
  import GroupLabels from './GroupLabels.svelte';
  import SharedTooltip from './SharedTooltip.svelte';

  export let data;

  const xKey = 'date';
  const yKey = 'total';
  const zKey = 'source_id';

  const seriesNames = Object.keys(data[0]).filter(d => d !== xKey);
  const seriesColors = ['#ffe4b8', '#ffb3c0', '#ff7ac7', '#ff00cc'];

  const parseDate = timeParse("%Y-%m-%dT%H:%M:%S%Z");

  /* --------------------------------------------
   * Create a "long" format that is a grouped series of data points
   * Layer Cake uses this data structure and the key names
   * set in xKey, yKey and zKey to map your data into each scale.
   */
  const dataLong = seriesNames.map(key => {
    return {
      [zKey]: key,
      values: data.map(d => {
        // Put this in a conditional so that we don't recast the data on second render
        d[xKey] = typeof d[xKey] === 'string' ? parseDate(d[xKey]) : d[xKey];
        return {
          [yKey]: +d[key],
          [xKey]: d[xKey]
        };
      })
    };
  });
  console.log(JSON.stringify(dataLong));
  const formatTickX = timeFormat('%b. %e');
  const formatTickY = d => format(`.${precisionFixed(d)}s`)(d);
</script>

<style>
  /*
    The wrapper div needs to have an explicit width and height in CSS.
    It can also be a flexbox child or CSS grid element.
    The point being it needs dimensions since the <LayerCake> element will
    expand to fill it.
  */
  .chart-container {
    width: 100%;
    height: 100%;
  }
</style>

<div class="chart-container">
  <LayerCake
    ssr={true}
    percentRange={true}
    padding={{ top: 7, right: 10, bottom: 20, left: 25 }}
    x={xKey}
    y={yKey}
    z={zKey}
    zScale={scaleOrdinal()}
    zRange={seriesColors}
    flatData={flatten(dataLong, 'values')}
    yDomain={[0, null]}
    data={dataLong}
  >
    <ScaledSvg>
       <AxisX
        gridlines={false}
        ticks={data.map(d => d[xKey]).sort((a, b) => a - b)}
        formatTick={formatTickX}
        snapTicks={true}
        tickMarks={true}
      />
      <AxisY
        baseline={true}
        formatTick={formatTickY}
      />
    </ScaledSvg>

    <Html>
      <GroupLabels/>
      <SharedTooltip
        formatTitle={formatTickX}
        dataset={data}
      />
    </Html>
  </LayerCake>
</div>