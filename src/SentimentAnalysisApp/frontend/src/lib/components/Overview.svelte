<script lang="ts">
    import {LayerCake, Svg} from 'layercake';
    import {scaleLinear} from 'd3-scale';

    import RadarChart from "./RadarChart.svelte";
    import AxisRadial from './AxisRadial.svelte';

    export let data;
    const seriesKey = 'game_id';
    const xKey = ['gameplay', 'performance_bugs', 'price', 'audio_visuals', 'community', 'story'];

    const seriesNames =  Object.keys(data[0]).filter(d => d !== seriesKey);
    data.forEach(d => {
		seriesNames.forEach(name => {
			d[name] = +d[name];
		});
	});

    let activeCategory = 0;
    function setActiveCategory(event) {
        activeCategory = event.detail.category
        console.log("activeCategory: ", activeCategory)
    }

</script>


<div class="chart-container">
    <LayerCake
            ssr={true}
            percentageRange={true}
            padding={{ top: 16, right: 16, bottom: 16, left: 16 }}
            x={xKey}
            xDomain={[0, 10]}
            xRange={({ height }) => [0, height / 2.3]}
            data={data}
    >
        <Svg>
            <AxisRadial textColor="#fff" textFont="roboto-mono" on:categorySelected={setActiveCategory}/>
            <RadarChart/>
        </Svg>
    </LayerCake>
</div>


<style>
    .chart-container {
        width: 40%;
        height: 100%;
    }
</style>





