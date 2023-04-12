<!--
	@component
	Generates an SVG area shape using the `area` function from [d3-shape](https://github.com/d3/d3-shape).
 -->
<script>
	import { getContext } from 'svelte';

	const { data, xGet, yGet, rGet, xScale, yScale, extents } = getContext('LayerCake');

	/**	@type {String} [fill='#ab00d610'] The shape's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
	export let fill = '#ab00d610';
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
      opacity="0.5"
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