# YouTube Faceless AI Shorts — iPad Kids Channel

## Concept
A fully automated, faceless YouTube Shorts channel targeting kids aged 3–8 who watch on iPads. All content generated with AI: visuals, voiceover, music, and captions. No camera, no presenter, no editing skills required.

---

## Target Audience
- Age: 3–8 years old
- Device: iPad (vertical screen, touch-first UX)
- Watch context: unsupervised, bedtime, car rides, mealtime
- Parents: want safe, calm, educational-ish content

---

## Content Pillars

### 1. Alphabet & Numbers
- "A is for Apple" style — bright Pixar-like visuals, slow voiceover, catchy jingle
- Tools: Midjourney / DALL-E for frames, ElevenLabs for voice, CapCut for assembly

### 2. Colors & Shapes
- "What color is this?" interactive-style questions with answers
- High contrast visuals optimized for small screens

### 3. Animals & Sounds
- "What does the cow say?" — realistic AI animal images + real sound effects
- Super high retention with toddlers

### 4. Simple Stories (30–60 sec)
- 3-frame micro-stories: problem → adventure → resolution
- Calm narrator voice, no scary elements, happy ending always

### 5. Lullaby / Wind-Down Shorts
- Soft AI animations + AI-generated lullaby music
- Targets bedtime iPad use — parents actively search this

---

## Automated Build Pipeline (Claude-built system)

```
Cron (2x/day on Railway)
    → Claude API        — generates nursery rhyme script + scene-by-scene breakdown
    → DALL-E 3          — generates one image per scene (1080x1920 vertical)
    → ElevenLabs        — English voiceover, kids-friendly voice
    → MoviePy           — assembles images + audio + burned-in captions into MP4
    → YouTube Data API  — uploads with title, tags, Made for Kids flag set
```

**Cost per video:** ~$0.10–$0.30 in API calls (pay-per-use, no SaaS subscriptions)  
**Runs:** fully unattended, 2x per day automatically  
**Reusable for:** any faceless YouTube niche — swap the prompt, same system

### APIs Needed to Start
| Service | What it does | Get key at |
|---------|-------------|------------|
| Anthropic | Script generation | console.anthropic.com |
| OpenAI | DALL-E 3 images | platform.openai.com |
| ElevenLabs | Kids voiceover | elevenlabs.io |
| Google / YouTube | Auto-upload | console.cloud.google.com |

### Hosting
- **Railway** — runs the Python pipeline on a cron schedule (2x/day)
- GitHub auto-deploy from `youtube1` repo

---

## Upload Strategy
- 2–3 Shorts per day (automated, no manual work)
- Best upload times: 6–9am, 12–2pm, 6–9pm (parent-managed iPad time)
- Titles: simple, searchable — "A B C for Kids | Alphabet Song Shorts"
- Tags: #kidsshorts #abcforkids #toddlerlearning #preschool #funforkids

---

## Monetization Path
1. **YouTube Shorts AdSense** — once 500 subs + 3M Shorts views in 90 days
2. **Merch** — printable flashcards, coloring pages (Gumroad)
3. **Affiliate** — kids apps, educational toys (Amazon Associates)
4. **Sponsorships** — kids app developers pay well for kid-audience channels
5. **Licensing** — sell video packs to other kids channels

### Realistic Earnings Timeline
| Stage | Views/month | Est. Revenue |
|-------|------------|--------------|
| Starting out | 0–100k | $0 |
| Growing | 500k–1M | $50–$200 |
| Established | 5M–10M | $500–$2,000 |
| Big channel | 50M+ | $5,000–$20,000+ |

Note: kids CPM is low ($1–$3) due to COPPA — volume and merch are the real play.

---

## Growth Hooks
- End every Short with a cliffhanger question: "Can you guess what comes next?"
- Use bright thumbnail stills (YouTube auto-picks best frame — choose wisely)
- Series format drives replays: "Letter A... Letter B... Letter C..."
- Comment bait for parents: "Which letter should we do next?"

---

## Tools Stack

| Task | Tool |
|------|------|
| Script | Claude API (Anthropic) |
| Images | DALL-E 3 (OpenAI) |
| Voiceover | ElevenLabs |
| Video assembly | MoviePy (Python) |
| Captions | Burned-in via MoviePy |
| Scheduling | Railway cron |
| Upload | YouTube Data API v3 |

---

## 30-Day Launch Plan

| Week | Goal |
|------|------|
| Week 1 | Set up channel, brand, workflow — publish 5 test Shorts |
| Week 2 | Daily uploads, A/B test thumbnails & titles |
| Week 3 | Double down on top-performing format |
| Week 4 | 60+ videos live, analyze retention data, optimize |

---

## KPIs to Track
- Views per Short (first 48h)
- Swipe-away rate (keep under 60%)
- Average view duration (aim for 80%+)
- Subscriber growth rate
- Comments from parents (social proof)

---

## Notes
- Never use scary sounds, sudden loud noises, or fast cuts — kids (and YouTube algo) penalize this
- Always add closed captions — helps with SEO and accessibility
- Keep branding consistent: same outro jingle, same color palette, same font
- Check YouTube's MADE FOR KIDS setting — must be set correctly to avoid policy issues
