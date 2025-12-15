# Social Media Manager - Project Brief & Implementation Guide

**Document Version:** 2.0  
**Created:** November 10, 2025  
**Last Updated:** November 15, 2025  
**Test Case Client:** Smoothie Bar (Cannabis Vape Brand)  
**Purpose:** Complete specification for building a universal social media management automation system

---

## 🔄 ARCHITECTURAL REVISION (Nov 15, 2025)

### Key Decision: Buffer + Make Integration Instead of Instagram Graph API

**Decision Made:** Build custom planning/content system that integrates with Buffer (via Make automation) rather than direct Instagram Graph API integration.

### Rationale

**Why NOT Graph API:**
- ❌ Complex authentication flow (Facebook Developer account, app review process)
- ❌ Frequent API changes and deprecations
- ❌ Rate limiting issues and reliability concerns
- ❌ Requires ongoing maintenance for Instagram's changing requirements
- ❌ Difficult debugging when things break
- ❌ Several week delay for app approval process
- ❌ Does not support all Instagram features (Stories/Reels are limited)

**Why Buffer + Make:**
- ✅ **Safety & Reliability:** Battle-tested posting infrastructure
- ✅ **Speed to Market:** Can start building immediately, no API approval wait
- ✅ **Simplicity:** No authentication headaches, Buffer handles Instagram relationship
- ✅ **Maintenance-Free:** Buffer updates when Instagram changes, we don't
- ✅ **Focus on Core Value:** We build planning/content tools, not posting infrastructure
- ✅ **Cost-Effective:** $6/mo Buffer + Free Make tier vs. enterprise API costs
- ✅ **Proven Integration:** Make + Buffer already works for thousands of users

### Revised System Architecture

**The Flow:**
```
YOUR PYTHON SYSTEM (Planning & Content Creation)
    ↓ (exports to)
GOOGLE SHEETS (Bridge/Data Store)
    ↓ (monitored by)
MAKE (Automation Glue - Free tier)
    ↓ (sends to)
BUFFER (Queue & Posting - $6/mo)
    ↓ (you review/approve)
BUFFER (Auto-posts to Instagram)
    ↓
INSTAGRAM (Posts go live)
    ↓
ICONOSQUARE (Analytics - manual check or auto-export)
```

### What Your Custom System DOES Build

**Core Competitive Advantages:**
1. **Comprehensive Monthly Planning** - ALL Instagram content types:
   - Feed Posts (12-16/month)
   - Stories (daily series, 20-25/month)
   - Reels (2-3/month with scripts)
   - Story Highlights (updates/new categories)
   - Engagement activities
   - Special campaigns

2. **AI Content Assistant** - Learns brand voice specifically:
   - Caption drafts that improve over time
   - Real-time editing suggestions
   - Brand voice scoring
   - Hashtag optimization

3. **Team Presentation Tools** - THE MAIN VALUE:
   - Beautiful PDF strategy decks
   - Shareable web links for review
   - Google Sheets exports for collaboration
   - Visual calendar presentations
   - **Present complete monthly plan to team BEFORE execution begins**

4. **Media Management:**
   - Library with auto-tagging
   - Link media to planned posts
   - Resource requisition tracking

5. **Execution Support:**
   - Copy/paste ready checklists for Stories/Reels
   - Automated feed post sync to Buffer
   - Progress tracking
   - Status management

6. **Analytics Dashboard:**
   - Pull from Iconosquare/Metricool
   - Custom visualizations
   - Weekly/monthly reports
   - Trend analysis

### What Your Custom System does NOT Build

**Delegated to Proven Tools:**
- ❌ Instagram authentication/API connection (Buffer handles)
- ❌ Post scheduling logic (Buffer handles)
- ❌ Actual posting infrastructure (Buffer handles)
- ❌ Deep analytics engine (Iconosquare handles)
- ❌ Rate limiting/retry logic (Make + Buffer handle)

### Technology Stack (Updated)

**Your Custom Application:**
- **Frontend/Backend:** Streamlit (all-in-one Python web framework)
- **AI:** Claude API (Anthropic)
- **Data Bridge:** Google Sheets API (gspread library)
- **Hosting:** Streamlit Cloud (free) or local

**Third-Party Services:**
- **Posting:** Buffer ($6/mo for Essentials)
- **Automation:** Make (free tier, up to 1,000 operations/month)
- **Analytics:** Iconosquare (trial, then $49/mo) OR Metricool ($12/mo with API)
- **Data Storage:** Google Sheets (free)

**Total Monthly Cost:** $6-55/month (vs. $100+ for all-in-one enterprise tools)

### Content Type Handling Strategy

**Feed Posts (Automated to Buffer):**
- Your system creates caption + hashtags
- Exports to Google Sheets
- Makes automatically Add to Buffer queue
- You review in Buffer
- Buffer auto-posts

**Stories & Reels (Manual with Smart Checklists):**
- Your system creates scripts/copy for all slides
- Generates downloadable ZIP with:
  - All media files
  - Text file with copy for each slide
  - Step-by-step posting checklist
- You manually post to IG (2-3 minutes)
- System tracks as "completed"

**Why This Hybrid Approach:**
- Buffer's Story/Reel support is limited
- Manual posting gives you final creative control
- System still does 90% of the work (planning + content prep)
- Total time saved: Still 10+ hours/week

### Emphasis on Planning & Presentation

**THE CORE VALUE PROPOSITION:**

This is primarily a **PLANNING and STRATEGY TOOL**, not just automation.

