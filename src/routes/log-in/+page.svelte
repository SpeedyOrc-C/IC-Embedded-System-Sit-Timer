<script lang="ts">
    let username = $state("")
    let password = $state("")
    let disabled = $derived(username.length == 0 || password.length == 0)

    async function LogIn()
    {
        try
        {
            const response = await fetch("/api/log-in", {body: JSON.stringify({username, password}), method: "POST", credentials: "include"})

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

    <button type="button" onclick={LogIn} {disabled}>
        Log in
    </button>
</form>
