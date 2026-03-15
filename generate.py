#!/usr/bin/env python3
"""Generate Privacy Policy and Terms of Service HTML pages for all 46 iOS apps."""

import os

EFFECTIVE_DATE = "March 15, 2026"
DEVELOPER = "Orca AI"
EMAIL = "orca.ai.admin@gmail.com"
BASE_URL = "https://orca-ai-admin.github.io/app-legal"

# App data: (display_name, slug, description, has_healthkit, is_health_app)
APPS = [
    ("ADHDLog", "adhdlog", "ADHD symptom and focus tracking", True, True),
    ("AnxietyKit", "anxietykit", "anxiety management and mood tracking", True, True),
    ("AsthmaLog", "asthmalog", "asthma symptom and trigger tracking", True, True),
    ("BPLog", "bplog", "blood pressure monitoring and tracking", True, True),
    ("BabyLog", "babylog", "baby feeding, sleep, and growth tracking", True, True),
    ("BackLog", "backlog", "back pain and posture tracking", True, True),
    ("BreathWork", "breathwork", "guided breathing exercises and respiratory tracking", True, True),
    ("CPAPLog", "cpaplog", "CPAP therapy and sleep apnea tracking", True, True),
    ("CaffeineLog", "caffeinelog", "caffeine intake and sleep quality tracking", True, True),
    ("ChronicLog", "chroniclog", "chronic condition symptom tracking", True, True),
    ("ColdPlunge", "coldplunge", "cold water therapy and recovery tracking", True, True),
    ("CycleTrack", "cycletrack", "menstrual cycle and fertility tracking", True, True),
    ("DailyAffirm", "dailyaffirm", "daily affirmations and positive mindset", False, False),
    ("DrinkWise", "drinkwise", "alcohol intake and sobriety tracking", True, True),
    ("EczemaLog", "eczemalog", "eczema flare and skin condition tracking", True, True),
    ("FertilityLog", "fertilitylog", "fertility tracking and ovulation monitoring", True, True),
    ("FibromyalgiaLog", "fibromyalgialog", "fibromyalgia pain and symptom tracking", True, True),
    ("FlashDeck", "flashdeck", "flashcard-based learning and study tool", False, False),
    ("GlucoseLog", "glucoselog", "blood glucose monitoring and diabetes tracking", True, True),
    ("GratitudeLog", "gratitudelog", "gratitude journaling and wellness reflection", False, False),
    ("HabitStack", "habitstack", "habit building and daily routine tracking", False, False),
    ("HydroLog", "hydrolog", "hydration and water intake tracking", True, True),
    ("IBSLog", "ibslog", "IBS symptom, diet, and trigger tracking", True, True),
    ("IntervalTimer", "intervaltimer", "interval training and fitness timer", True, True),
    ("JournalDark", "journaldark", "private journaling with dark-themed interface", False, False),
    ("MacroLog", "macrolog", "macronutrient and calorie tracking", True, True),
    ("MealPlan", "mealplan", "meal planning and nutrition tracking", True, True),
    ("MigraineLog", "migrainelog", "migraine and headache tracking", True, True),
    ("NicoFree", "nicofree", "smoking cessation and nicotine tracking", True, True),
    ("NoiseBox", "noisebox", "ambient sounds and focus noise generator", False, False),
    ("PetLog", "petlog", "pet health and care tracking", False, False),
    ("PillRemind", "pillremind", "medication reminders and adherence tracking", True, True),
    ("PlantMom", "plantmom", "plant care scheduling and tracking", False, False),
    ("PomodoroFlow", "pomodoroflow", "Pomodoro technique focus and productivity timer", False, False),
    ("PostureLog", "posturelog", "posture and ergonomics tracking", True, True),
    ("ReadingList", "readinglist", "personal reading list and book tracker", False, False),
    ("RheumaLog", "rheumalog", "rheumatoid arthritis symptom and pain tracking", True, True),
    ("SkinLog", "skinlog", "skin condition and skincare routine tracking", True, True),
    ("SoberStreak", "soberstreak", "sobriety milestones and recovery tracking", True, True),
    ("StepUp", "stepup", "step counting and walking goal tracking", True, True),
    ("SubSync", "subsync", "subscription management and expense tracking", False, False),
    ("ThyroidLog", "thyroidlog", "thyroid condition and symptom tracking", True, True),
    ("TinnitusLog", "tinnituslog", "tinnitus symptoms and sound sensitivity tracking", True, True),
    ("TipTracker", "tiptracker", "tip calculation and bill splitting", False, False),
    ("VocabBoost", "vocabboost", "vocabulary building and word learning", False, False),
    ("WorkoutLog", "workoutlog", "workout logging and fitness tracking", True, True),
]

