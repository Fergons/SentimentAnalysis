<!--
    Modified component from Layer Cake (https://layercake.graphics/example)
	@component
	Generates an SVG area shape using the `area` function from [d3-shape](https://github.com/d3/d3-shape).
 -->
<script>
	import { getContext } from 'svelte';

	const { data, xGet, yGet, rGet, xScale, yScale, extents } = getContext('LayerCake');
    export let opacity = 0.5;
    $: path = values => { return 'M' + values
		.map(d => $xGet(d) + ',' + $yGet(d))
		.join('L');
    }

</script>

<g class="line-group">
  {#each $data as group}
    <path
      class="path-line"
      d="{path(group.values)}"
      stroke="{$rGet(group)}"
      opacity="{opacity}"
    ></path>
  {/each}
</g>

<style>
	.path-line {
		fill: none;
		stroke-linejoin: round;
		stroke-linecap: round;
		stroke-width: 3px;
	}
</style>