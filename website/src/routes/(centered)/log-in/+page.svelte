<script lang="ts">
    import {goto} from "$app/navigation";

    let username = $state("")
    let password = $state("")
    let waiting = $state(false)
    let loginBtnDisabled = $derived(username.length == 0 || password.length == 0 || waiting)

    async function LogIn()
    {
        try
        {
            waiting = true

            const res = await fetch("/api/log-in", {body: JSON.stringify({username, password}), method: "POST"})

            if (!res.ok)
            {
                alert("Username and password mismatched.")
                return
            }

            await goto("/dashboard")
        } finally
        {
            waiting = false
        }
    }
</script>

<form onsubmit={LogIn}>
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

    <button type="submit" disabled={loginBtnDisabled} class="my-btn">
        Log in
    </button>

    <p id="no-account-sign-up">
        Don't have an account? <a href="/sign-up">Sign up</a>.
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

    #no-account-sign-up {
        text-align: center;
    }
</style>
