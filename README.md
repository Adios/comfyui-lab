# 🧪 ComfyUI Lab

A personal laboratory for Stable Diffusion workflows, optimization research, and technical documentation.

## 📂 Repository Structure

### `experiments/`
Documentation and analysis reports.
* **Reports:** Detailed markdown logs of sampler comparisons (e.g., Euler A vs Euler), scheduler tests, and optimization strategies.
* **Naming:** `YYYY-MM-DD_topic-name`

### `workflows/`
This directory follows a split-repository structure for security and privacy.

* **`workflows/templates/`**: (Public)
    * Sanitized, production-ready workflow templates. Safe for general use (no personal paths or prompts).
* **`workflows/private/`**: (Sub-Repository)
    * Contains the raw `.json` workflow files, full prompt stacks, and LoRA/Checkpoints lists.
    * **Note:** This folder is a separate private Git repository. It is ignored by the main public repo to protect sensitive prompt engineering and assets.

### `scripts/`
Maintenance and utility scripts for the lab.
* **`sanitize_workflow.py`**: A CLI tool to prepare workflows for public release.
    * *Function:* Removes prompt text, sanitizes local file paths (LoRAs, Checkpoints), and clears personal metadata.
    * *Usage:* `python3 scripts/sanitize_workflow.py input.json -o output_template.json`

## 🚀 Current Baseline (Jan 2026)
* **Model:** NoobAI XL
* **Sampler:** `euler_ancestral` (Euler A)
* **Scheduler:** `simple`
* **Detailing:** Face Only (Hand Detailer disabled in Master).
