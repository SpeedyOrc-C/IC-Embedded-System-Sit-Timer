<svelte:head>
  <title>SitSense - Home</title>
</svelte:head>

<!-- HERO SECTION -->
<section class="hero">
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <h1>Welcome to SitSense</h1>
    <p>
      Prevent the Health Risks of Prolonged Sitting with Our Smart Seating
      Monitor
    </p>
    <a class="cta-button" href="about">Learn More</a>
  </div>
</section>

<!-- MAIN CONTENT -->
<main>
  <section>
    <h2>Stay Active, Stay Healthy</h2>
    <p>
      Prolonged sitting can lead to a variety of health risks, including
      cardiovascular disease, obesity, and musculoskeletal issues. SitSense
      helps you monitor your sitting habits in real-time and reminds you to take
      breaks, so you can maintain a healthier, more active lifestyle.
    </p>
    <p>
      Ready to dive deeper? Visit our <a href="about">About</a> page to learn
      how SitSense works, or check out our
      <a href="pricing">Pricing</a> to find a plan that fits your needs.
    </p>
  </section>
  <!-- VIDEO SECTION -->
  <section class="video-section">
    <h2>Watch Our Overview</h2>
    <!-- svelte-ignore a11y_media_has_caption -->
    <video controls>
      <source src="/marketing-video.mp4" type="video/mp4" />
      Your browser does not support the video tag.
    </video>
  </section>
</main>

<!-- FOOTER -->
<footer>
  <p>&copy; 2025 SitSense. All rights reserved.</p>
  <div class="footer-links">
    <a href="about">About</a>
    <a href="pricing">Pricing</a>
    <a href="contact">Contact</a>
  </div>
</footer>

<style lang="scss">
  @use "$lib/style";
</style>
