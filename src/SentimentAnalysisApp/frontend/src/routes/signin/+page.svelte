<script lang="ts">
    import Textfield from '@smui/textfield';
    import HelperText from '@smui/textfield/helper-text';
    import Paper from '@smui/paper';
    import Button, {Label} from '@smui/button';
    import {Icon} from '@smui/common';
    import {enhance} from "$app/forms";
    import type {ActionData} from './$types';
    import type {TextfieldInputState} from "../../lib/utils/inputState";
    import {
        isTextfieldInputStateValid,
        makeDefaultTextfieldInputState,
    } from "../../lib/utils/inputState";

    let email = makeDefaultTextfieldInputState();
    let password = makeDefaultTextfieldInputState();

    $: disabled = !(isTextfieldInputStateValid(email) && isTextfieldInputStateValid(password));
    export let form: ActionData;
    const handleSubmit = () => {
        console.log("Submitted!")
    }
</script>

<section title="Sign In">
    <div class="signin-form-container form-container">
        <Paper style="width: 50%; min-width: 250px; align-items: center">
            <h1 class="mdc-typography--headline4" style="margin: 0 0 8px 0; text-align: center">Sign In</h1>
            <form method="post" class="signin-form form" use:enhance>
                <Textfield bind:value={email.value}
                           bind:invalid={email.invalid}

                           helperLine$style="width: 100%;"
                           updateInvalid
                           type="email"
                           input$name="email"
                           input$autocomplete="email"
                           class="signin-form-item"
                           required

                >

                    <svelte:fragment slot="label">
                        <Icon class="material-icons"
                              style="font-size: 1em; line-height: normal; vertical-align: top;"
                        >
                            email
                        </Icon>
                        Email
                    </svelte:fragment>
                    <HelperText validationMsg slot="helper" class="signin-form-item">
                        That's not a valid email address.
                    </HelperText>
                </Textfield>

                <Textfield
                        bind:value={password.value}
                        bind:invalid={password.invalid}
                        updateInvalid
                        type="password"
                        input$name="password"
                        label="Password"
                        class="signin-form-item"
                        required
                />
                <Button
                        type="submit"
                        class="signin-button signin-form-item"
                        variant="raised"
                        disabled={disabled}
                >Sign In
                </Button>
                <div class="signup-cta-container mdc-typography--caption" style="color: grey">
                    <h3>Don't have an account?
                        <Button href="/signup" target="_blank"><Label>Sign Up</Label></Button>
                    </h3>
                </div>
            </form>
        </Paper>
    </div>
</section>

<style>
    .signin-form-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: center;
        height: 100%;
        width: 100%;
    }

    .signin-form {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    * :global(.signin-form-item) {
        width: 100%;
        margin-bottom: 8px;
    }

    .signup-cta-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        margin-top: 1em;
    }
</style>