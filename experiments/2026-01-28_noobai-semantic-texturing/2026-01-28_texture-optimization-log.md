# 📔 Log: LoRA Adaptation & Texture Optimization

**Date:** January 28, 2026
**Subject:** Workflow Migration (High-Contrast -> Low-Contrast LoRA) and Semantic Texturing
**Model:** NoobAI XL
**Scope:** Resolving "Flatness" in soft-style LoRAs without breaking the Anime domain.

---

### 1. The Challenge: "The Flatness Trap"
Migrating the Master Workflow from a "High Contrast" character LoRA to a "Soft Style" character LoRA resulted in significant quality degradation.
* **Symptoms:** Skin appeared "flat" (lacking texture) and details rendered with "soft 3D shading" rather than the desired "hard-edge" anime style.
* **Root Cause:** The target LoRA has a different native contrast/saturation bias, requiring a recalibration of the "Texture Prompting" strategy.

### 2. Failed Optimization Attempts
| Attempt | Adjustment | Result | Analysis |
| :--- | :--- | :--- | :--- |
| **Negative Filters** | Added `flat color`, `flat lighting`, `photorealistic` | **Mixed** | Improved shading slightly but occasionally forced a "semi-realistic" look. |
| **Style Weighting** | Increased `anime screencap` (1.0 → 1.2) | **Failure** | Did not solve the flatness; only made lines thicker. |
| **Direct Realism** | Added `realistic skin`, `realistic shades` | **Collapse** | **CRITICAL FAILURE.** Caused domain conflict (Anime vs Photo), destroying the drawing style. |
| **Hybrid Realism** | Added `realistic shades` (Clothing only) | **Failure** | Did not propagate texture correctly. |

---

### 3. The Solution: "Semantic Texturing" (Intricate)
The breakthrough was moving away from "Realism" tokens and using **Complexity** tokens.

**The "Intricate" Injection Strategy:**
Instead of modifying the global style, specific texture tags were injected *inside* the character and clothing blocks.

1.  **Skin Injection:** `dark skin, intricate shades, dark-skinned female`
    * *Effect:* Forces the model to render high-frequency shading details on the skin without switching to a photorealistic style.
2.  **Clothing Injection:** `[costume name], intricate shades`
    * *Effect:* Adds fold and fabric density to the outfit.

---

### 4. Parameter Drift (Adaptation Analysis)

| Parameter | Character A (Baseline) | Character B (Target) | Reason |
| :--- | :--- | :--- | :--- |
| **Trigger Weight** | `1.1` | **`1.0`** | Target LoRA is stiffer; over-weighting causes burn. |
| **RescaleCFG** | `0.75` | **`0.85`** | Target LoRA is naturally flatter; needs higher CFG to force contrast. |
| **FX Weighting** | `0.7` | **`1.0`** | `light particles`, `aura` needed a boost to be visible against the softer style. |
| **Lens FX** | `1.0` | **`1.2`** | `chromatic aberration`, `film grain` needed 20% boost to register. |
| **Negative** | `saturated` | **(Removed)** | Target LoRA is naturally desaturated; removing this prevents "grey" images. |

### 📝 Conclusion
"Realism" tags are destructive in NoobAI anime workflows when trying to fix flatness. To fix texture issues in soft LoRAs, use **"Intricate Shades"** targeting specific elements (Skin/Clothes). This increases detail density while preserving the 2D Anime Domain.
