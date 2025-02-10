<script lang="ts">
    let {children} = $props()
</script>

<div class="wrapper-out">
    <div>
        {@render children()}
    </div>
</div>

<style>
    .wrapper-out {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100vw;
        overflow: hidden;
    }
</style>
