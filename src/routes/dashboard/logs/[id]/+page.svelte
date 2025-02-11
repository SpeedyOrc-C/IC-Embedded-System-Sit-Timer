<script lang="ts">
    const {data} = $props()

    const logs: { time: Date, existence: boolean }[] = data.logs.map(({time, existence}) => ({
        time: new Date(time),
        existence
    }))

    console.log(logs)

    // Remove first "stand up" record
    if (logs.length > 0 && !logs[0].existence)
    {
        logs.shift()
    }

    // Remove last "stand down" record
    if (logs.length > 0 && logs[logs.length - 1].existence)
    {
        logs.pop()
    }

    const normalizedLogs: { time: Date, existence: boolean }[] = []

    if (logs.length > 0)
    {
        let {existence: lastExistence} = logs[0]

        normalizedLogs.push(logs[0])

        logs.shift()

        for (const log of logs)
        {
            if (log.existence !== lastExistence)
            {
                normalizedLogs.push(log)
                lastExistence = log.existence
            }
        }
    }

    const intervals: { start: Date, end: Date }[] = []

    for (let i = 0; i < normalizedLogs.length / 2; i += 1)
    {
        intervals.push({start: normalizedLogs[i * 2].time, end: normalizedLogs[i * 2 + 1].time})
    }

    function ReadableDuration(ms: number)
    {
        const s = ms / 1000

        if (s < 60)
        {
            return `Less than 1 min`
        }

        const m = s / 60

        if (m < 60)
        {
            return `${Math.floor(m)} min`
        }

        const h = m / 60

        if (m % 60 < 1)
        {
            return `${Math.floor(h)} hour`
        }

        return `${Math.floor(h)} hour ${Math.floor(m % 60)} min`
    }
</script>

<svelte:head>
    <title>Logs for {data.name}</title>
</svelte:head>

<p>Disclaimer: Your data will not be disclosed to the public nor be used in any research.</p>

<table class="my-border">

    <thead>
    <tr>
        <th>Sitting Start Time</th>
        <th>Duration</th>
    </tr>
    </thead>

    <tbody>
    {#each intervals.toReversed() as {start, end}}
        <tr>
            <td>{start.toLocaleString()}</td>
            <td>{ReadableDuration(end.getTime() - start.getTime())}</td>
        </tr>
    {/each}
    </tbody>

</table>

<style lang="scss">
    @use "$lib/global.scss";

    table {
        border-collapse: collapse;
    }

    th, td {
        padding: 0.5rem 0.8rem;
        font-size: 1rem;
    }
</style>
