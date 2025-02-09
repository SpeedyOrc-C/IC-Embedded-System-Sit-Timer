<script lang="ts">
    let {children} = $props()
</script>

{@render children()}

<style>
    :global(body) {
        margin: 1rem;
        font-family: -apple-system, sans-serif;
    }
</style>
