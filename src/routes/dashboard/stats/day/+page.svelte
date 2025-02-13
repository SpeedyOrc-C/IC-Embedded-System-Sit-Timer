<script lang="ts">
    import {PadZero} from "$lib";

    const {data} = $props()

    const now = new Date()

    let intervalMs = $state(1000 * 60 * 60)
    let startDateString = $state(`${now.getFullYear()}-${PadZero(now.getMonth()+1)}-${PadZero(now.getDate())}T04:00:00`)

    const startDate = $derived(new Date(startDateString))
    const endDate = $derived(new Date(startDate.getTime() + 1000 * 60 * 60 * 24))

    const highlightedTimes = $derived.by(() =>
    {
        const xs: Date[] = []

        for (let offsetMs = 0; offsetMs < 1000 * 60 * 60 * 24; offsetMs += intervalMs)
        {
            xs.push(new Date(startDate.getTime() + offsetMs))
        }

        return xs
    })

    const devicesLogsWithinRange = $derived.by(() =>
    {
        const map = new Map<string, { start: Date, end: Date }[]>()

        for (const [device_id, logs] of data.devicesLogs)
        {
            const logsWithinRange = logs.filter(log => log.start >= startDate && log.end < endDate)

            map.set(device_id, logsWithinRange)
        }

        return map
    })

    const sitData = $derived.by(() =>
    {
        const map: Map<string, boolean[]> = new Map()

        for (const [device_id, logs] of devicesLogsWithinRange)
        {
            const data = new Array(highlightedTimes.length).fill(false)

            for (const log of logs)
            {
                const {start, end} = log

                const startIndex = Math.floor((start.getTime() - startDate.getTime()) / intervalMs)
                const endIndex = Math.floor((end.getTime() - startDate.getTime()) / intervalMs)

                for (let i = startIndex; i <= endIndex; i++)
                {
                    data[i] = true
                }
            }

            map.set(device_id, data)
        }

        return map
    })
</script>

<div style="display: flex; justify-content: center; align-items: center;">
    <div>
        Starts at
    </div>

    <input type="datetime-local" bind:value={startDateString} class="my-border">
</div>

<br>

<div style="display: flex; justify-content: center; align-items: center;">
    <div>
        With intervals of
    </div>

    <select class="my-border my-btn" bind:value={intervalMs}>
        <option value={1000 * 60 * 60}>
            60 mins
        </option>
        <option value={1000 * 60 * 30}>
            30 mins
        </option>
        <option value={1000 * 60 * 20}>
            20 mins
        </option>
        <option value={1000 * 60 * 15}>
            15 mins
        </option>
        <option value={1000 * 60 * 10}>
            10 mins
        </option>
        <option value={1000 * 60 * 5}>
            5 mins
        </option>
        <option value={1000 * 60}>
            1 min
        </option>
    </select>
</div>

<br>

<div id="chart"
     style:grid-template-columns="repeat({data.devices.length + 1}, auto)"
     style:grid-template-rows="repeat({highlightedTimes.length + 1}, auto)"
>
    <div class="grid-head">
        Time Interval
    </div>

    {#each data.devices as {name}}
        <div class="grid-head">
            {name}
        </div>
    {/each}

    {#each highlightedTimes as highlightedTime, index}
        <code class="grid-body time">
            {PadZero(highlightedTime.getHours())}<span style="color: #bbb">:{PadZero(highlightedTime.getMinutes())}</span>
        </code>

        {#each data.devices as {device_id}}
            <div class="grid-body device-name" class:sit={sitData.get(device_id)[index]}></div>
        {/each}
    {/each}
</div>

<br>

<style lang="scss">
    @use "$lib/global";

    input[type="datetime-local"], select {
        font-size: 1.2rem;
        margin: 0 0.5rem;
        padding: 0.2rem 0.3rem;
    }

    #chart {
        margin: 0 auto;
        display: grid;
        width: fit-content;

        & .time {
            text-align: center;
        }
    }

    .sit {
        background-color: #333;
    }

    .grid-head {
        writing-mode: vertical-lr;
        text-align: end;
        padding: 1rem 0.5rem;

        background-color: white;
        position: sticky;
        top: 0;

        font-weight: bold;
    }

    .grid-body {
        border-top: 1px solid #ddd;
        border-right: 1px solid #ddd;
    }
</style>