**Monthly Workflow:**
1. **Last week of month:** Generate next month's complete plan (30 mins)
2. **Export beautiful presentation:** PDF deck + shareable links
3. **Present to team:** Get buy-in on strategy BEFORE execution
4. **Receive feedback:** Team edits/approves in Google Sheets
5. **Finalize plan:** Lock in the calendar
6. **Execute throughout month:** Use system for content creation + posting

**This eliminates:**
- ❌ Last-minute "what should we post?"
- ❌ Reactive content creation
- ❌ Misalignment with team
- ❌ Missing opportunities (events, trends)
- ❌ Stress and burnout

**This enables:**
- ✅ Strategic, intentional content month-ahead
- ✅ Team alignment and buy-in
- ✅ Professional presentations to stakeholders
- ✅ Resource planning (photo shoots, interviews scheduled in advance)
- ✅ Calm, organized execution

---

## EXECUTIVE SUMMARY

### What We're Building
A comprehensive social media management automation system that helps non-technical people manage Instagram (and eventually other platforms) professionally. The system assists with planning, content creation, media management, deployment, engagement, and analytics.

### Why We're Building It
Current social media management requires juggling multiple tools, manual posting, inconsistent engagement, and reactive rather than proactive planning. This system centralizes everything into one cohesive workflow that works 1 month ahead, reducing stress and improving quality.

### First Use Case: Smoothie Bar
Smoothie Bar is a cannabis vape brand launching on Instagram. They have:
- Completed brand strategy with 5 content pillars
- "Will it Blend?" series (5 posts ready for production)
- Consumer Education content started
- Need to scale to consistent posting schedule
- Perfect test case for the automation system

---

## PART 1: SMOOTHIE BAR CONTEXT (The Test Case)

### Brand Overview

**Brand Name:** Smoothie Bar  
**Product:** Dual-tank ceramic-coil cannabis vapes (Blend Collection)  
**Unique Value Prop:** Only vape that lets you experience two strains separately OR blended together  
**Target Audience:** Cannabis-positive LA residents aged 21-35 (creatives, industry professionals, lifestyle enthusiasts)  
**Brand Voice:** Culturally curious, knowledgeable but never pretentious, genuinely enthusiastic about cannabis and creativity

### Strategic Positioning
- Authentic voice of LA cannabis culture
- Curator/tastemaker (not pushy advertiser)
- Educational authority building trust through expertise
- Professional tone with strategic authenticity
- Focus on craftsmanship and curation process

### Instagram Strategy (5 Content Pillars)

**1. Flavor Spotlights**
- Posts explaining strain combinations and effects
- Flagship series: "Will it Blend?"
- 4-slide carousel format
- Educational focus on terpenes, genetics, flavor profiles

**2. Cultural Documentaries**
- Features on LA creatives (artists, musicians, skaters)
- Shows cannabis in authentic lifestyle context
- Multi-part interviews
- Behind-the-scenes of creative process

**3. Consumer Education**
- Teaching cannabis basics in accessible ways
- COA (Certificate of Analysis) education
- Lab results interpretation
- Vape temperature optimization
- Terpene education

**4. Community Engagement**
- Polls and discussion starters
- Giveaway campaigns
- Educational quizzes
- Brand updates
- Culture-focused questions

**5. Behind-the-Scenes**
- Authentic glimpses into brand creation
- Production process
- Sourcing decisions
- Team culture
- Transparency content

### Completed Work (What Exists Now)

**"Will it Blend?" Series (5 Posts - Production Ready)**

1. **Series Introduction** (Published Sept 8, 2025)
   - Introduced concept behind strain combinations
   - Explained dual-tank technology
   - Teased 4 upcoming combinations
   - Call-to-action for community suggestions

2. **Truffle Butter x Blue Dream** (Ready for production)
   - Luxury meets legend theme
   - When California's beloved classic elevates an indulgent newcomer
   - Full genetic lineage included for graphics team

3. **Lava Pop x Tropicana** (Ready for production)
   - Fire and citrus balance
   - Sweet-and-heat combination
   - Genetic lineage complete

4. **Cannalope Haze x Snow Cone** (Ready for production)
   - Summer vibes: melon sweetness with uplifting hybrid refreshment
   - Genetic lineage complete

5. **Dark Web x Agent Orange** (Ready for production)
   - Gassy candy meets fresh oranges
   - Decadent and irresistible
   - Genetic lineage complete

**Consumer Education Pillar**
- Comprehensive COA guide post (ready for production)
- Visual guide methodology established
- Technical terminology explanations
- Educational authority positioning

**Supporting Documentation**
- Product descriptions (multiple versions for different contexts)
- Instagram strategy executive summaries
- Content calendar templates
- Interview frameworks (lifestyle, street interviews)
- Giveaway frameworks
- 30-day onboarding plans

### Brand Voice Guidelines (Critical for AI Content Assistance)

**DO:**
- Use natural, conversational tone
- Lead with compelling hooks (avoid repetitive "Ever wonder..." openings)
- Food analogies for flavor descriptions
- Cultural and geographic references
- Direct, engaging language
- Incorporate emojis strategically (not excessively)
- Strong calls-to-action focused on community/culture
- Educational without being preachy

**DON'T:**
- Sound overly polished or AI-generated
- Make specific terpene percentage claims
- Mention breeders by name (compliance)
- Use overly technical jargon without explanation
- Sound corporate or sales-y
- Use repetitive intro structures
- Start with "Great", "Certainly", "Okay", "Sure"

