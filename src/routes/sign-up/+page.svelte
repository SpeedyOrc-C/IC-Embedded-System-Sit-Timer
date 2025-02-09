<script lang="ts">
    let username = $state("")
    let password = $state("")
    let confirmPassword = $state("")
    let disabled = $derived(username.length == 0 || password.length == 0 || password != confirmPassword)

    async function SignUp()
    {
        try
        {
            const response = await fetch("/api/sign-up", {body: JSON.stringify({username, password}), method: "POST"})

            console.info(await response.text())
        }
        catch (e)
        {
            alert(e)
        }
    }
</script>

<form>
    <div>
        <label for="username">
            Username
        </label>
        <input type="text" name="username" bind:value={username}>
    </div>

    <div>
        <label for="password">
            Password
        </label>
        <input type="password" name="password" bind:value={password}>
    </div>

    <div>
        <label for="confirm-password">
            Confirm Password
        </label>
        <input type="password" name="confirm-password" bind:value={confirmPassword}>
    </div>

    <button type="button" onclick={SignUp} {disabled}>
        Sign up
    </button>
</form>
