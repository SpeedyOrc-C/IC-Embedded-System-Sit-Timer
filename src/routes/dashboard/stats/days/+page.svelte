<script lang="ts">
    import {PadZero} from "$lib";
    import {onMount} from "svelte";

    const {data} = $props()

    const barScaleCoefficient = 1 / 1000 / 60 / 6

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

    onMount(()=>
    {
        const now = new Date()
        inputStartDate = `${now.getFullYear()}-${PadZero(now.getMonth() + 1)}-${PadZero(now.getDate())}T04:00:00`
    })

    function UpdateInputStartDateWhenDurationDaysChanges()
    {
        const d = new Date(new Date(inputStartDate).getTime() - 1000 * 60 * 60 * 24 * durationDays)
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

<table>
    <thead>
    <tr>
        <th>Colour</th>
        <th>Device Name</th>
    </tr>
    </thead>
    <tbody>
    {#each data.devices as {name}}
    <tr>
        <td></td>
        <td>{name}</td>
    </tr>
    {/each}
    </tbody>
</table>

<div id="chart">
    <div class="grid-head">Date</div>
    <div class="grid-head">Duration</div>

    {#each highlightedTimes as time, i}
        <div>
            <code>
                {time.getMonth() + 1}<span style="color: #bbb">/</span>{time.getDate()}
            </code>
        </div>

        <div class="duration">
            {#each durationData[i].map(x => x * barScaleCoefficient) as length}
                <div style="width: {length}px">
                    <!--{duration}-->
                </div>
            {/each}
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

    #chart {
        margin: 0 auto;
        display: grid;
        width: fit-content;

        grid-template-columns: auto auto;
    }

    .grid-head {
        padding: 0.5rem 1rem;

        background-color: white;
        position: sticky;
        top: 0;

        font-weight: bold;
    }

    .duration {
        display: flex;

        & > div {
            &         { background-color: cornflowerblue; }
            &+div     { background-color: coral; }
            &+div+div { background-color: darkolivegreen; }
        }
    }
</style>
