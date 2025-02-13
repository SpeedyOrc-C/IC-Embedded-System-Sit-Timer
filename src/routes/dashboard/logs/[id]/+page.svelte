<script lang="ts">
    import {goto} from "$app/navigation";

    const {data} = $props()

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
    <title>Logs | {data.name}</title>
</svelte:head>

<nav style="display: flex; justify-content: space-between; align-items: center;">
    <button id="btn-back" class="my-btn" onclick={() => goto("/dashboard")} style="height: 3rem; width: 3rem">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
            <!--!Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.-->
            <path d="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.2 288 416 288c17.7 0 32-14.3 32-32s-14.3-32-32-32l-306.7 0L214.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z"/>
        </svg>
    </button>

    <div id="name" style="flex-grow: 1; text-align: center; font-size: 1.5rem">
        {data.name}
    </div>
</nav>

<p id="disclaimer" style="font-size: 0.8rem; color: #aaa">
    Your data will not be disclosed to the public nor be used in any forms of research.
</p>

<table class="my-border">

    <thead>
    <tr>
        <th>Sitting Start Time</th>
        <th>Duration</th>
    </tr>
    </thead>

    <tbody>
    {#each data.intervals.toReversed() as {start, end}}
        <tr>
            <td>{start.toLocaleString()}</td>
            <td>{ReadableDuration(end.getTime() - start.getTime())}</td>
        </tr>
    {/each}
    </tbody>

</table>

<style lang="scss">
    @use "$lib/global";

    table {
        border-collapse: collapse;
    }

    th, td {
        padding: 0.5rem 0.8rem;
        font-size: 1rem;
    }

    th {
        border-bottom: 3px solid #333;
    }

    td {
        border-top: 1px solid #333;
    }
</style>
