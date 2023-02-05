<script lang="ts">
    import Textfield from '@smui/textfield';
    import Paper from '@smui/paper';
    import Button from '@smui/button';
    import {Icon} from '@smui/common';

    let email: string | undefined = '';
    let password: string | undefined = '';
    let confirm: string | undefined = '';
    let match: boolean;
    $: match = password === confirm;

    const handleSubmit = () => {
            console.log("Submitted!")
    }
</script>

<section title="Sign Up">
    <div class="signin-form-container">
        <Paper style="width: 460px">
            <h1 class="mdc-typography--headline4" style="margin: 0 0 8px 0; text-align: center">Create Account</h1>
            <form class="signin-form" on:submit|preventDefault={handleSubmit}>
                <Textfield bind:value={email} type="email" class="signin-form-item">
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
                        label="Password"
                        class="signin-form-item"
                />
                 <Textfield
                        bind:value={confirm}
                        invalid={!match}
                        type="password"
                        label="Confirm Password"
                        class="signin-form-item"
                        validationMessage="Passwords don't match!"
                />
                <Button type="submit" class="signin-button signin-form-item" variant="raised">Sign up</Button>
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