<script lang="ts">
    const {children} = $props()
</script>

<main>
    {@render children()}
</main>

<style lang="scss">
    @use "$lib/global.scss";

    main {
        margin: 1rem auto;
        padding: 0 1rem;
        max-width: 40rem;
    }
</style>
