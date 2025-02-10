<script lang="ts">
    import {goto} from "$app/navigation";

    const {data: dataImmutable} = $props()

    const data = $state(dataImmutable)

    let waiting = $state(false)

    async function ChangeDeviceName(index: number, name: string)
    {
        if (waiting)
        {
            return
        }

        if (data.userId == null)
        {
            console.error("Not logged in.")
            return
        }

        const newName = prompt("Enter a new name for the device", name)

        if (newName == null)
        {
            return
        }

        waiting = true

        try
        {
            const res = await fetch(`/api/device/${data.devices[index].device_id}/name`, {method: "PUT", body: newName})

            if (!res.ok)
            {
                return
            }
        } finally
        {
            waiting = false
        }

        data.devices[index].name = newName
    }

    async function DeleteDevice(index: number)
    {
        if (waiting)
        {
            return
        }

        if (data.userId == null)
        {
            console.error("Not logged in.")
            return
        }

        if (!confirm(`Are you sure you want to delete ${data.devices[index].name}?`))
        {
            return
        }

        waiting = true

        try
        {
            const res = await fetch(`/api/device/${data.devices[index].device_id}`, {method: "DELETE"})

            if (!res.ok)
            {
                return
            }
        } finally
        {
            waiting = false
        }

        data.devices.splice(index, 1)
    }

    async function AddNewDevice()
    {
        if (data.userId == null)
        {
            console.error("Not logged in.")
            return
        }

        const codeRaw = prompt("Enter the 4-digit code on the device:")

        if (codeRaw == null)
        {
            return
        }

        if (codeRaw.length != 4)
        {
            alert("The code must be exactly 4 digits.")
            return
        }

        if (!/^[0-9a-fA-F]{4}$/.test(codeRaw))
        {
            alert("The code can only contain numbers (0~9) and letters (A~F).")
            return
        }

        const code = codeRaw.toLowerCase()

        waiting = true

        try
        {
            const res = await fetch(`/api/device/pairing/${code}`, {method: "GET"})

            if (!res.ok)
            {
                alert("Invalid code.")
                return
            }

            const {newDeviceId} = await res.json()

            data.devices.unshift({name: "Untitled Device", device_id: newDeviceId})
        } finally
        {
            waiting = false
        }
    }

    async function LogOut()
    {
        if (waiting)
        {
            return
        }

        if (!confirm("Are you sure you want to log out?"))
        {
            return
        }

        waiting = true

        try
        {
            await fetch("/api/log-out", {method: "POST"})
        } finally
        {
            waiting = false
            await goto("/log-in")
        }

    }

    async function LogOutFromAllPlaces()
    {
        if (waiting)
        {
            return
        }

        if (!confirm("Are you sure you want to log out from all places?"))
        {
            return
        }

        waiting = true

        try
        {
            await fetch("/api/log-out/all-places", {method: "POST"})
        } finally
        {
            waiting = false
            await goto("/log-in")
        }

    }

    function CopyId(id: string)
    {
        navigator.clipboard.writeText(id)
    }
</script>

<svelte:head>
    <title>Sitting Dashboard</title>
</svelte:head>