CSS = """/* app-legal shared stylesheet */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #ffffff;
  --surface: #f9f9f9;
  --border: #e5e5e5;
  --text: #1a1a1a;
  --muted: #666666;
  --accent: #0066cc;
  --accent-dark: #004a99;
  --max-width: 780px;
  --radius: 8px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f0f0f;
    --surface: #1a1a1a;
    --border: #2e2e2e;
    --text: #f0f0f0;
    --muted: #999999;
    --accent: #4da6ff;
    --accent-dark: #80bdff;
  }
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  font-size: 16px;
  padding: 0 1rem;
}

.container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 3rem 0 5rem;
}

header {
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.app-tag {
  display: inline-block;
  background: var(--accent);
  color: #fff;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 0.25rem 0.65rem;
  border-radius: 4px;
  margin-bottom: 0.75rem;
}

h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
  letter-spacing: -0.02em;
}

.meta {
  color: var(--muted);
  font-size: 0.9rem;
}

h2 {
  font-size: 1.15rem;
  font-weight: 600;
  margin: 2rem 0 0.6rem;
  color: var(--text);
}

p { margin-bottom: 1rem; color: var(--text); }

ul {
  margin: 0.4rem 0 1rem 1.4rem;
  color: var(--text);
}

li { margin-bottom: 0.3rem; }

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; color: var(--accent-dark); }

.section {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.4rem 1.6rem;
  margin-bottom: 1.25rem;
}

.section h2 { margin-top: 0; }

.nav-links {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.nav-links a {
  font-size: 0.9rem;
  color: var(--accent);
}

.badge {
  display: inline-block;
  background: #e8f4e8;
  color: #2d7a2d;
  font-size: 0.78rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  margin-left: 0.4rem;
}

@media (prefers-color-scheme: dark) {
  .badge { background: #1a3a1a; color: #6db86d; }
}

footer {
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  color: var(--muted);
  font-size: 0.85rem;
}

footer a { color: var(--muted); }

/* Index page specific */
.app-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.app-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.1rem 1.3rem;
  transition: border-color 0.15s;
}

.app-card:hover { border-color: var(--accent); }

.app-card h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.6rem;
}

.app-card .desc {
  font-size: 0.83rem;
  color: var(--muted);
  margin-bottom: 0.8rem;
}

.app-card .links {
  display: flex;
  gap: 0.75rem;
  font-size: 0.83rem;
}

.search-box {
  width: 100%;
  max-width: 400px;
  padding: 0.6rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  color: var(--text);
  font-size: 0.95rem;
  margin: 1rem 0;
}

.search-box:focus {
  outline: 2px solid var(--accent);
  border-color: var(--accent);
}

@media (max-width: 600px) {
  h1 { font-size: 1.5rem; }
  .container { padding: 2rem 0 4rem; }
  .app-grid { grid-template-columns: 1fr; }
}
"""

PRIVACY_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{app_name} — Privacy Policy</title>
  <link rel="stylesheet" href="../../styles.css">
