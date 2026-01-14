"""
Re-classify human annotation samples with IMPROVED framing prompt.
Version 2 - Based on disagreement analysis with human annotations.
January 2025
"""

import pandas as pd
import json
import time
import os
import sys
from openai import OpenAI
# from dotenv import load_dotenv
import os
import sys
# from openai import OpenAI
# Note: Users must provide their own OpenAI API key
api_key = os.getenv("OPENAI_API_KEY") 
if not api_key:
    print("Please set your OPENAI_API_KEY environment variable.")
    # api_key = "YOUR_API_KEY_HERE"

# client = OpenAI(api_key=api_key)


def classify_post(title: str, body: str = "") -> dict:
    """Classify a single post using the IMPROVED prompt."""
    text = f"Title: {title}\nBody: {body[:500] if body else 'N/A'}"
    
    prompt = f"""You are an international relations researcher. Classify the following Reddit post into ONE of 5 framing categories.

## ⚠️ Critical Classification Rules (Apply First!)

### Rule 1: No Action = NEUTRAL
If the post is a **question, hypothesis, speculation, or factual report** without explicit government action, classify as **NEUTRAL**.
- Example: "What if Ukraine and Russia go to war?" → NEUTRAL (question, no action)
- Example: "Russia's submarine activity at highest level" → NEUTRAL (factual report)

### Rule 2: Verbal vs Physical Actions
If a state is **only verbally criticizing or warning** another state (not taking physical/military action), classify as **DIPLOMACY**, not THREAT.
- Example: "China warns India over military buildup" → DIPLOMACY (verbal warning)
- Example: "Russia claims US supporting terrorism" → DIPLOMACY (verbal criticism)

### Rule 3: Individual Harm = HUMANITARIAN
If the harm is to **specific individuals** (protesters, defectors, refugees, civilians), classify as **HUMANITARIAN**, not THREAT.
- Example: "North Korea soldier shot while defecting" → HUMANITARIAN (individual harm)
- Example: "Cyberattack hits app used by Hong Kong protesters" → HUMANITARIAN (targeting civilians)

### Rule 4: Conflicting Frames = NEUTRAL
When **DIPLOMACY and THREAT (or other frames) are equally present** and competing, classify as **NEUTRAL**.
- Example: "Syria shifts to diplomacy while US pushes for war" → NEUTRAL (equal competing frames)

### Rule 5: Domestic Politics = NEUTRAL
**Commentary on domestic political issues**, even if mentioning foreign countries, is NEUTRAL.
- Example: "Democrats criticize Trump on Russia policy" → NEUTRAL (domestic politics)

---

## Classification Criteria

### THREAT (Military Tension/Conflict)
**Physical military actions that increase conflict possibility**

Include:
- Military actions: missile launches, nuclear tests, military exercises, shows of force
- Arms buildup: weapons sales, arms provision, military equipment deployment
- Military threats with NO dialogue possibility (ultimatums)
- Cyberattacks on military/government infrastructure

**Exclude (classify as DIPLOMACY instead):**
- Verbal warnings with possibility of dialogue remaining
- One state verbally criticizing another's actions
- Requests to stop military activities (diplomatic pressure)

---

### DIPLOMACY (Diplomatic Interaction)
**Relationship adjustment through dialogue, negotiation, or verbal pressure**

Include:
- Summit meetings, diplomatic negotiations, bilateral/multilateral talks
- Agreements, treaties, accord signings
- Attempts to improve/normalize relations
- Sanctions relief or easing
- **Verbal criticism, condemnation, or warnings between states**
- **One state urging another to stop certain actions** (diplomatic pressure)
- Even if a summit fails, focus on the summit itself → DIPLOMACY

---

### ECONOMIC (Economic Measures)
**Pressure or cooperation through economic means**

Include:
- Imposition/strengthening of economic sanctions
- Sanctions evasion activities
- Trade measures (tariffs, import/export restrictions)
- Economic cooperation, investment, aid

**Exclude:**
- Arms deals → THREAT
- If the main focus is diplomatic action, not economic → DIPLOMACY

---

### HUMANITARIAN (Humanitarian Issues)
**Human rights and individual/civilian harm**

Include:
- Human rights violations, oppression (targeting civilians within a country)
- Refugee issues
- Humanitarian assistance/aid
- War crimes, genocide
- **Harm to individuals (protesters, defectors, refugees, civilians)**
- **Cyberattacks targeting protesters or civilian groups**

---

### NEUTRAL (Neutral Information)
**Cases not fitting specific frames**

Include:
- Simple factual reporting, analysis, information delivery
- **Domestic politics** (party conflicts, government criticism, etc.)
- **Questions and hypothetical scenarios** ("What if X happens?")
- **Factual descriptions without explicit government action**
- **When multiple frames are equally present and competing**
- Complex cases where priority determination is difficult

---

## Post
{text}

## Response Format (JSON only)
{{"frame": "THREAT|DIPLOMACY|ECONOMIC|HUMANITARIAN|NEUTRAL", "confidence": 0.0-1.0, "reason": "One sentence explaining classification rationale"}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a political science researcher analyzing media framing of international relations. Apply the Critical Classification Rules FIRST before classifying."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200,
            response_format={"type": "json_object"}
        )
        
        result_text = response.choices[0].message.content.strip()
        result = json.loads(result_text)
        
        # Validate frame
        valid_frames = ['THREAT', 'DIPLOMACY', 'NEUTRAL', 'ECONOMIC', 'HUMANITARIAN']
        if result.get('frame') not in valid_frames:
            result['frame'] = 'NEUTRAL'
            result['confidence'] = 0.5
            
        return result
        
    except Exception as e:
        return {
            "frame": "NEUTRAL",
            "confidence": 0.5,
            "reason": f"Error: {str(e)}"
        }


def main():
    print("=" * 70)
    print("📊 LLM vs Human Framing Agreement Analysis (IMPROVED PROMPT v2)")
    print("=" * 70)
    
    # Load all three annotation files
    batch_pilot = pd.read_csv('data/annotations/framing_human_annotation_Moon - batch_pilot.csv')
    batch_1 = pd.read_csv('data/annotations/framing_human_annotation_Moon - batch_1.csv')
    batch_2 = pd.read_csv('data/annotations/framing_human_annotation_Moon - batch_2.csv')
    
    print(f"\n📁 Loaded files:")
    print(f"  - batch_pilot: {len(batch_pilot)} rows")
    print(f"  - batch_1: {len(batch_1)} rows")
    print(f"  - batch_2: {len(batch_2)} rows")
    
    # Combine all batches
    combined = pd.concat([batch_pilot, batch_1, batch_2], ignore_index=True)
    
    # Clean and filter
    combined['final_frame_clean'] = combined['final_frame'].astype(str).str.strip().str.upper()
    
    # Filter: only valid frames (exclude empty, nan, unmatched)
    valid_frames = ['THREAT', 'DIPLOMACY', 'NEUTRAL', 'ECONOMIC', 'HUMANITARIAN']
    valid = combined[combined['final_frame_clean'].isin(valid_frames)]
    valid = valid.dropna(subset=['title'])
    valid = valid[valid['title'].str.len() > 0]
    
    total = len(valid)
    print(f"\n✅ Valid samples for analysis: {total}")
    print(f"📊 Human annotation distribution:")
    print(valid['final_frame_clean'].value_counts())
    print()
    
    results = []
    
    # Manual progress display
    for idx in range(total):
        row = valid.iloc[idx]
        title = str(row['title'])
        body = str(row.get('text', '')) if pd.notna(row.get('text')) else ''
        
        result = classify_post(title, body)
        
        results.append({
            'sample_id': row.get('sample_id', idx),
            'post_id': row.get('post_id', ''),
            'title': title[:100],
            'human_frame': row['final_frame_clean'],
            'llm_frame': result.get('frame', 'NEUTRAL'),
            'llm_confidence': result.get('confidence', 0.5),
            'llm_reason': result.get('reason', '')
        })
        
        # Progress display every 10 samples
        if (idx + 1) % 10 == 0 or idx == total - 1:
            pct = (idx + 1) / total * 100
            print(f"  Progress: {idx + 1}/{total} ({pct:.1f}%)", flush=True)
        
        # Rate limiting
        time.sleep(0.15)
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    # ========== Calculate Metrics ==========
    print("\n" + "=" * 70)
    print("📊 ANALYSIS RESULTS (IMPROVED PROMPT v2)")
    print("=" * 70)
    
    # Overall accuracy
    matches = results_df['human_frame'] == results_df['llm_frame']
    accuracy = matches.sum() / len(results_df)
    print(f"\n✅ Overall Accuracy: {accuracy:.1%} ({matches.sum()}/{len(results_df)})")
    
    # Cohen's Kappa
    kappa = cohen_kappa_score(results_df['human_frame'], results_df['llm_frame'])
    print(f"📈 Cohen's Kappa: {kappa:.3f}")
    
    if kappa < 0.2:
        kappa_interp = "Poor agreement"
    elif kappa < 0.4:
        kappa_interp = "Fair agreement"
    elif kappa < 0.6:
        kappa_interp = "Moderate agreement"
    elif kappa < 0.8:
        kappa_interp = "Substantial agreement"
    else:
        kappa_interp = "Almost perfect agreement"
    print(f"   Interpretation: {kappa_interp}")
    
    # Per-class metrics
    print("\n📊 Per-Frame Results:")
    print("-" * 60)
    for frame in valid_frames:
        human_count = (results_df['human_frame'] == frame).sum()
        llm_count = (results_df['llm_frame'] == frame).sum()
        
        tp = ((results_df['human_frame'] == frame) & (results_df['llm_frame'] == frame)).sum()
        
        recall = tp / human_count if human_count > 0 else 0
        precision = tp / llm_count if llm_count > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"  {frame:12s}: Human={human_count:3d}, LLM={llm_count:3d} | "
              f"Precision={precision:.2f}, Recall={recall:.2f}, F1={f1:.2f}")
    
    # Confusion Matrix
    print("\n📊 Confusion Matrix:")
    print("-" * 60)
    cm = confusion_matrix(results_df['human_frame'], results_df['llm_frame'], labels=valid_frames)
    print("         " + "  ".join(f"{f[:6]:>6s}" for f in valid_frames))
    for i, frame in enumerate(valid_frames):
        row_str = " ".join(f"{cm[i, j]:6d}" for j in range(len(valid_frames)))
        print(f"{frame[:8]:8s} {row_str}")
    
    # Classification report
    print("\n📊 Detailed Classification Report:")
    print("-" * 60)
    print(classification_report(results_df['human_frame'], results_df['llm_frame'], 
                                labels=valid_frames, zero_division=0))
    
    # Save results
    output_path = 'data/annotations/llm_improved_v2_classification.csv'
    results_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n💾 Results saved to: {output_path}")
    
    # Show some disagreement examples
    disagreements = results_df[~matches]
    if len(disagreements) > 0:
        print(f"\n⚠️ Disagreement Examples (showing first 10):")
        print("-" * 60)
        for _, row in disagreements.head(10).iterrows():
            print(f"  Title: {row['title'][:60]}...")
            print(f"    Human: {row['human_frame']} | LLM: {row['llm_frame']}")
            print(f"    Reason: {row['llm_reason'][:80]}...")
            print()
    
    print("=" * 70)
    print("✅ Analysis Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
