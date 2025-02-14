<svelte:head>
    <title>SitSense - About</title>
</svelte:head>

<!-- MAIN CONTENT -->
<main>
    <!-- What is SitSense -->
    <section>
        <h2>What is SitSense?</h2>
        <p>
            SitSense is an innovative smart monitoring system designed to track your sitting habits and help prevent
            health issues caused by prolonged sitting. This system uses a Raspberry Pi, a GPIO ultrasonic sensor, and
            an I2C flex sensor to detect when someone is seated and for how long. If you sit for more than 30 minutes,
            the LED lights up as a reminder to take a break. Additionally, SitSense logs your sitting data and uploads
            it to our server, where you can analyze your habits through an interactive website.
        </p>
    </section>

    <!-- How It Works -->
    <section>
        <h3>How It Works</h3>
        <ul>
            <li>
                <strong>Detecting Sitting Time</strong> <br>A GPIO ultrasonic sensor and an I2C flex sensor detect seating
                pressure and proximity, sending real-time data to the Raspberry Pi.
            </li>
            <li>
                <strong>Smart Notification System</strong> <br> If you exceed 30 minutes of continuous sitting, the LED
                lights up as a reminder.
            </li>
            <li>
                <strong>Data Processing & Storage</strong> <br> The collected data is transmitted via HTTPS to our
                secure server.
            </li>
            <li>
                <strong>Visual Insights & Analysis</strong> <br> Our website provides tools to analyze your total sitting
                time and maximum sitting duration per session, helping you track long-term trends.
            </li>
            <li>
                <strong>Health Awareness</strong> <br> Monitor your sitting behavior to reduce the risk of long-term
                health problems.
            </li>
            <li>
                <strong>Multi-Device Compatibility</strong> <br> SitSense can be used on both toilets and chairs, providing
                accurate sitting detection in different environments.
            </li>
            <li>
                <strong>Long-time Battery</strong> <br> SitSense is working with Four AAA batteries, and which can last for
                one
                year each time.
                <br>
            </li>
            <li>
                <strong>Dual-Sensor Reliability</strong> <br> It works with two sensors for double-check accuracy. If one
                sensor
                fails, the system can rely on the other for continued functionality.
            </li>

        </ul>
    </section>

    <!-- Health Risks -->
    <section>
        <h3>Health Risks of Prolonged Sitting</h3>
        <p><strong>🚽 Toilet-Related Risks:</strong> Sitting on a toilet for too long can increase pressure on the rectal
            veins, leading to hemorrhoids and even prolapse. The perineum is also unsupported, which can contribute to
            discomfort and strain.</p>
        <p><strong>🚨 Obesity & Metabolic Disorders:</strong> Sitting for long hours reduces calorie burning and can lead
            to weight gain and metabolic syndrome.</p>
        <p><strong>⚠️ Cardiovascular Diseases:</strong> Prolonged sitting has been linked to an increased risk of heart
            disease and high blood pressure.</p>
        <p><strong>🩺 Back and Spinal Issues:</strong> Poor posture and prolonged sitting contribute to chronic back pain
            and spinal disorders.</p>
        <p><strong>🧠 Mental Health Impact:</strong> Reduced physical activity due to excessive sitting can contribute to
            stress, anxiety, and depression.</p>
    </section>

    <!-- NEW: Product Image Section -->
    <section>
        <h3>Product Preview</h3>
        <p>Get a closer look at our cutting-edge SitSense hardware.</p>
        <br>
        <div class="product-image-container">

            <!-- Replace the src with your actual product image URL -->
            <img
                    src="/product-in-toilet.jpg"
                    class="product-image"
                    alt="SitSense Product Image"
            >
            <img
                    src="/product-on-table.jpg"
                    class="product-image"
                    alt="SitSense Product Image"
            >
        </div>
    </section>
</main>

<!-- FOOTER -->
<footer>
    <p>&copy; 2025 SitSense. All rights reserved.</p>
    <div class="footer-links">
        <a href="/">Home</a>
        <a href="pricing">Pricing</a>
        <a href="contact">Contact</a>
    </div>
</footer>

<style lang="scss">
  @use "$lib/style";

  li{
    padding: 8px 0;
  }
</style>