**Example of Good Brand Voice:**
"Will it Blend? It's the question behind every Smoothie Bar: Blend product, and we're bringing you along for the journey that follows every strain pairing we create."

**Example of Bad Brand Voice:**
"Certainly! We're excited to introduce our new product line. Our ceramic coil technology is really good and we think you'll love it."

### Visual Strategy

**Post Format:** 4-slide carousels (standard)

**Slide Structure:**
1. Title/hook with brand logo
2. Visual content (product, lifestyle, or educational imagery)
3. Detail/explanation slides
4. Call-to-action with community engagement prompt

**Image Specs:**
- Square format: 1080x1080px
- File size: <5MB
- Professional quality
- White backgrounds perform 40% better (proven through testing)

**Hashtag Strategy:**
- 15-20 hashtags per post
- Mix of series-specific, educational, and broader cannabis tags
- Examples: #WillItBlend #CannabisEducation #LAcannabis #DualTank #StrainPairing

### Success Metrics (What Smoothie Bar Measures)
- Quality engagement over follower count
- Brand association with authentic LA culture
- Community trust and participation
- Educational content authority
- Product inquiry and sales attribution
- Engagement rate benchmarks: 8-10% considered excellent

### Current Status & Gaps

**✅ COMPLETED:**
- Full strategy framework
- Brand voice defined and refined
- "Will it Blend?" series complete (5 posts)
- Consumer Education pillar started (1 post)
- Product descriptions finalized
- Visual strategy locked in

**❌ GAPS (What the Automation System Will Help With):**
- No consistent posting schedule or calendar
- Manual deployment process (time-consuming)
- No systematic engagement strategy
- No analytics tracking or reporting
- Cultural Documentary content not started
- Community Engagement content needs development
- No monthly planning workflow
- Media management is disorganized
- No automation for repetitive tasks

---

## PART 2: AUTOMATION SYSTEM REQUIREMENTS

### System Philosophy
**Human controls creativity and strategy. System handles automation, tedious work, and optimization.**

### Core Design Principles
1. **1-Month Ahead Planning:** Always working 30+ days in advance
2. **AI as Assistant, Not Creator:** AI suggests, humans decide
3. **Non-Technical User Focused:** Simple interface, minimal learning curve
4. **Separation of Concerns:** Tool code separate from client content
5. **Resilient & Forgiving:** Graceful error handling, undo functionality
6. **Future-Proof:** Built with modern, stable technologies

---

## PHASE 0: INITIAL SETUP & CONFIGURATION

### Purpose
Configure the system once with brand information, templates, and preferences before starting monthly workflows.

### Required Data Input (From Client)

**Brand Profile:**
- Company name, industry, target audience
- Brand voice examples (5-10 past successful posts)
- Content pillars definition
- Posting frequency preference
- Visual style guidelines

**Integration Setup:**
- Instagram Business account credentials (Graph API)
- Syncthing folder paths for media sync
- Notification preferences (email/in-app)
- Timezone configuration

**Template Library:**
- Caption templates with placeholders
- Hashtag categories (broad, niche, branded)
- Response templates for common comments
- Media requisition templates

### Smoothie Bar Specific Configuration

```json
{
  "brand_profile": {
    "name": "Smoothie Bar",
    "industry": "Cannabis/Vape",
    "target_audience": "LA cannabis-positive adults 21-35",
    "brand_voice_keywords": ["authentic", "curious", "knowledgeable", "cultural"],
    "content_pillars": [
      "Flavor Spotlights",
      "Cultural Documentaries",
      "Consumer Education",
      "Community Engagement",
      "Behind-the-Scenes"
    ],
    "posting_frequency": "4x per week",
    "optimal_times": ["Tuesday 6PM", "Thursday 6-7PM"],
    "visual_style": "Professional, white backgrounds preferred, product-focused"
  },
  "caption_templates": [
    {
      "name": "Will it Blend Format",
      "structure": "[Hook Question] + [Strain Details] + [Curation Philosophy] + [Community CTA]",
      "example_post_id": "002_truffle_butter_blue_dream"
    },
    {
      "name": "Educational Format",
      "structure": "[Problem Statement] + [Explanation] + [How We Solve It] + [CTA]",
      "example_post_id": "001_coa_guide"
    }
  ],
  "hashtag_categories": {
    "series_specific": ["#WillItBlend", "#SmoothieBarBlend"],
    "educational": ["#CannabisEducation", "#COAeducation", "#TerpeneEducation"],
    "location": ["#LAcannabis", "#CaliforniaCannabis"],
    "product": ["#DualTank", "#CeramicCoil", "#VapeQuality"],
    "general": ["#CannabisConnoisseur", "#StrainPairing"]
  },
  "voice_examples": [
    {
      "post_id": "001_will_it_blend_intro",
      "why_good": "Natural hook, educational without being preachy, strong community CTA"
    }
  ]
}
```

### Success Criteria
- Brand profile loaded and visible in UI
- Instagram API connection verified
- Templates accessible for content creation
- Media sync folders configured

---

## PHASE 1: MONTHLY PLANNING & CALENDAR GENERATION

### Purpose
Generate a complete 30-day content plan that can be reviewed and modified BEFORE content creation starts. This eliminates last-minute posting and allows team collaboration.

### Monthly Plan Components

**1. Regular Posts (12-16 per month)**
Each post includes:
- Specific date and optimal time
- Content pillar assignment (rotated evenly)
- Topic/theme suggestion (AI-generated based on pillars)
- Media type needed (product photo, lifestyle, infographic)
- Hashtag category to use
- Priority level (normal/high)
- Status tracking (planned → needs_content → needs_media → ready → posted)

