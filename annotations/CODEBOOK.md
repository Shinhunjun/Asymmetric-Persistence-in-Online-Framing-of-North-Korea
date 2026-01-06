# Framing Annotation Codebook

**Version:** 2.0 (English / Improved Prompt)  
**Last Updated:** January 2025  

This codebook defines the criteria used to classify Reddit posts into five framing categories. It serves as the ground truth for both human annotation and LLM-based classification.

---

## ⚠️ Critical Classification Rules (Priority)

These rules resolve ambiguities and edge cases. They must be applied **before** the general category definitions.

### Rule 1: No Action = NEUTRAL

If the post is a **question, hypothesis, speculation, or factual report** without explicit government action, classify as **NEUTRAL**.

- *Example:* "What if Ukraine and Russia go to war?" → **NEUTRAL** (question, no action)
- *Example:* "Russia's submarine activity at highest level" → **NEUTRAL** (factual report)

### Rule 2: Verbal vs. Physical Actions

If a state is **only verbally criticizing or warning** another state (without taking physical/military action), classify as **DIPLOMACY**, not THREAT.

- *Example:* "China warns India over military buildup" → **DIPLOMACY** (verbal warning)
- *Example:* "Russia claims US supporting terrorism" → **DIPLOMACY** (verbal criticism)

### Rule 3: Individual Harm = HUMANITARIAN

If the harm is to **specific individuals** (protesters, defectors, refugees, civilians), classify as **HUMANITARIAN**, not THREAT.

- *Example:* "North Korea soldier shot while defecting" → **HUMANITARIAN** (individual harm)
- *Example:* "Cyberattack hits app used by Hong Kong protesters" → **HUMANITARIAN** (targeting civilians)

### Rule 4: Conflicting Frames = NEUTRAL

When **DIPLOMACY and THREAT (or other frames) are equally present** and competing, classify as **NEUTRAL**.

- *Example:* "Syria shifts to diplomacy while US pushes for war" → **NEUTRAL** (equal competing frames)

### Rule 5: Domestic Politics = NEUTRAL

**Commentary on domestic political issues**, even if mentioning foreign countries, is **NEUTRAL**.

- *Example:* "Democrats criticize Trump on Russia policy" → **NEUTRAL** (domestic politics)

---

## Classification Guidelines by Category

### 1. THREAT (Military Tension/Conflict)

**Physical military actions that increase the possibility of conflict.**

**Include:**

- Military actions: missile launches, nuclear tests, military exercises, shows of force
- Arms buildup: weapons sales, arms provision, military equipment deployment
- Military threats with **NO** dialogue possibility (ultimatums)
- Cyberattacks on military/government infrastructure

**Exclude (classify as DIPLOMACY instead):**

- Verbal warnings with possibility of dialogue remaining
- One state verbally criticizing another's actions
- Requests to stop military activities (diplomatic pressure)

### 2. DIPLOMACY (Diplomatic Interaction)

**Relationship adjustment through dialogue, negotiation, or verbal pressure.**

**Include:**

- Summit meetings, diplomatic negotiations, bilateral/multilateral talks
- Agreements, treaties, accord signings
- Attempts to improve/normalize relations
- Sanctions relief or easing
- **Verbal criticism, condemnation, or warnings between states**
- **One state urging another to stop certain actions** (diplomatic pressure)
- Even if a summit fails, focus on the summit itself → DIPLOMACY

### 3. ECONOMIC (Economic Measures)

**Pressure or cooperation through economic means.**

**Include:**

- Imposition/strengthening of economic sanctions
- Sanctions evasion activities
- Trade measures (tariffs, import/export restrictions)
- Economic cooperation, investment, aid

**Exclude:**

- Arms deals → **THREAT**
- If the main focus is diplomatic action, not economic → **DIPLOMACY**

### 4. HUMANITARIAN (Humanitarian Issues)

**Human rights violations and harm to individuals or civilians.**

**Include:**

- Human rights violations, oppression (targeting civilians within a country)
- Refugee issues
- Humanitarian assistance/aid
- War crimes, genocide
- **Harm to individuals (protesters, defectors, refugees, civilians)**
- **Cyberattacks targeting protesters or civilian groups**

### 5. NEUTRAL (Neutral Information)

**Cases not fitting specific frames or lacking explicit state action.**

**Include:**

- Simple factual reporting, analysis, information delivery
- **Domestic politics** (party conflicts, government criticism, etc.)
- **Questions and hypothetical scenarios** ("What if X happens?")
- **Factual descriptions without explicit government action**
- **When multiple frames are equally present and competing**
- Complex cases where priority determination is difficult

---

## Annotation Procedure

1. Read the post title (and body if available).
2. Check **Critical Rules 1-5** first.
3. If no critical rule applies, determine the **primary action** described.
4. Assign the category that best fits the primary action.
5. If two categories are equally strong, assign **NEUTRAL**.
