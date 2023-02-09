<script lang="ts">
    import Textfield from '@smui/textfield';
    import HelperText from '@smui/textfield/helper-text';
    import Paper from '@smui/paper';
    import Button, {Label} from '@smui/button';
    import IconButton from '@smui/icon-button';
    import {Icon} from '@smui/common';
    import Snackbar, {Actions} from '@smui/snackbar';
    import {enhance} from "$app/forms";
    import type {ActionData} from './$types';
    import {makeDefaultTextfieldInputState} from "../../lib/utils/inputState";

    export let form: FormData;
    export let data: ActionData;

    let snackbar: Snackbar;
    let snackbarText: string = "";

    let email = makeDefaultTextfieldInputState(null, false) //setting dirty to false so we can check if field was touched
    let password = makeDefaultTextfieldInputState(null, false) // ^this

    function onSubmit({data, form, action, cancel}) {

        return async ({result, update}) => {
            console.log("result: ", result)
            if (result) {
                switch (result.type) {
                    case "success":
                        if (result.data.errors) {
                            const errors = result.data.errors;
                            email.value = "";
                            email.value = result.data.data.email;
                            if (errors.email) {
                                email.invalid = true;
                                email.helperText = errors.email;
                            }
                            if (errors.password) {
                                password.invalid = true;
                            }
                            if (errors.response) {
                                if(errors.response.status === 400) {
                                    snackbarText = "Invalid email or password";
                                    snackbar.open();
                                }else{
                                    snackbarText = "Something went wrong";
                                    snackbar.open();
                                }
                            }
                        } else {
                            console.log("success")
                            window.location.href = "/";
                        }

                        break;
                    case "invalid":
                        console.log("invalid")
                        break;
                    default:
                        console.log("default")
                        break;
                }
            }
            await update();
        }

    }
</script>

<section title="Sign In">

    <div class="signin-form-container form-container">
        <Snackbar bind:this={snackbar} labelText={snackbarText}>
        <Label>This is a snackbar.</Label>
        <Actions>
            <IconButton class="material-icons" title="Dismiss">close</IconButton>
        </Actions>
    </Snackbar>
        <Paper style="width: 50%; min-width: 250px; align-items: center">
            <h1 class="mdc-typography--headline4" style="margin: 0 0 8px 0; text-align: center">Sign In</h1>
            <form method="POST"
                  class="signin-form form"
                  use:enhance={onSubmit}
            >
                <Textfield
                        bind:value={email.value}
                        bind:invalid={email.invalid}
                        updateInvalid
                        helperLine$style="width: 100%;"
                        type="email"
                        input$name="email"
                        input$pattern="\S+@\S+\.\S+"
                        input$title="Please enter a valid email address"
                        input$maxlength="64"
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

                    <svelte:fragment slot="helper">
                        <HelperText
                                slot="helper"
                                class="signin-form-item"
                        >
                            {email.helperText}
                        </HelperText>
                    </svelte:fragment>
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
                >
                </Textfield>
                <Button
                        type="submit"
                        class="signin-button signin-form-item"
                        variant="raised"
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
        margin-bottom: 4px;
    }

    .signup-cta-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        margin-top: 1em;
    }

    * :global(.signin-button) {
        margin-top: 8px;
    }
</style>