**2. Auxiliary Content**
- Stories: 3-5 story series per week
- Reels: 2-3 per month (if applicable)
- Story highlight categories
- Behind-the-scenes opportunities

**3. Engagement Strategy**
- Target accounts list (competitors, industry leaders, potential customers)
- Daily engagement goals (like X posts, comment on Y, follow Z)
- Response templates for common comments
- DM outreach targets (influencers, partnerships)

**4. Key Dates & Events**
- Industry events (conferences, trade shows)
- Holidays (national and industry-specific)
- Product launches
- Promotional periods
- Competitor activity to monitor

**5. Paid Promotion Plan**
- Which posts to boost (1-2 per month)
- Budget allocation
- Target audience parameters
- Expected ROI based on past performance
- Boosting schedule (optimal days after organic posting)

**6. Influencer/Celebrity Schedule**
- Upcoming launches they might mention
- Relevant hashtag campaigns to join
- Partnership outreach timing
- Content collaboration deadlines

**7. Competitor Research Schedule**
- Weekly check-ins on 3-5 competitors
- Track posting frequency and engagement
- Monitor top-performing content
- Identify content gaps to fill

### Auto-Generation Logic

**Input Data:**
- Last 3 months of post performance (if available)
- Brand content pillars
- Posting frequency preference
- Industry calendar (holidays, events)
- Competitor data (optional)

**Generation Process:**
1. Analyze historical performance to identify:
   - Best posting days/times
   - Top-performing content types
   - Optimal hashtag combinations
   - Engagement patterns
2. Map content pillars to calendar (ensure even distribution)
3. Identify seasonal/holiday opportunities
4. Generate topic suggestions using AI based on:
   - Content pillar focus
   - Past successful themes
   - Brand voice guidelines
   - Competitor gaps
5. Assign optimal posting times
6. Flag special dates requiring custom content
7. Build engagement strategy based on industry targets
8. Create media requisition list

**Output:**
- Complete 30-day calendar in calendar view
- Exportable PDF/Google Doc for team review
- Editable structure allowing modifications
- Status: "Draft" → "Under Review" → "Approved" → "Active"

### Smoothie Bar Example: December 2025 Plan

```
Week 1 (Dec 1-7):
- Dec 3, 6:00 PM: Flavor Spotlight - "Will it Blend? Series Continues"
  - Topic: Next strain combination
  - Media: Product closeup, white background
  - Hashtags: Educational category
  - Status: Planned
  
- Dec 5, 7:00 PM: Consumer Education - "Understanding Terpene Profiles"
  - Topic: Common terpenes and their effects
  - Media: Infographic or visual guide
  - Hashtags: Educational + product category
  - Status: Planned

Week 2 (Dec 8-14):
- Dec 10, 6:30 PM: Cultural Documentary - "LA Artist Feature"
  - Topic: Local creative using cannabis in their work
  - Media: Lifestyle photos, interview quotes
  - Hashtags: Cultural + location category
  - Status: Planned, HIGH PRIORITY (requires interview scheduling)

- Dec 12, 6:00 PM: Community Engagement - "Holiday Poll"
  - Topic: Best strain for holiday relaxation
  - Media: Carousel with options
  - Hashtags: Community + seasonal
  - Status: Planned

Week 3 (Dec 15-21):
- Dec 17, 5:30 PM: Flavor Spotlight - "Will it Blend?"
  - Topic: Holiday-themed combination
  - Media: Product with seasonal styling
  - Hashtags: Series + seasonal
  - Status: Planned

- Dec 19, 7:00 PM: Behind-the-Scenes - "How We Curate Strains"
  - Topic: Selection process transparency
  - Media: Team photos, product testing
  - Hashtags: BTS + educational
  - Status: Planned

Week 4 (Dec 22-31):
- Dec 24: Holiday Message (no sales pitch)
  - Status: Planned, note: Keep light, community-focused

- Dec 28, 6:00 PM: Year in Review - "2025 Top Blends"
  - Topic: Recap best combinations
  - Media: Carousel of product shots
  - Hashtags: Year-end + product
  - Status: Planned

Key Dates:
- Dec 25: Christmas (no posting)
- Dec 31: New Year's Eve (limited engagement)

Engagement Targets:
- @competitor_vape_brand (like 2 posts/day, thoughtful comments 3x/week)
- @cannabis_influencer_la (engage when they post, reply to stories)
- #ceramiccoils feed (find 5 new accounts weekly)

Paid Promo:
- Boost Dec 10 Cultural Documentary post ($100, 3-day campaign)
- Expected reach: 5,000-8,000 based on similar past performance

Competitor Tracking:
- Monitor @competitor1, @competitor2 weekly
- Note: @competitor1 launching new product mid-December, prepare response strategy
```

### User Workflow

**Step 1: Generate Plan**
- Click "Generate December Plan"
- System processes for ~60 seconds
- Presents draft calendar

**Step 2: Review & Modify**
- View in interactive calendar
- Add/remove posts
- Adjust dates/times
- Change topic suggestions
- Add notes for team
- Flag priorities

**Step 3: Export for Team Review**
- Export as PDF or shareable link
- Team adds feedback via notes/comments
- Marketing approves strategy
- Leadership signs off

**Step 4: Finalize**
- Mark as "Approved"
- Calendar structure locks (dates set)
- Individual posts still editable
- System begins tracking progress

