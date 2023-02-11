<script lang="ts">
    import {makeDefaultTextfieldInputState} from "../../../lib/utils/inputState";
    import FormField from '@smui/form-field';
    import Textfield from '@smui/textfield';
    import Switch from '@smui/switch';
    import {enhance} from '$app/forms'
    import {Icon} from "@smui/common";
    import Paper from "@smui/paper";
    import userStore from "../../../lib/stores/user";
    import type {PageServerData} from "./$types";

    export let data: PageServerData;
    $userStore = data?.user ?? null
    let email = makeDefaultTextfieldInputState($userStore?.email ?? null);
    let password = makeDefaultTextfieldInputState()
    let edit = false;
</script>

<section>
    <div class="account-me-container">
        <Paper>
            <FormField>
                <Switch bind:checked={edit}/>
                <span slot="label">Edit
                </span>
            </FormField>
            <form method="POST"
                  use:enhance={() => {
                      return async ({ result, update }) => {
                            edit=false;
                            if (result.type === 'success' && !result.data.errors) {
                                await userStore.update(user => {
                                    user = result.data
                                    return user
                                })
                                await update();
                            }
                            email.value = $userStore?.email ?? null


                      }
            }
            }>
                <Textfield
                        bind:value={email.value}
                        bind:invalid={email.invalid}
                        updateInvalid
                        style="width: 100%;"
                        disabled={!edit}
                        input$name="email"
                        input$type="email"
                        input$required
                        input$title="Please enter a valid email address"
                        input$pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{'{2,4}'}$"
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
        width: 60%;
    }

</style>