<script lang="ts">
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
        }
        finally
        {
            waiting = false
        }
    }

    function CopyId(id: string)
    {
        navigator.clipboard.writeText(id)
    }
</script>

<svelte:head>
    <title>Dashboard | {data.userId}</title>
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
        </div>

        <table>

            <caption>{data.devices.length} Device(s)</caption>

            <thead>
            <tr>
                <th>Operations</th>
                <th>Name</th>
                <th>Unique ID</th>
            </tr>
            </thead>

            <tbody>
            {#each data.devices as {name, device_id}, index}
                <tr>

                    <td>
                        <button onclick={() => DeleteDevice(index)} disabled={waiting}>
                            Delete...
                        </button>
                        <button onclick={() => ChangeDeviceName(index, name)} disabled={waiting}>
                            Rename...
                        </button>
                        <button onclick={() => CopyId(device_id)}>
                            Copy ID
                        </button>
                    </td>

                    <td class="device-name">
                        {name}
                    </td>

                    <td class="device-id">
                        {device_id}
                    </td>

                </tr>
            {/each}
            </tbody>

        </table>

    {/if}

</main>

<style>
    .device-name {
        cursor: pointer;
    }

    .device-id {
        max-width: 10rem;
        overflow: auto;
    }
</style>
