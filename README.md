# 🧪 ComfyUI Lab

A personal laboratory for Stable Diffusion workflows, optimization research, and technical documentation.

## 📂 Repository Structure

This repository is organized into "Tools" (Workflows) and "Research" (Experiments).

### `workflows/`
Production-ready and experimental workflows for ComfyUI.
* **`master/`**: Stable, clean workflows used for daily generation (e.g., Face-only detailer pipelines).
* **`highres/`**: Workflows specialized for upscaling and hand refinement.
* **`repair/`**: Specialized "surgery" workflows (e.g., MeshGraphormer) for fixing specific seeds.
* **`experimental/`**: Drafts and work-in-progress nodes.

### `experiments/`
Documentation, logs, and comparative analysis reports.
* Contains markdown reports (`.md`) detailing sampler comparisons, scheduler tests, and optimization logs.
* Each experiment folder follows the naming convention: `YYYY-MM-DD_topic-name`.

## 🚀 Usage
* **Workflows:** Drag and drop the `.json` (or associated `.png`) files directly into ComfyUI.
* **Reports:** Read the markdown files in `experiments/` to understand the rationale behind specific workflow settings.

## 📝 Current Focus
* **Model:** NoobAI XL
* **Optimization:** Refining Sampler (Euler A) vs. Scheduler interactions.
* **Pipeline:** Migrating from destructive hand-repair techniques to non-invasive refinement pipelines.
