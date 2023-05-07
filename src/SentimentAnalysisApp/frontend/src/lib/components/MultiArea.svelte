<!--
  Modified component from Layer Cake (https://layercake.graphics/example)
  @component
  Generates an SVG multi-series area chart. It expects your data to be an array of objects, each with a `values` key that is an array of data objects.
 -->
<script>
  import { getContext } from 'svelte';

  const { data, xGet, yGet, zGet, xScale, yScale, extents } = getContext('LayerCake');
  export let opacity = 0.5;
  $: areaPath = values => {
    const areaPoints = values.map(d => {
      return $xGet(d) + ',' + $yGet(d);
    });
    const yRange = $yScale.range()[0] // Calculate the y-coordinate for the bottom of the area
    return (
      "M" +
      $xScale($extents.x ? $extents.x[0] : 0) +
      "," +
      yRange +
      "L" +
      areaPoints.join("L") +
      "L" +
      $xScale($extents.x ? $extents.x[1] : 0) +
      "," +
      yRange +
      "Z"
    );
  };
</script>

<g class="area-group">
  {#each $data as group}
    <path
      class="path-area"
      d="{areaPath(group.values)}"
      fill="{$zGet(group)}"
      opacity="0.1"
    ></path>
  {/each}
</g>

<style>
  .path-area {
    stroke-linejoin: round;
    stroke-linecap: round;
  }
</style>