</head>
<body>
<div class="container">
  <header>
    <div class="app-tag">{app_name}</div>
    <h1>Privacy Policy</h1>
    <p class="meta">Effective date: {effective_date} &nbsp;·&nbsp; Developer: {developer}</p>
    <div class="nav-links">
      <a href="terms.html">Terms of Service →</a>
      <a href="../../index.html">← All Apps</a>
    </div>
  </header>

  <div class="section">
    <h2>Overview</h2>
    <p>Your privacy is fundamental to {app_name}. This app is designed to help you with {description}. All data you enter stays on your device — always.</p>
  </div>

  <div class="section">
    <h2>Data We Collect</h2>
    <p>The only data {app_name} collects is what <strong>you choose to enter</strong> into the app. This includes:</p>
    <ul>
      <li>Logs, entries, and records you create within the app</li>
      <li>App settings and preferences you configure</li>
      {health_data_item}
    </ul>
    <p>All data is stored <strong>locally on your device</strong> using Apple's SwiftData framework. Nothing is uploaded to any server.</p>
  </div>

  <div class="section">
    <h2>Data Storage &amp; Security</h2>
    <ul>
      <li><strong>Local only:</strong> All app data is stored on your device using SwiftData</li>
      <li><strong>No cloud sync:</strong> Your data does not sync to any cloud service (including iCloud)</li>
      <li><strong>No remote servers:</strong> {app_name} does not have any backend servers or databases</li>
      <li><strong>No analytics:</strong> We do not use analytics tools, crash reporters, or performance trackers</li>
      <li><strong>No third-party SDKs:</strong> The app contains no third-party frameworks that collect data</li>
    </ul>
  </div>

  {healthkit_section}

  <div class="section">
    <h2>Payments &amp; Subscriptions</h2>
    <p>If {app_name} offers in-app purchases or subscriptions, all transactions are handled exclusively through <strong>Apple's App Store and StoreKit</strong>. Orca AI never sees, stores, or processes your payment information. Apple's privacy policy governs all payment data.</p>
    <p>Subscriptions are auto-renewable and can be managed or cancelled at any time in your iOS Settings → Apple ID → Subscriptions.</p>
  </div>

  <div class="section">
    <h2>No Account Required</h2>
    <p>{app_name} requires no account, no registration, no email address, and no sign-in. The app works entirely offline and independently of any online service.</p>
  </div>

  <div class="section">
    <h2>No Tracking or Advertising</h2>
    <p>We do not track you, advertise to you, or share your data with advertisers or data brokers. {app_name} contains no advertising frameworks, behavioral tracking, or cross-app tracking of any kind.</p>
    <p>{app_name} will request <strong>App Tracking Transparency (ATT)</strong> permission only if required — and will function identically regardless of your choice.</p>
  </div>

  <div class="section">
    <h2>Data Deletion</h2>
    <p>You have complete control over your data:</p>
    <ul>
      <li><strong>In-app deletion:</strong> Navigate to Settings within {app_name} to delete all your data</li>
      <li><strong>Full deletion:</strong> Deleting the app from your device permanently removes all associated data</li>
    </ul>
    <p>We cannot recover deleted data, as we never had access to it in the first place.</p>
  </div>

  <div class="section">
    <h2>Children's Privacy</h2>
    <p>{app_name} is not directed at children under the age of 13. We do not knowingly collect personal information from children under 13. If you are a parent or guardian and believe your child has used the app, please contact us — though as noted above, no data leaves the device.</p>
  </div>

  <div class="section">
    <h2>Changes to This Policy</h2>
    <p>If we make material changes to this Privacy Policy, we will update the effective date above. We encourage you to review this policy periodically. Continued use of the app constitutes acceptance of any updates.</p>
  </div>

  <div class="section">
    <h2>Contact Us</h2>
    <p>Questions about privacy? We're happy to help.</p>
    <p><strong>Orca AI</strong><br>
    Email: <a href="mailto:{email}">{email}</a></p>
  </div>

  <footer>
    <p>© 2026 Orca AI · <a href="mailto:{email}">{email}</a></p>
  </footer>
