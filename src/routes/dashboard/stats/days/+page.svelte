<script lang="ts">
    import {PadZero, ReadableShortDuration} from "$lib";
    import {onMount} from "svelte";

    const {data} = $props()

    let durationDays = $state(7)
    let inputStartDate = $state(`1970-01-01T00:00:00`)

    const durationMs = $derived(1000 * 60 * 60 * 24 * durationDays)
    const startDate = $derived(new Date(inputStartDate))
    const endDate = $derived(new Date(startDate.getTime() + durationMs))

    const highlightedTimes = $derived.by(() =>
    {
        const xs: Date[] = []

        const date = new Date(startDate.getTime())

        for (; date < endDate; date.setTime(date.getTime() + 1000 * 60 * 60 * 24))
        {
            xs.push(new Date(date.getTime()))
        }

        return xs
    })

    const durationData = $derived.by(() =>
    {
        const xss: number[][] = new Array(durationDays)

        for (let i = 0; i < durationDays; i += 1)
        {
            xss[i] = new Array(data.devices.length).fill(0)
        }

        for (const [device_id, logs] of data.devicesLogs)
        {
            for (const log of logs)
            {
                const {start, end} = log

                const startIndex = Math.floor((start.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24))

                if (startIndex < 0 || startIndex >= durationDays)
                {
                    continue
                }

                const endIndex = Math.floor((end.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24))

                if (endIndex < 0 || endIndex >= durationDays)
                {
                    continue
                }

                if (startIndex == endIndex)
                {
                    const deviceIndex = data.devices.findIndex(({device_id: d}) => device_id == d)

                    xss[startIndex][deviceIndex] += end.getTime() - start.getTime()
                }
            }
        }

        return xss
    })

    const max1SitAtDateData = $derived.by(() =>
    {
        const xs: number[] = new Array(durationDays).fill(0)

        for (let day = 0; day < durationDays; day += 1)
        {
            const thisDayStart = new Date(startDate.getTime() + 1000 * 60 * 60 * 24 * day)
            const thisDayEnd = new Date(thisDayStart.getTime() + 1000 * 60 * 60 * 24)

            for (const [, logs] of data.devicesLogs)
            {
                for (const log of logs.filter(({start, end}) => thisDayStart <= start && end < thisDayEnd))
                {
                    xs[day] = Math.max(xs[day], log.end.getTime() - log.start.getTime())
                }
            }
        }

        return xs
    })

    const longestDurationMs = $derived(
        durationData
            .map(xs => xs.reduce((a, b) => a + b, 0))
            .reduce((a, b) => Math.max(a, b), 0)
    )

    onMount(() =>
    {
        const now = new Date(new Date().getTime() - 1000 * 60 * 60 * 24 * (durationDays - 1))
        inputStartDate = `${now.getFullYear()}-${PadZero(now.getMonth() + 1)}-${PadZero(now.getDate())}T04:00:00`
    })

    function UpdateInputStartDateWhenDurationDaysChanges()
    {
        const d = new Date(new Date().getTime() - 1000 * 60 * 60 * 24 * (durationDays - 1))
        inputStartDate = `${d.getFullYear()}-${PadZero(d.getMonth() + 1)}-${PadZero(d.getDate())}T04:00:00`
    }
</script>

<div style="display: flex; justify-content: center; align-items: center">
    <div>
        Starts from
    </div>

    <input type="datetime-local" bind:value={inputStartDate} class="my-border">
</div>

<br>

<div style="display: flex; justify-content: center; align-items: center">
    <div>
        With duration of
    </div>

    <select class="my-border my-btn" bind:value={durationDays} onchange={UpdateInputStartDateWhenDurationDaysChanges}>
        <option value={7}>
            1 week
        </option>
        <option value={14}>
            2 weeks
        </option>
        <option value={30}>
            1 month
        </option>
        <option value={90}>
            3 months
        </option>
        <option value={180}>
            6 months
        </option>
        <option value={365}>
            1 year
        </option>
    </select>
</div>

<br>

<p>Legend</p>

<ul id="legend" class="my-colour-series">
    {#each data.devicesLogs as [id,]}
        <li>{data.devices.find(d => d.device_id == id).name}</li>
    {/each}
</ul>

<br>

<div id="chart" class="my-border">
    <div class="grid-head">Date</div>
    <div class="grid-head">Max Sit</div>
    <div class="grid-head">Duration</div>

    {#each highlightedTimes as time, i}
        {@const totalDurationMs = durationData[i].reduce((a, b) => a + b, 0)}
        <div class="time">
            <code>
                {time.getMonth() + 1}<span style="color: #bbb">/</span>{time.getDate()}
            </code>
        </div>

        <div class="max-1-sit">
            {#if max1SitAtDateData[i] > 0}
                {ReadableShortDuration(max1SitAtDateData[i])}
            {/if}
        </div>

        <div class="duration my-colour-series">
            {#each durationData[i].map(x => x / longestDurationMs * 350) as length}
                <div style="width: {length}px"></div>
            {/each}
            <div style="background-color: unset; margin-left: 0.5rem">
                {#if totalDurationMs > 0}
                    {ReadableShortDuration(totalDurationMs)}
                {/if}
            </div>
        </div>
    {/each}
</div>

<style lang="scss">
    @use "$lib/global.scss";

    input[type="datetime-local"], select {
        font-size: 1.2rem;
        margin: 0 0.5rem;
        padding: 0.2rem 0.3rem;
    }

    #legend {
        & > li {
            padding: 0.2rem 0.4rem;
            width: fit-content;
            color: white;
            font-weight: bold;
        }
    }

    #chart {
        margin: 0 auto;
        display: grid;
        width: fit-content;
        padding: 0.5rem;

        grid-template-columns: auto auto auto;
    }

    .grid-head {
        padding: 0.2rem 0.5rem;

        background-color: white;
        position: sticky;
        top: 0;

        font-weight: bold;
    }

    .duration {
        display: flex;
    }

    .my-colour-series {
        & > * {
            & {
                background-color: #093145;
            }

            & + * {
                background-color: #829356;
            }

            & + * + * {
                background-color: #BCA136;
            }

            & + * + * + * {
                background-color: #C2571A;
            }
        }
    }

    .time, .max-1-sit {
        text-align: center;
    }
</style>
