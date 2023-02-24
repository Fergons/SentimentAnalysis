<script lang="ts">
    import {LayerCake, Svg} from 'layercake';
    import {scaleLinear} from 'd3-scale';

    import RadarChart from "./RadarChart.svelte";
    import AxisRadial from './AxisRadial.svelte';

    export let data;
    const seriesKey = 'name';
    const xKey = ['gameplay', 'performance_bugs', 'price', 'audio_visuals', 'community', 'story'];

    const seriesNames = ['gameplay', 'price', 'story', 'performance_bugs', 'audio_visuals', 'community'];
    const data1 = [Object.fromEntries(data)];
    console.log(data1);

    let activeCategory = 0;
    function setActiveCategory(event) {
        activeCategory = event.detail.category
        console.log("activeCategory: ", activeCategory)
    }

</script>


<div class="chart-container">
    <LayerCake
            padding={{ top: 30, right: 0, bottom: 7, left: 0 }}
            x={xKey}
            xDomain={[0, 10]}
            xRange={({ height }) => [0, height / 2]}
            data={data1}
    >
        <Svg>
            <AxisRadial textColor="#fff" textFont="roboto-mono" on:categorySelected={setActiveCategory}/>
            <RadarChart/>
        </Svg>
    </LayerCake>
</div>


<style>
    .chart-container {
        padding: 16px;
        width: 30%;
        height: 80%;
    }
</style>





