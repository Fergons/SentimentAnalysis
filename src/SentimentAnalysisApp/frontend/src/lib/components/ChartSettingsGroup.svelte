<script lang="ts">

    import FormField from "@smui/form-field";
    import Switch from "@smui/switch";
    import IconButton from "@smui/icon-button";
    import {LayerCake} from "layercake";
    import List, {Subheader, Item} from "@smui/list";

    export let subHeader = "Series";
    export let seriesNames: string[];
    export let selectedSeries: string[];
    export let onReset = () => {
    };
    export let onLast = () => {
    };

    export let rollout = false;

</script>

<List>
    <Subheader style="color: #5f768c">{subHeader}</Subheader>
    <div class="chart-settings-group">
        <div class="options-container">
            {#each seriesNames as name}
                <Item>
                        <FormField align="end" style="width: 100%; margin-right: auto; margin-left: 0">
                        <span slot="label" style="text-transform: capitalize;">{name.replace("_", " & ")}</span>
                            <Switch
                                    bind:group={selectedSeries}
                                    value={name}
                                    on:change={(last)=>{selectedSeries.length === 0? onLast(last.srcElement.value):()=>{}}}
                            />
                        </FormField>
                </Item>
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
</List>

<style>
    .chart-settings-group {
        display: flex;
        flex-direction: column;
        padding-bottom: 2rem;
        padding-left: 0.5rem;
    }

    .buttons-container {
        display: flex;
        flex-direction: row;
        padding-left: 0.5rem;
    }


    :global(.mdc-form-field--align-end>label) {
        margin-right: auto;
        margin-left: 0;
    }


</style>