### Data Structure

```json
{
  "monthly_plan": {
    "id": "dec_2025_plan",
    "month": "December 2025",
    "client": "smoothie_bar",
    "status": "approved",
    "created_at": "2025-11-10T14:30:00Z",
    "approved_at": "2025-11-12T09:15:00Z",
    "posts": [
      {
        "id": "dec_2025_001",
        "date": "2025-12-03",
        "time": "18:00",
        "timezone": "America/Los_Angeles",
        "content_pillar": "Flavor Spotlights",
        "topic": "Will it Blend? - New combination reveal",
        "media_type": "product_closeup",
        "media_specs": "1080x1080, white background",
        "hashtag_category": "educational",
        "priority": "normal",
        "status": "planned",
        "notes": "Graphics team: macro shot of ceramic coil",
        "assigned_to": "content_creator_1"
      }
    ],
    "stories": [],
    "reels": [],
    "engagement_targets": [
      {
        "username": "@competitor_vape",
        "action": "like_and_comment",
        "frequency": "daily",
        "comment_theme": "supportive, educational"
      }
    ],
    "key_dates": [
      {
        "date": "2025-12-25",
        "event": "Christmas",
        "note": "No posting, community message only"
      }
    ],
    "paid_promo": [
      {
        "post_id": "dec_2025_003",
        "budget": 100,
        "duration_days": 3,
        "target_audience": "LA cannabis enthusiasts",
        "expected_roi": "5k-8k reach based on past performance"
      }
    ],
    "influencer_schedule": [],
    "competitor_tracking": ["@competitor1", "@competitor2"]
  }
}
```

### Success Criteria
- Plan generated in <60 seconds
- Includes all 7 components (posts, stories, engagement, dates, paid, influencer, competitor)
- Exportable as shareable document
- Team can add feedback/notes
- Changes save automatically
- Approved plan locks calendar structure

---

## PHASE 2: CONTENT CREATION & EDITING

### Purpose
Transform planned topics into polished post content (captions, hashtags) with AI as a collaborative assistant, NOT the primary creator.

### Core Philosophy
**AI drafts → Human edits to perfection → Human approves**

The system recognizes that AI-generated content is typically mediocre. Instead, AI serves as a writing assistant that:
- Generates starting drafts based on templates
- Suggests improvements in real-time
- Learns from human edits
- Provides optimization feedback

### Workflow for Each Post

**Step 1: Select Post from Calendar**
- User clicks post in calendar view
- Sees: topic, pillar, media type needed, scheduled time
- Status shows: "Planned" → starting "Content Creation"

**Step 2: AI Draft Generation**
- User clicks "Generate Draft"
- AI creates 3 caption options based on:
  - Topic/theme from plan
  - Brand voice examples
  - Similar past successful posts (if available)
  - Specific caption template for this pillar
  - Content pillar guidelines
- AI ranks drafts by predicted performance
- Shows best option + 2 alternatives

**Step 3: Human Editing (THE CRITICAL PHASE)**

**Split-Screen Editor:**
```
┌─────────────────────┬─────────────────────┐
│  AI DRAFT           │  YOUR EDIT          │
│  (Reference)        │  (Active Editor)    │
│                     │                     │
│  [Draft text]       │  [Editable text]    │
│                     │                     │
│  Alternative 1      │  Real-time stats:   │
│  Alternative 2      │  - 287 characters   │
│                     │  - Reading ease: 8th│
│                     │  - Voice match: 87% │
│                     │  - Has CTA: ✓       │
└─────────────────────┴─────────────────────┘
```

**Real-Time AI Suggestions (As You Type):**
- Weak phrases detected: "really good" → suggest "game-changing"
- Missing elements: "No CTA detected, try adding..."
- Brand voice alignment: "This phrasing sounds too corporate"
- Emoji suggestions: "Consider 🤔 for this question"
- Similar post performance: "Nov 3 post with similar tone got 1.8k likes"
- Character count optimization: "Optimal length is 150-300 chars, you're at 87"

**Suggestion Sidebar Examples:**
```
💡 SUGGESTIONS:
• Hook is weak. Try: "What if you never burned oil again?"
• Add specifics: What makes these coils different?
• This sounds AI-generated. Use more conversational language.
• Strong finish! The CTA is compelling.

📊 METRICS:
• Length: 287 chars (optimal: 150-300) ✓
• Reading ease: 8th grade (good for IG) ✓
• Brand voice match: 82% (good) ✓
• Emoji count: 3 (appropriate) ✓

🔍 SIMILAR POSTS:
• Your Oct 15 post used similar language → 2.1k likes
• This structure matches your top-performing format
```

**Step 4: Hashtag Selection**
- AI suggests 20-25 hashtags ranked by:
  - Relevance to post topic
  - Competition level (avoid oversaturated)
  - Past performance (if tracked)
  - Search volume
- User selects 15-20 final hashtags
- Can save custom hashtag sets for reuse

**Step 5: Version History & Comparison**
- Every save creates a version
- Can view version history
- Compare versions side-by-side
- Revert to any previous version
- See what changed between versions

**Step 6: Final Approval**
- Mark caption as "Content Complete"
- Status changes: "Needs Content" → "Needs Media"
- Post enters media compilation phase

### AI Draft Generation Logic

**Inputs:**
- Post topic: "How ceramic coils prevent burning"
- Content pillar: "Consumer Education"
- Brand voice guidelines (from config)
- Template structure: "[Problem] + [Explanation] + [Solution] + [CTA]"
- Past successful posts in same category
- Tone keywords: authentic, educational, not preachy

