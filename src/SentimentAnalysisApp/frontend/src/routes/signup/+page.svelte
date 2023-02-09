<script lang="ts">
    import Textfield from '@smui/textfield';
    import Paper from '@smui/paper';
    import Button from '@smui/button';
    import {Icon} from '@smui/common';
    import {enhance} from "$app/forms";

    let email: string | undefined = '';
    let password: string | undefined = '';
    let confirm: string | undefined = '';
    let invalidEmail: boolean = false;
    let invalidPassword: boolean = false;
    let match: boolean;
    $: match = password === confirm;
    $: disabled = !(match && email && password && !invalidEmail && !invalidPassword);
    async function onSubmit ({data, form, action, cancel}) {
        return async ({result, update}) =>{
            await update()
        }


    }
</script>

<section title="Sign Up">
    <div class="signin-form-container">
        <Paper style="width: 460px">
            <h1 class="mdc-typography--headline4" style="margin: 0 0 8px 0; text-align: center">Create Account</h1>
            <form method="POST" class="signin-form" use:enhance={onSubmit}>
                <Textfield bind:value={email}
                           bind:invalid={invalidEmail}
                           updateInvalid
                           type="email"
                           class="signin-form-item"
                           input$autocomplete="email"
                           input$type="email"
                           input$pattern="\S+@\S+\.\S+"
                           input$maxlength="64"
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
                </Textfield>
                <Textfield
                        bind:value={password}
                        bind:invalid={invalidPassword}
                        updateInvalid
                        type="password"
                        label="Password"
                        class="signin-form-item"
                        input$maxlength="32"
                        input$minlength="8"
                        required
                />
                 <Textfield
                        bind:value={confirm}
                        invalid={!match}
                        type="password"
                        label="Confirm Password"
                        class="signin-form-item"
                        validationMessage="Passwords don't match!"
                        input$maxlength="32"
                        input$minlength="8"
                        required
                />
                <Button type="submit" class="signin-button signin-form-item" variant="raised" disabled={disabled}>Sign up</Button>
                <div class="signup-cta-container mdc-typography--caption" style="color: grey">
                    <h3>Already have an account? <a href="/signin">Sign In</a></h3>
                </div>
            </form>
        </Paper>
    </div>
</section>

<style>
    .signin-form-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        width: 40%;
    }

    .signin-form {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    * :global(.signin-form-item) {
        width: 80%;
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