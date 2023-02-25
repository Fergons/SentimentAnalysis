<!--
  @component
  Generates an SVG radial scale, useful for radar charts.
 -->
<script>
    import {getContext} from 'svelte';
    import {createEventDispatcher} from 'svelte';

    const dispatch = createEventDispatcher();

    const {width, height, xScale, extents, config} = getContext('LayerCake');

    /** @type {Number} [lineLengthFactor=1.1] - How far to extend the lines from the circle's center. A value of `1` puts them at the circle's circumference. */
    export let lineLengthFactor = 1.1;

    /** @type {Number} [labelPlacementFactor=1.25] - How far to place the labels from the circle's center. A value of `1` puts them at the circle's circumference. */
    export let labelPlacementFactor = 1.25;

    /** @type {String} [textColor='#8c8c8c'] - Color of the labels.*/
    export let textColor = '#fff';

    /** @type {String} [labelBackgroundColor='#0363f0'] - Color of the labels.*/
    export let labelBackgroundColor = '#0363f0';

    /** @type {Number} [textSize=18] - Font size of the labels.*/
    export let textSize = 18;

    /** @type {String} [textFont='roboto'] - Font of the labels.*/
    export let textFont = 'roboto';

    $: max = $xScale(Math.max(...$extents.x));

    $: lineLength = max * lineLengthFactor;
    $: labelPlacement = max * labelPlacementFactor;

    $: angleSlice = (Math.PI * 2) / $config.x.length;

    let activeCategory = 0;

    function anchor(total, i) {
        if (i === 0 || i === total / 2) {
            return 'middle';
        } else if (i < total / 2) {
            return 'start';
        }
        return 'end';
    }

    console.log($config);
</script>
<defs>
    <filter id="rounded-corners" x="-5%" width="110%" y="0%" height="100%">
        <feFlood flood-color="{labelBackgroundColor}"></feFlood>
        <feComposite operator="over" in="SourceGraphic"></feComposite>
    </filter>
</defs>
<g
        transform="translate({ $width / 2 }, { $height / 2 })"
>
    <circle
            cx="0"
            cy="0"
            r="{max}"
            stroke="#ccc"
            stroke-width="1"
            fill="#CDCDCD"
            fill-opacity="0.1"
    ></circle>
    <circle
            cx="0"
            cy="0"
            r="{max / 2}"
            stroke="#ccc"
            stroke-width="1"
            fill="none"
    ></circle>

    {#each $config.x as label, i}
        {@const thisAngleSlice = angleSlice * i - Math.PI / 2}
        <line
                x1="0"
                y1="0"
                x2="{lineLength * Math.cos(thisAngleSlice)}"
                y2="{lineLength * Math.sin(thisAngleSlice)}"
                stroke="#ccc"
                stroke-width="1"
                fill="none"
        >
        </line>
        <text
                text-anchor="{anchor($config.x.length, i)}"
                dy="0.35em"
                font-family="{textFont}"
                font-size="{textSize}px"
                fill="{textColor}"
                class:active={i === activeCategory}
                on:click={() => {
                    console.log(`clicked on ${label}`);
                    activeCategory = i;
                    dispatch('categorySelected', {category: i});
                }}
                on:focus={() => {
                    console.log(`focused on ${label}`);
                    activeCategory = i;
                    dispatch('categorySelected', {category: i});
                }}
                tabindex="0"
                transform="translate({(labelPlacement) * Math.cos(thisAngleSlice)}, {labelPlacement * Math.sin(thisAngleSlice)})"
        >
            {label}
        </text>
    {/each}
</g>

<style>
    text {
        cursor: pointer;
    }

    text.active {
        font-weight: bold;
    }
</style>