**AI Processing:**
1. Analyze top 3 similar past posts
2. Extract successful elements:
   - Hook structure
   - Tone and vocabulary
   - Emoji usage pattern
   - CTA style
3. Generate 3 draft variations:
   - Draft A: More technical/detailed
   - Draft B: Simpler/more accessible
   - Draft C: Story-driven approach
4. Rank by predicted performance based on historical data
5. Present best + alternatives

**Output Example:**

```
DRAFT A (Recommended - 87% voice match):
Ever wondered why your oil tastes burnt? 🤔

Most vape coils heat unevenly, creating hotspots that destroy your concentrate's flavor profile. That burnt taste? It's your terpenes dying.

Our ceramic coils distribute heat evenly across the entire surface. No hotspots. No burning. Just pure, clean flavor the way it's meant to taste.

Try Smoothie Bar's ceramic technology and taste what you've been missing.

Link in bio 👆

DRAFT B (Alternative - More casual):
Burnt oil = sad times 😞

Here's why it happens: Most vapes have metal coils that heat up way too fast in certain spots. Your expensive concentrate? Getting scorched.

Ceramic changes everything. Even heat. No burning. Pure flavor every time.

That's the Smoothie Bar difference.
[Link in bio]

DRAFT C (Alternative - Story approach):
The first time we tested ceramic coils, the difference was obvious. Same concentrate, completely different experience.

No more burnt taste. No more wasted product. Just the pure flavor profile you paid for.

We knew we had to build our entire line around this technology. Because you deserve better than burnt oil.

Experience the Smoothie Bar difference 👆
```

**Hashtag Generation Example:**

```
RECOMMENDED HASHTAGS (15-20):

High Relevance, Low Competition:
#CeramicCoilTechnology ★★★★★
#VapeTips ★★★★☆
#CleanVape ★★★★☆

Medium Relevance, Medium Competition:
#CannabisEducation ★★★☆☆
#VapeCommunity ★★★☆☆
#TerpenePreservation ★★★☆☆

Branded/Series:
#SmoothieBar
#SmoothieBarBlend
#WillItBlend

Location:
#LAcannabis
#CaliforniaCannabis

General (High Competition, Use Sparingly):
#Cannabis
#VapeLife
```

### Learning System

**AI tracks human editing patterns:**
- User consistently removes flowery language → AI reduces
- User always adds emoji at specific points → AI learns placement
- User prefers shorter captions → AI adjusts length
- User changes "Click link" to "Link in bio" → AI adopts phrasing

**Feedback loop:**
```
Draft: "Our innovative ceramic technology revolutionizes the vaping experience"
Human edits to: "Ceramic coils that actually preserve your terpenes"

AI learns:
• Avoid words like "innovative", "revolutionizes"
• Be more specific and benefit-focused
• User prefers direct, technical language
• "Terpenes" is a word this audience understands

Next draft:
"Ceramic coils preserve your terpenes. Metal coils burn them."
(Closer to user's style)
```

### Smoothie Bar Content Creation Examples

**Example 1: Flavor Spotlight Post**

**AI Draft:**
```
🔥 NEW BLEND ALERT 🔥

Truffle Butter x Blue Dream - when luxury meets legend.

Truffle Butter brings that rich, earthy complexity that serious connoisseurs appreciate. Blue Dream delivers the California classic profile we all know and love.

Together? Something entirely new. The indulgent depth of Truffle Butter gets lifted by Blue Dream's bright, berry-forward notes.

This is why we designed the dual-tank system. Experience each strain solo. Then blend and discover the magic.

What blend should we feature next? Drop your suggestions 👇

#WillItBlend #SmoothieBarBlend #CannabisConnoisseur #StrainPairing #DualTank #TruffleButterStrain #BlueDreamStrain #LAcannabis #CannabisEducation
```

**Human Edit (More Smoothie Bar Voice):**
```
Truffle Butter x Blue Dream

When luxury meets legend. When earthy indulgence meets California's most beloved classic.

Truffle Butter alone? Rich, complex, almost decadent. Blue Dream solo? That bright, berry-forward profile that made it iconic. But together...something unexpected happens.

The dual-tank design lets you taste each strain's character first. Then blend. The indulgent depth of Truffle Butter doesn't overshadow Blue Dream—it amplifies it. Those berry notes shine brighter against the earthy backdrop.

This is the curation process. Not every pairing works. This one does.

What blend are you curious about?

#WillItBlend #SmoothieBarBlend #CannabisConnoisseur #StrainPairing #DualTank #TruffleButterStrain #BlueDreamStrain #LAcannabis #CannabisEducation #CeramicCoil #TerpenePreservation #VapeQuality
```

**AI Learns:** Less emoji, more substance. Focus on "why it works" rather than hype. Community engagement through genuine curiosity, not generic CTAs.

### Data Structure

