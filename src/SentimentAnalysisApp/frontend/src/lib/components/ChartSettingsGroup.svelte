<script lang="ts">

    import FormField from "@smui/form-field";
    import CheckBox from "@smui/checkbox";
    import Button from "@smui/button";

    export let seriesNames: string[];
    export let selectedSeries: string[];
    export let onReset = () => {
    };
    export let onLast = () => {
    };

</script>

<div class="chart-settings-group">
    {#each seriesNames as name}
        <div class="checkbox-container">
            <FormField>
                <CheckBox
                        bind:group={selectedSeries}
                        value={name}
                        on:change={(last)=>{selectedSeries.length === 0? onLast(last.srcElement.value):()=>{}}}
                />
                <span slot="label">{name}</span>
            </FormField>
        </div>
    {/each}
    <div class="buttons-container">
        <Button size="mini" on:click={onReset}>Reset</Button>
        <Button size="mini" on:click={()=>selectedSeries = [...seriesNames]}>All</Button>
    </div>
</div>

<style>
    .chart-settings-group {
        display: flex;
        flex-direction: column;
        padding: 1rem;
    }

    .checkbox-container {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .buttons-container {
        display: flex;
    }


</style>