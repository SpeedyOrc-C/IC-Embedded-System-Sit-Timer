<script lang="ts">
  const {children} = $props()
</script>

<header>
  <nav class="nav-bar">
    <div class="logo">SitSense</div>
    <ul class="nav-menu">
      <li><a href="/">Home</a></li>
      <li><a href="about">About</a></li>
      <li><a href="pricing">Pricing</a></li>
      <li><a href="contact">Contact</a></li>
      <li><a href="/log-in">Login</a></li>
    </ul>
  </nav>
</header>

{@render children()}

<style lang="scss">
  @use "$lib/style";
</style>
