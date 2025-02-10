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
        width: 100%;

        & > div {
            width: fit-content;
            margin: 0 auto;
        }
    }
</style>
