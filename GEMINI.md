# 🤖 GEMINI.md - Agent Context & Operational Manual

**Identity:** `comfyui-lab`
**Purpose:** A dual-purpose repository for Stable Diffusion research (public) and production workflow management (private).

## 🏗️ Architecture: The "Stowaway" Pattern

This project uses a nested repository structure to separate public code from private assets.

*   **Public Scope (`/`)**: 
    *   Contains experimentation reports, sanitization scripts, and "template" workflows.
    *   *Rule:* **NEVER** commit personal paths, NSFW prompts, or raw JSONs here.
*   **Private Scope (`/workflows/private/`)**:
    *   A separate git repository nested inside the public one (ignored via `.gitignore`).
    *   Contains raw production workflows, full prompt stacks, and LoRA lists.
    *   *Rule:* All "working" files go here.

## 📏 Operational Mandates

### 1. Naming Conventions
*   **Experiments/Reports:** `YYYY-MM-DD_topic-name` (e.g., `2026-01-20_sampler-comparison`).
*   **Workflows:** **Functional** naming, not Output naming.
    *   ✅ `noobai_master_face_v1.json` (describes the pipeline)
    *   ❌ `magical_girl_blue_eyes.json` (describes the picture)
*   **Assets:** Thumbnails must be "Birds-eye view" screenshots of the entire node graph.

### 2. Workflow Release Lifecycle
1.  **Develop:** Edit and refine in `workflows/private/master/`.
2.  **Sanitize:** Run `python3 scripts/sanitize_workflow.py <input> -o <output>` to strip metadata.
3.  **Publish:** Commit the sanitized output to `workflows/templates/` in the public repo.

### 3. Git Standards
*   **Style:** Conventional Commits (`type(scope): subject`).
    *   `feat(master): add new face detailer node`
    *   `docs(experiment): add sampler comparison log`
*   **Private Repo:** Requires manual directory switching (`cd workflows/private`) to manage git operations.

## 🛠️ Environment & Tooling

*   **Docker Integration:**
    *   Host Path: `~/s/comfyui-lab/workflows/private`
    *   Container Path: `/opt/ComfyUI/user/default/workflows/git_lab`
    *   *Note:* Bind mounts are configured to allow "Save in Browser -> Commit in Terminal" workflows.
*   **Sanitizer:** `scripts/sanitize_workflow.py`
    *   Automatically nukes local file paths and `PrimitiveStringMultiline` (prompts).

## 🚀 Current Tech Stack (Jan 2026)
*   **Base Model:** NoobAI XL
*   **Sampler:** `euler_ancestral` (Euler A)
*   **Scheduler:** `simple`
*   **Strategy:** Face-only detailing (Hand detailer currently disabled).
