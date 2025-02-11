<script lang="ts">
    import {goto} from "$app/navigation";

    let username = $state("")
    let password = $state("")
    let confirmPassword = $state("")
    let waiting = $state(false)
    let signupBtnDisabled = $derived(username.length == 0 || password.length == 0 || password != confirmPassword || waiting)

    async function SignUp()
    {
        try
        {
            waiting = true

            const res = await fetch("/api/sign-up", {body: JSON.stringify({username, password}), method: "POST"})

            if (!res.ok)
            {
                const message = await res.text()
                alert(message)

                return
            }

            const res2 = await fetch("/api/log-in", {body: JSON.stringify({username, password}), method: "POST"})

            if (!res2.ok)
            {
                alert("Failed to log in after sign up, please contact us.")

                return
            }

            await goto("/dashboard")
        } finally
        {
            waiting = false
        }
    }
</script>

<form onsubmit={SignUp}>
    <p>
        <label for="username">
            Username
        </label>
        <input type="text" name="username" bind:value={username}>
    </p>

    <p>
        <label for="password">
            Password
        </label>
        <input type="password" name="password" bind:value={password}>
    </p>

    <p>
        <label for="confirm-password">
            Confirm Password
        </label>
        <input type="password" name="confirm-password" bind:value={confirmPassword}>
    </p>

    <button type="submit" disabled={signupBtnDisabled} class="my-btn">
        Sign up
    </button>

    <p id="have-account-log-in">
        Already have an account? <a href="/log-in">Log in</a>.
    </p>
</form>

<style lang="scss">
    @use "$lib/global.scss";

    form {
        width: 100%;
        max-width: 21rem;
        padding: 1rem;
    }

    label, input {
        display: block;
    }

    input {
        font-size: 1.5rem;
        padding: 0.5rem 0.8rem;
        width: 100%;
    }

    button {
        font-size: 1.5rem;
        padding: 0.5rem 0.8rem;
        width: 100%;
    }

    #have-account-log-in {
        text-align: center;
    }
</style>