</div>
</body>
</html>
"""

TERMS_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{app_name} — Terms of Service</title>
  <link rel="stylesheet" href="../../styles.css">
</head>
<body>
<div class="container">
  <header>
    <div class="app-tag">{app_name}</div>
    <h1>Terms of Service</h1>
    <p class="meta">Effective date: {effective_date} &nbsp;·&nbsp; Developer: {developer}</p>
    <div class="nav-links">
      <a href="privacy.html">Privacy Policy →</a>
      <a href="../../index.html">← All Apps</a>
    </div>
  </header>

  <div class="section">
    <h2>Acceptance of Terms</h2>
    <p>By downloading or using {app_name}, you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use the app.</p>
  </div>

  <div class="section">
    <h2>License to Use</h2>
    <p>Orca AI grants you a personal, non-exclusive, non-transferable, revocable license to use {app_name} on Apple devices you own or control, subject to these Terms and the <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/" target="_blank" rel="noopener">Apple Standard EULA</a>.</p>
    <p>You may not:</p>
    <ul>
      <li>Copy, modify, or distribute the app or its content</li>
      <li>Reverse engineer, decompile, or disassemble the app</li>
      <li>Use the app for any unlawful purpose</li>
      <li>Attempt to circumvent any security or access controls</li>
    </ul>
  </div>

  <div class="section">
    <h2>Subscriptions &amp; Payments</h2>
    <p>If {app_name} offers auto-renewable subscriptions:</p>
    <ul>
      <li>Subscriptions are charged to your Apple ID at confirmation of purchase</li>
      <li>Subscriptions automatically renew unless cancelled at least 24 hours before the end of the current period</li>
      <li>Renewal charges are made within 24 hours before the period ends at the same price</li>
      <li>You can manage and cancel subscriptions in your iOS Settings → Apple ID → Subscriptions</li>
      <li>No refunds are provided for partial subscription periods, subject to Apple's refund policies</li>
    </ul>
    <p>All payments are processed by Apple. Orca AI does not store payment information.</p>
  </div>

  {medical_disclaimer}

  <div class="section">
    <h2>App Provided "As Is"</h2>
    <p>{app_name} is provided on an <strong>"as is" and "as available"</strong> basis without warranties of any kind, either express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, or non-infringement.</p>
    <p>We do not warrant that:</p>
    <ul>
      <li>The app will be uninterrupted, timely, secure, or error-free</li>
      <li>The results obtained from use of the app will be accurate or reliable</li>
      <li>Any errors in the app will be corrected</li>
    </ul>
  </div>

  <div class="section">
    <h2>Limitation of Liability</h2>
    <p>To the fullest extent permitted by applicable law, Orca AI and its affiliates, officers, directors, employees, and agents shall not be liable for any indirect, incidental, special, consequential, or punitive damages, including but not limited to loss of data, loss of profits, or personal injury, arising out of or in connection with your use of {app_name}.</p>
    <p>In no event shall Orca AI's total liability to you exceed the amount you paid for the app in the twelve (12) months preceding the claim.</p>
  </div>

  <div class="section">
    <h2>User Data &amp; Content</h2>
    <p>Any data you enter into {app_name} remains yours. As outlined in our <a href="privacy.html">Privacy Policy</a>, all data is stored locally on your device. We do not claim ownership of your content.</p>
    <p>You are responsible for maintaining backups of your data. Orca AI is not responsible for data loss resulting from app deletion, device issues, or other causes.</p>
  </div>

  <div class="section">
    <h2>Intellectual Property</h2>
    <p>The {app_name} app, including its design, code, graphics, and content (excluding user-entered data), is the intellectual property of Orca AI and is protected by applicable copyright, trademark, and other intellectual property laws.</p>
  </div>

  <div class="section">
    <h2>Third-Party Services</h2>
    <p>The App Store and in-app purchases are governed by Apple Inc.'s terms and privacy policies. We are not responsible for the practices of Apple or any other third-party service you may interact with in connection with the app.</p>
  </div>

  <div class="section">
    <h2>Changes to Terms</h2>
    <p>We reserve the right to modify these Terms at any time. We will update the effective date when changes are made. Continued use of {app_name} after changes constitutes acceptance of the revised Terms.</p>
  </div>

  <div class="section">
    <h2>Governing Law</h2>
    <p>These Terms are governed by and construed in accordance with the laws of the <strong>State of California, USA</strong>, without regard to its conflict of law provisions. Any disputes shall be subject to the exclusive jurisdiction of the courts located in California.</p>
  </div>

  <div class="section">
    <h2>Contact Us</h2>
    <p>Questions about these Terms? Contact us:</p>
    <p><strong>Orca AI</strong><br>
    Email: <a href="mailto:{email}">{email}</a></p>
  </div>

  <footer>
    <p>© 2026 Orca AI · <a href="mailto:{email}">{email}</a></p>
  </footer>
</div>
</body>
</html>
"""

HEALTHKIT_SECTION = """\
  <div class="section">
    <h2>HealthKit Integration <span class="badge">HealthKit</span></h2>
    <p>{app_name} may request access to Apple HealthKit to read and/or write health data relevant to {description}. This is <strong>optional</strong> — the app functions without HealthKit access.</p>
    <ul>
      <li>HealthKit data is accessed only with your explicit permission</li>
      <li>Data read from HealthKit is used solely within the app to enhance your experience</li>
      <li>We never upload HealthKit data to any server or share it with third parties</li>
      <li>HealthKit data is not used for advertising or sold to data brokers</li>
      <li>You can revoke HealthKit access at any time in iOS Settings → Privacy &amp; Security → Health</li>
    </ul>
  </div>
"""

