# 🧪 ComfyUI Lab

A personal laboratory for Stable Diffusion workflows, optimization research, and technical documentation.

## 📂 Repository Structure

### `experiments/`
Documentation and analysis reports.
* **Reports:** Detailed markdown logs of sampler comparisons (e.g., Euler A vs Euler), scheduler tests, and optimization strategies.
* **Naming:** `YYYY-MM-DD_topic-name`

### `workflows/`
This directory follows a split-repository structure for security and privacy.

* **`workflows/private/`**: (Sub-Repository)
    * Contains the actual `.json` workflow files, prompts, and thumbnail assets.
    * **Note:** This folder is a separate private Git repository. It is ignored by the main public repo to protect sensitive prompt engineering and assets.

#### Workflow Categories (Inside Private):
* **`master/`**: Production-ready pipelines (e.g., NoobAI XL + FaceDetailer).
* **`highres/`**: Upscaling and refinement pipelines.
* **`repair/`**: Surgical tools (MeshGraphormer) for fixing specific failures.
* **`experimental/`**: Drafts and research nodes.

## 🚀 Current Baseline (Jan 2026)
* **Model:** NoobAI XL
* **Sampler:** `euler_ancestral` (Euler A)
* **Scheduler:** `simple`
* **Detailing:** Face Only (Hand Detailer disabled in Master).