```json
{
  "post": {
    "id": "dec_2025_001",
    "content_status": "content_complete",
    "caption_versions": [
      {
        "version": 1,
        "created_at": "2025-11-15T10:30:00Z",
        "created_by": "ai",
        "text": "[AI draft text]",
        "brand_voice_score": 72
      },
      {
        "version": 2,
        "created_at": "2025-11-15T10:45:00Z",
        "created_by": "human",
        "text": "[Human edited text]",
        "brand_voice_score": 89,
        "changes_from_previous": "Removed flowery language, added specifics"
      },
      {
        "version": 3,
        "created_at": "2025-11-15T11:00:00Z",
        "created_by": "human",
        "text": "[Final version]",
        "brand_voice_score": 94,
        "changes_from_previous": "Refined hook, strengthened CTA"
      }
    ],
    "caption_final": "[Final approved caption text]",
    "hashtags": ["tag1", "tag2", ...],
    "first_comment": "[Optional additional context posted as first comment]",
    "cta": "What blend are you curious about?",
    "brand_voice_score": 94,
    "ai_suggestions_shown": 12,
    "ai_suggestions_accepted": 3,
    "editing_time_minutes": 8,
    "ai_learning_notes": [
      "User prefers questions over imperative CTAs",
      "Less emoji usage than AI suggests",
      "Focus on 'why' over features"
    ]
  }
}
```

### Success Criteria
- AI draft quality improves over time (learning works)
- Human can complete caption editing in <10 minutes
- Brand voice score consistently >85%
- Real-time suggestions are helpful, not annoying
- Version history saves all changes
- User feels in control, not fighting AI
- Can toggle AI suggestions on/off
- Alternative drafts available if primary draft is poor

---

## PHASE 3: MEDIA COMPILATION & REQUISITION

### Purpose
Link completed captions with appropriate visual media (images/videos). When media doesn't exist, create trackable requisition requests for photographers/designers.

### Media Library System

**Auto-Synced Folder Structure:**
```
/syncthing/smoothie_bar_media/
├── product_shots/
│   ├── ceramic_coils/
│   ├── full_device/
│   └── packaging/
├── lifestyle/
│   ├── user_photos/
│   └── studio_lifestyle/
├── educational/
│   ├── infographics/
│   └── diagrams/
└── behind_the_scenes/
    ├── production/
    └── team/
```

**Auto-Detection Workflow:**
1. Syncthing monitors folder for new files
2. When new image/video added:
   - Generate thumbnail
   - Extract metadata (date, size, camera info, dimensions)
   - AI analyzes image: "This appears to be [product/lifestyle/educational] photo"
   - Tag automatically
   - Add to searchable media library
3. Check if any posts need this type of media
4. Suggest linkage if match found
5. Notify user: "New media detected, review for Post #dec_2025_003"

---

## REMAINING PHASES SUMMARY

**PHASE 4: DEPLOYMENT & SCHEDULING**
- Calendar view of ready posts
- One-click scheduling with optimal time suggestions
- Automated posting at scheduled times
- Pre-flight validation checks
- Rollback capability (delete within 5 min)
- Queue management

**PHASE 5: ENGAGEMENT AUTOMATION**
- Comment monitoring (every 15 min)
- AI-drafted responses requiring human approval
- Engagement bot (likes, comments, follows on target accounts)
- Rate limiting to avoid IG bans
- Daily engagement reports

**PHASE 6: ANALYTICS & REPORTING**
- Daily data sync from Instagram
- Live dashboard with key metrics
- Weekly analysis with AI insights
- Monthly PDF reports
- Competitor tracking
- Performance-based recommendations

---

## TECHNICAL STACK

**Backend:** FastAPI (Python)  
**Database:** Supabase or PocketBase  
**UI:** Streamlit (Python web interface)  
**Scheduling:** APScheduler + Temporal/Prefect  
**File Sync:** Syncthing  
**Image Processing:** Pillow + ImageMagick  
**AI:** Claude API (Anthropic)  
**Service Management:** NSSM (Windows) / systemd (Linux)  
**Queue:** Redis + Celery  
**Monitoring:** structlog + Sentry  
**Reports:** WeasyPrint/ReportLab (PDF generation)  
**Charts:** Plotly  

---

## PROJECT STRUCTURE (RECOMMENDED)

```
📁 Dev/Projects/
│
├── 📁 Smoothie_Bar_IG/                    ← EXISTING - Keep as-is
│   ├── memory-bank/                       ← Current context
│   ├── Posts/                             ← Completed posts
│   ├── Old Files/                         ← Supporting docs
│   ├── SOCIAL_MEDIA_MANAGER_PROJECT_BRIEF.md  ← THIS DOCUMENT
│   └── [all other current files]
│
└── 📁 Social_Media_Manager/               ← NEW - Build this
    ├── api/                               ← FastAPI backend
    │   ├── main.py
    │   ├── routes/
    │   │   ├── content.py
    │   │   ├── instagram.py
    │   │   └── analytics.py
    │   └── models.py
    ├── workflows/                         ← Task orchestration
    │   ├── monthly_planning.py
    │   ├── content_creation.py
    │   ├── deployment.py
    │   ├── engagement.py
    │   └── analytics.py
    ├── services/                          ← Business logic
    │   ├── claude_client.py
    │   ├── instagram_client.py
    │   ├── image_processor.py
    │   └── analytics_engine.py
    ├── ui/                                ← Streamlit interface
    │   └── streamlit_app.py
    ├── db/                                
    │   └── supabase_client.py
    ├── config/                            
    │   ├── settings.toml
    │   └── clients/
    │       └── smoothie_bar.toml          ← Points to: ../../../Smoothie_Bar_IG/
    ├── tests/
    ├── requirements.txt
    ├── docker-compose.yml
    └── README.md
```

---

## IMPLEMENTATION ROADMAP

### Phase 1: MVP (Weeks 1-2)
**Goal:** Basic functionality working with Smoothie Bar