MEDICAL_DISCLAIMER = """\
  <div class="section">
    <h2>No Medical Advice</h2>
    <p><strong>IMPORTANT:</strong> {app_name} is designed for personal tracking and informational purposes only. The app is <strong>not a medical device</strong> and does not provide medical advice, diagnosis, or treatment.</p>
    <ul>
      <li>Information logged in {app_name} is not a substitute for professional medical advice</li>
      <li>Always consult a qualified healthcare provider for medical decisions</li>
      <li>Do not disregard professional medical advice because of something you tracked or read in this app</li>
      <li>In case of a medical emergency, call emergency services immediately</li>
    </ul>
  </div>
"""

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Orca AI — App Legal Documents</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="container">
  <header>
    <div class="app-tag">Orca AI</div>
    <h1>App Legal Documents</h1>
    <p class="meta">Privacy Policies &amp; Terms of Service for all {count} apps by Orca AI</p>
    <p style="margin-top:0.75rem; color:var(--muted); font-size:0.9rem;">
      Developer: <a href="mailto:{email}">{email}</a> &nbsp;·&nbsp; Effective: {effective_date}
    </p>
  </header>

  <input type="search" class="search-box" id="search" placeholder="Search apps…" oninput="filterApps(this.value)">

  <div class="app-grid" id="appGrid">
{app_cards}
  </div>

  <footer>
    <p>© 2026 Orca AI &nbsp;·&nbsp; <a href="mailto:{email}">{email}</a> &nbsp;·&nbsp;
    All apps developed independently. No data leaves your device.</p>
  </footer>
</div>
<script>
function filterApps(q) {{
  const grid = document.getElementById('appGrid');
  const cards = grid.querySelectorAll('.app-card');
  const lq = q.toLowerCase();
  cards.forEach(c => {{
    const text = c.textContent.toLowerCase();
    c.style.display = text.includes(lq) ? '' : 'none';
  }});
}}
</script>
</body>
</html>
"""

APP_CARD_TEMPLATE = """\
    <div class="app-card" data-app="{slug}">
      <h3>{app_name}{health_badge}</h3>
      <p class="desc">{description_cap}</p>
      <div class="links">
        <a href="{slug}/privacy.html">Privacy Policy</a>
        <a href="{slug}/terms.html">Terms of Service</a>
      </div>
    </div>"""


def generate_privacy(app_name, slug, description, has_healthkit):
    health_data_item = "<li>Health and wellness data you manually log in the app</li>" if has_healthkit else ""
    healthkit_section = HEALTHKIT_SECTION.format(app_name=app_name, description=description) if has_healthkit else ""
    return PRIVACY_TEMPLATE.format(
        app_name=app_name,
        slug=slug,
        description=description,
        has_healthkit=has_healthkit,
        health_data_item=health_data_item,
        healthkit_section=healthkit_section,
        effective_date=EFFECTIVE_DATE,
        developer=DEVELOPER,
        email=EMAIL,
    )


def generate_terms(app_name, slug, description, is_health_app):
    medical_disclaimer = MEDICAL_DISCLAIMER.format(app_name=app_name) if is_health_app else ""
    return TERMS_TEMPLATE.format(
        app_name=app_name,
        slug=slug,
        description=description,
        is_health_app=is_health_app,
        medical_disclaimer=medical_disclaimer,
        effective_date=EFFECTIVE_DATE,
        developer=DEVELOPER,
        email=EMAIL,
    )


def main():
    base = os.path.expanduser("~/projects/app-factory/legal-pages")

    # Write shared CSS
    with open(os.path.join(base, "styles.css"), "w") as f:
        f.write(CSS)
    print("✓ styles.css")

    # Generate app pages
    app_cards = []
    for app_name, slug, description, has_healthkit, is_health_app in APPS:
        app_dir = os.path.join(base, slug)
        os.makedirs(app_dir, exist_ok=True)

        privacy_html = generate_privacy(app_name, slug, description, has_healthkit)
        terms_html = generate_terms(app_name, slug, description, is_health_app)

        with open(os.path.join(app_dir, "privacy.html"), "w") as f:
            f.write(privacy_html)
        with open(os.path.join(app_dir, "terms.html"), "w") as f:
            f.write(terms_html)

        health_badge = ' <span class="badge">HealthKit</span>' if has_healthkit else ''
        description_cap = description[0].upper() + description[1:]
        app_cards.append(APP_CARD_TEMPLATE.format(
            app_name=app_name,
            slug=slug,
            health_badge=health_badge,
            description_cap=description_cap,
        ))

        print(f"✓ {app_name} ({slug})")

    # Generate index
    index_html = INDEX_TEMPLATE.format(
        count=len(APPS),
        email=EMAIL,
        effective_date=EFFECTIVE_DATE,
        app_cards="\n".join(app_cards),
    )
    with open(os.path.join(base, "index.html"), "w") as f:
        f.write(index_html)
    print(f"✓ index.html ({len(APPS)} apps)")

    print(f"\n✅ Generated {len(APPS) * 2 + 2} files total ({len(APPS)} privacy + {len(APPS)} terms + styles.css + index.html)")


if __name__ == "__main__":
    main()
