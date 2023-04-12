<script lang="ts">

    import FormField from "@smui/form-field";
    import Switch from "@smui/switch";
    import IconButton from "@smui/icon-button";

    export let seriesNames: string[];
    export let selectedSeries: string[];
    export let onReset = () => {
    };
    export let onLast = () => {
    };

    export let rollout = false;

</script>

<div class="chart-settings-group">
    <div class="options-container">
        {#each seriesNames as name}
            <div class="option-container">
                <FormField>
                    <Switch
                            bind:group={selectedSeries}
                            value={name}
                            on:change={(last)=>{selectedSeries.length === 0? onLast(last.srcElement.value):()=>{}}}
                    />
                    <span slot="label">{name}</span>
                </FormField>
            </div>
        {/each}
    </div>
    <div class="buttons-container">
        {#if seriesNames.length > 1}
            <IconButton class="material-icons" on:click={()=>selectedSeries = []}>
                delete_sweep
            </IconButton>
            <IconButton class="material-icons" on:click={()=>selectedSeries = [...seriesNames]}>
                done_all
            </IconButton>
        {/if}
    </div>
</div>

<style>
    .chart-settings-group {
        display: flex;
        flex-direction: column;
        padding: 1rem;
    }
    .option-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 0.5rem;
    }
    .buttons-container {
        display: flex;
        flex-direction: row;
        padding-left: 0.5rem;
    }


</style>