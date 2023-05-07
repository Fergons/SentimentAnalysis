<!--
  Modified component from Layer Cake (https://layercake.graphics/example)
  @component
  Generates a radar chart used for category comparison.
-->
<script lang="ts">
    import {getContext} from 'svelte';
    import {line, curveCardinalClosed} from 'd3-shape';

    const {data, width, height, xGet, config} = getContext('LayerCake');

    /**  @type {String} [fill='#0363f0'] The radar's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
    export let fill = '#0363f0'

    /**  @type {String} [stroke='#0363f0'] The radar's stroke color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
    export let stroke = '#0363f0'

    /**  @type {Number} [stroke=2] The radar's stroke color. */
    export let strokeWidth = 2

    /**  @type {Number} [fillOpacity=0.5] The radar's fill opacity. */
    export let fillOpacity = 0.5

    /**  @type {Number} [r=4.5] Each circle's radius. */
    export let r = 4.5;

    /**  @type {String} [circleFill="#0363f0"] Each circle's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
    export let circleFill = "#0363f0";

    /**  @type {String} [circleStroke="#fff"] Each circle's stroke color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
    export let circleStroke = "#fff";

    /**  @type {Number} [circleStrokeWidth=1] Each circle's stroke width. */
    export let circleStrokeWidth = 1;

    $: angleSlice = (Math.PI * 2) / $config.x.length;

    $: path = line()
        .curve(curveCardinalClosed)
        .x((d, i) => d * Math.cos(angleSlice * i - Math.PI / 2))
        .y((d, i) => d * Math.sin(angleSlice * i - Math.PI / 2));

</script>

<g
        transform="translate({ $width / 2 }, { $height / 2 })"
>
    {#each $data as row}
        {@const xVals = $xGet(row)}
        <!-- Draw a line connecting all the dots -->
        <path
                class='path-line'
                d='{path(xVals)}'
                stroke="{stroke}"
                stroke-width="{strokeWidth}"
                fill="{fill}"
                fill-opacity="{fillOpacity}"
        ></path>

        <!-- Plot each dots -->
        {#each xVals as circleR, i}
            {@const thisAngleSlice = angleSlice * i - Math.PI / 2}
            <circle
                    cx={circleR * Math.cos(thisAngleSlice)}
                    cy={circleR * Math.sin(thisAngleSlice)}
                    r="{r}"
                    fill="{circleFill}"
                    stroke="{circleStroke}"
                    stroke-width="{circleStrokeWidth}"
            ></circle>
        {/each}
    {/each}
</g>

<style>
    .path-line {
        stroke-linejoin: round;
        stroke-linecap: round;
    }
</style>