<main>

    {#if data.userId == null}

        <p>Not logged in, please <a href="/log-in">log in</a>.</p>

    {:else}

        <p>Hello, {data.userId}!</p>

        <div>

            <button onclick={() => AddNewDevice()} disabled={waiting}>
                Add new device...
            </button>

            <button onclick={() => LogOut()} disabled={waiting}>
                Log out...
            </button>

            <button onclick={() => LogOutFromAllPlaces()} disabled={waiting}>
                Log out from all places...
            </button>

        </div>

        <div>
            {#each data.devices as {name, device_id}, index}
                <article class="my-border">
                    <div style="display: flex; gap: 1rem; justify-content: space-between;">
                        <header>
                            {name}
                        </header>
                        <code>
                            {device_id.slice(0, 8)}
                        </code>
                    </div>

                    <br>

                    <div class="operations">
                        <button class="my-btn">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--!Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.--><path d="M160 80c0-26.5 21.5-48 48-48l32 0c26.5 0 48 21.5 48 48l0 352c0 26.5-21.5 48-48 48l-32 0c-26.5 0-48-21.5-48-48l0-352zM0 272c0-26.5 21.5-48 48-48l32 0c26.5 0 48 21.5 48 48l0 160c0 26.5-21.5 48-48 48l-32 0c-26.5 0-48-21.5-48-48L0 272zM368 96l32 0c26.5 0 48 21.5 48 48l0 288c0 26.5-21.5 48-48 48l-32 0c-26.5 0-48-21.5-48-48l0-288c0-26.5 21.5-48 48-48z"/></svg>
                        </button>

                        <button title="Change name" class="my-btn btn-change-name" onclick={() => ChangeDeviceName(index, name)} disabled={waiting}>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.--><path d="M471.6 21.7c-21.9-21.9-57.3-21.9-79.2 0L362.3 51.7l97.9 97.9 30.1-30.1c21.9-21.9 21.9-57.3 0-79.2L471.6 21.7zm-299.2 220c-6.1 6.1-10.8 13.6-13.5 21.9l-29.6 88.8c-2.9 8.6-.6 18.1 5.8 24.6s15.9 8.7 24.6 5.8l88.8-29.6c8.2-2.7 15.7-7.4 21.9-13.5L437.7 172.3 339.7 74.3 172.4 241.7zM96 64C43 64 0 107 0 160L0 416c0 53 43 96 96 96l256 0c53 0 96-43 96-96l0-96c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 96c0 17.7-14.3 32-32 32L96 448c-17.7 0-32-14.3-32-32l0-256c0-17.7 14.3-32 32-32l96 0c17.7 0 32-14.3 32-32s-14.3-32-32-32L96 64z"/></svg>
                        </button>

                        <button title="Copy ID" class="my-btn btn-copy-id" onclick={() => CopyId(device_id)}>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--!Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.--><path d="M181.3 32.4c17.4 2.9 29.2 19.4 26.3 36.8L197.8 128l95.1 0 11.5-69.3c2.9-17.4 19.4-29.2 36.8-26.3s29.2 19.4 26.3 36.8L357.8 128l58.2 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-68.9 0L325.8 320l58.2 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-68.9 0-11.5 69.3c-2.9 17.4-19.4 29.2-36.8 26.3s-29.2-19.4-26.3-36.8l9.8-58.7-95.1 0-11.5 69.3c-2.9 17.4-19.4 29.2-36.8 26.3s-29.2-19.4-26.3-36.8L90.2 384 32 384c-17.7 0-32-14.3-32-32s14.3-32 32-32l68.9 0 21.3-128L64 192c-17.7 0-32-14.3-32-32s14.3-32 32-32l68.9 0 11.5-69.3c2.9-17.4 19.4-29.2 36.8-26.3zM187.1 192L165.8 320l95.1 0 21.3-128-95.1 0z"/></svg>
                        </button>

                        <button title="Delete" class="my-btn btn-delete" onclick={() => DeleteDevice(index)} disabled={waiting}>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--!Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.--><path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"/></svg>
                        </button>
                    </div>
                </article>
            {/each}
        </div>

    {/if}

</main>

<style lang="scss">
    @import "$lib/global.scss";

    main {
        margin: 1rem;
    }

    article {
        min-width: 18rem;
        width: fit-content;
        max-width: 40rem;
        margin: 1rem;
        padding: 1rem;

        & header {
            font-size: 1.5rem;
        }

        & code {
            color: #888;
        }
    }

    .operations {
        display: flex;
        gap: 10px;

        & > button {
            height: 3rem; width: 3rem;

            &:hover {
                &.btn-delete {
                    background: orangered;
                }
            }
        }
    }
</style>