- [ ] Project setup & structure
- [ ] Database schema (Supabase/PocketBase)
- [ ] Instagram API integration (test with Smoothie Bar account)
- [ ] Simple Streamlit UI showing calendar
- [ ] Manual content creation interface
- [ ] Manual "Post Now" deployment
- [ ] Basic analytics dashboard

**Deliverable:** Can manually create and post content with tracking

### Phase 2: Core Features (Weeks 3-4)
**Goal:** AI-assisted workflows operational

- [ ] Monthly planning generator (AI-powered)
- [ ] AI content draft generation with real-time suggestions
- [ ] Brand voice scoring system
- [ ] Media library browser
- [ ] Automatic scheduling
- [ ] Comment monitoring

**Deliverable:** Full workflow from planning → deployment

### Phase 3: Automation (Weeks 5-6)
**Goal:** System runs with minimal human intervention

- [ ] Engagement bot (tested with Smoothie Bar targets)
- [ ] Auto-responses to comments (human approval required)
- [ ] Weekly/monthly report generation
- [ ] Competitor tracking automation
- [ ] AI learning from human edits
- [ ] Performance optimization

**Deliverable:** System manages day-to-day with human oversight only

---

## SMOOTHIE BAR INTEGRATION POINTS

### Data to Load from Existing Project

**From:** `Smoothie_Bar_IG/memory-bank/`
- `projectbrief.md` → Brand strategy
- `activeContext.md` → Current decisions & voice refinements
- `progress.md` → What works/what's needed

**From:** `Smoothie_Bar_IG/Posts/`
- All 5 "Will it Blend?" posts → AI training examples
- COA guide post → Educational content example

**From:** Root directory
- `smoothie_bar_product_description.md` → Product info
- Content calendars → Planning template reference

### Configuration File: `smoothie_bar.toml`

```toml
[brand]
name = "Smoothie Bar"
industry = "Cannabis/Vape"
instagram_handle = "@smoothiebar"  # Replace with actual
data_path = "../../../Smoothie_Bar_IG"

[voice]
keywords = ["authentic", "curious", "knowledgeable", "cultural"]
avoid_words = ["Great", "Certainly", "Okay", "Sure", "revolutionary", "innovative"]
tone = "Conversational, never corporate"

[content.pillars]
primary = ["Flavor Spotlights", "Cultural Documentaries", "Consumer Education"]
secondary = ["Community Engagement", "Behind-the-Scenes"]

[posting]
frequency = "4x per week"
optimal_times = ["Tuesday 18:00", "Thursday 18:00-19:00"]
timezone = "America/Los_Angeles"

[visual]
format = "1080x1080"
preferred_style = "White backgrounds, professional, product-focused"

[hashtags]
count_range = [15, 20]
categories = ["series_specific", "educational", "location", "product", "general"]

[example_posts]
voice_reference = "001_will_it_blend_intro"
educational_reference = "001_coa_guide"
```

---

## SUCCESS CRITERIA

### For Smoothie Bar (Test Case):
✅ Generate December 2025 plan in <60 seconds  
✅ AI drafts match brand voice >85% of time  
✅ Create/edit/schedule post in <15 minutes total  
✅ Automated posting works 99%+ reliability  
✅ Engagement bot saves 2+ hours/week  
✅ Monthly reports complete automatically  
✅ Non-technical user operates independently  

### For Generic Tool (Future):
✅ Onboard new brand in <30 minutes  
✅ Works with any Instagram Business account  
✅ Adapts to different brand voices  
✅ Scales to multiple simultaneous clients  

---

## NEXT STEPS

### 1. Review & Approve This Brief
- [ ] User confirms Smoothie Bar context is accurate
- [ ] User approves system architecture
- [ ] User agrees on Phase 1-3 roadmap

### 2. Create Social_Media_Manager Project
- [ ] Set up folder structure
- [ ] Initialize Git repository
- [ ] Configure Python virtual environment
- [ ] Install base dependencies (FastAPI, Streamlit, etc.)

### 3. Phase 1 Development
- [ ] Build database schema
- [ ] Connect to Instagram API (test with Smoothie Bar)
- [ ] Create minimal Streamlit UI
- [ ] Implement manual posting
- [ ] Test with Smoothie Bar "Will it Blend?" content

### 4. Iterate Based on Real Usage
- [ ] Deploy Phase 1 and use with Smoothie Bar
- [ ] Gather feedback
- [ ] Build Phase 2 features
- [ ] Continue expanding

---

## APPENDIX: SMOOTHIE BAR QUICK REFERENCE

**Brand Voice:** Authentic, curious, knowledgeable, cultural  
**Avoid:** Great, Certainly, Okay, Sure, revolutionary, innovative  
**Posting:** 4x/week, Tue/Thu 6-7PM PST  
**Engagement Goal:** 8-10% rate  
**Visual Style:** 1080x1080, white backgrounds preferred  
**Hashtags:** 15-20 per post  

**Current Status (Nov 2025):**
- ✅ 5 "Will it Blend?" posts (need graphics)
- ✅ 1 COA education post (need graphics)
- ❌ No posting schedule
- ❌ No automated deployment
- ❌ No engagement strategy
- ❌ No analytics tracking

**What This System Will Solve:**
- Monthly planning calendar
- AI-assisted content creation respecting brand voice
- Scheduled automated posting
- Systematic engagement
- Performance tracking & reporting

---

**END OF PROJECT BRIEF**

*This document serves as the complete specification for building the Social Media Manager automation system with Smoothie Bar as the inaugural test case.*
