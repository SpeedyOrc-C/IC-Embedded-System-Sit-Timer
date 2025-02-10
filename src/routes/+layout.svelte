<script lang="ts">
    let {children} = $props()
</script>

{@render children()}

<style>
    :global(body) {
        margin: 0;
        color: #333;
        font-family: -apple-system, sans-serif;
    }

    :global(*) {
        box-sizing: border-box;
    }
</style>
