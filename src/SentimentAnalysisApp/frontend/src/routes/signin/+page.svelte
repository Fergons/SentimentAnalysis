<script lang="ts">
    import Textfield from '@smui/textfield';
    import Paper from '@smui/paper';
    import Button from '@smui/button';
    import {Icon} from '@smui/common';
    import {enhance} from "$app/forms";
    import type { ActionData } from './$types';


    let email: string | undefined = '';
    let password: string | undefined = '';
    export let form: ActionData;
    const handleSubmit = () => {
            console.log("Submitted!")
    }
</script>

<section title="Sign In">
    <div class="signin-form-container">
        <Paper style="width: 460px">
            <h1 class="mdc-typography--headline4" style="margin: 0 0 8px 0; text-align: center">Sign In</h1>
            <form method="post" class="signin-form"  use:enhance>
                <Textfield bind:value={email}
                           type="email"
                           input$name="email"
                           class="signin-form-item"
                           required>
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
                        type="password"
                        input$name="password"
                        label="Password"
                        class="signin-form-item"
                        required
                />
                <Button type="submit" class="signin-button signin-form-item" variant="raised">Sign In</Button>
                <div class="signup-cta-container mdc-typography--caption" style="color: grey">
                    <h3>Don't have an account? <a href="/signup">Sign Up</a></h3>
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