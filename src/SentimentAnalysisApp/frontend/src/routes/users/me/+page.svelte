<script lang="ts">
    import {makeDefaultTextfieldInputState} from "../../../lib/utils/inputState";
    import FormField from '@smui/form-field';
    import Textfield from '@smui/textfield';
    import Switch from '@smui/switch';
    import {enhance} from '$app/forms'
    import {Icon} from "@smui/common";
    import {page} from '$app/stores';
    import Paper from "@smui/paper";
    import {User} from "../../../lib/server/api/types";
    import {PageData} from "./$types";


    export let data: PageData;

    let email = makeDefaultTextfieldInputState();
    $: data.user.email = email.value;
    let password = makeDefaultTextfieldInputState()
    let edit = false;
</script>

<section>
    <div class="account-me-container">
        <Paper>
            <FormField>
                <Switch bind:checked={edit}

                />

                <span slot="label">
            Edit
        </span>
            </FormField>
            <form method="POST" use:enhance>
                <Textfield
                        bind:value={email.value}
                        bind:invalid={email.invalid}
                        bind:dirty={email.dirty}
                        style="width: 100%;"
                        disabled={!edit}
                >
                    <svelte:fragment slot="label">
                        <Icon class="material-icons"
                              style="font-size: 1em; line-height: normal; vertical-align: top;"
                        >
                            email
                        </Icon>
                        Email
                    </svelte:fragment>
                </Textfield>
            </form>
        </Paper>
    </div>

</section>

<style>
    .account-me-container {
        display: flex;
        justify-content: center;
        flex-direction: column;
    }

</style>