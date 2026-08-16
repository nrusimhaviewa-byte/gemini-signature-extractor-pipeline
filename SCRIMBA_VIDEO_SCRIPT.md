# 🎬 Scrimba Interactive Video Recording Plan & Script

**Project Title**: Gemini 2.5 / 3.7 Multimodal Application Form Signature Extractor & Dataset Comparator  
**GitHub Repo**: [nrusimhaviewa-byte/gemini-signature-extractor-pipeline](https://github.com/nrusimhaviewa-byte/gemini-signature-extractor-pipeline)  
**Target Platform**: [Scrimba (scrimba.com)](https://scrimba.com/)

---

## 📍 Step-by-Step Instructions to Create the Video on Scrimba

### Step 1: Initialize your Scrimba Workspace
1. Go to [Scrimba.com](https://scrimba.com/) and log in with your GitHub account (**nrusimhaviewa-byte**).
2. Click **Create New Scrim** -> **Import from GitHub**.
3. Paste your repository URL:  
   `https://github.com/nrusimhaviewa-byte/gemini-signature-extractor-pipeline`
4. Scrimba will load the full file tree (`schemas.py`, `form_signature_analyser_pipeline.py`, `main.py`, `BENCHMARK.md`).

---

## 🎙️ Interactive Video Script & Voiceover Guide

### Scene 1: Introduction & Architecture Overview (0:00 - 0:45)
* **Screen Focus**: `README.md`
* **Voiceover**:
  > *"Welcome! In this lesson, we're building an end-to-end Application Form Signature Extractor & Reference Dataset Comparator using Google's Gemini Vision API with Pydantic Structured Outputs."*
  > *"Our pipeline operates in two stages: Stage 1 detects signature presence and bounding boxes anywhere on the form. Stage 2 crops the signature and compares it against every reference signature in a dataset."*

---

### Scene 2: Stage 1 Pydantic Schemas (0:45 - 1:30)
* **Screen Focus**: Open `schemas.py`
* **Action in Code**: Highlight lines 4-20 (`BoundingBox` & `Stage1SignatureAnalysis`).
* **Voiceover**:
  > *"Let's look at `schemas.py`. We define `BoundingBox` coordinates normalized to a 0 to 1000 scale. `Stage1SignatureAnalysis` enforces strict JSON outputs for signature presence, classification (such as wet_signature vs pasted_image), confidence scores, and visual evidence."*

---

### Scene 3: Gemini Multimodal Vision API (1:30 - 2:30)
* **Screen Focus**: Open `form_signature_analyser_pipeline.py`
* **Action in Code**: Scroll to `analyze_form` (Line 26).
* **Voiceover**:
  > *"Here in `form_signature_analyser_pipeline.py`, we pass the application form image along with our prompt to Gemini via `client.models.generate_content`. Notice how we pass `response_schema=Stage1SignatureAnalysis` to guarantee 100% compliant JSON responses."*
  > *"Once Gemini returns the normalized bounding box, we crop the signature and draw a red visual box overlay."*

---

### Scene 4: Stage 2 Reference Dataset Comparison & DOCX Report (2:30 - 3:30)
* **Screen Focus**: Scroll to `compare_with_reference` and `generate_docx_report` (Line 77 & 109).
* **Voiceover**:
  > *"In Stage 2, the pipeline loops through every reference image in `signaturedataset/` and asks Gemini to compare visual stroke trajectories, character loops, and terminal flourishes."*
  > *"Finally, we generate a landscape Word (.docx) report with side-by-side comparison tables, as well as JSON and CSV exports."*

---

### Scene 5: Live Execution & Benchmarks (3:30 - 4:15)
* **Screen Focus**: Scrimba Terminal / `BENCHMARK.md`
* **Action in Terminal**: Type:
  ```bash
  python main.py --model gemini-3.7-flash
  ```
* **Voiceover**:
  > *"Let's run `python main.py --model gemini-3.7-flash`. Gemini 3.7 Flash gives us top-tier DocVQA accuracy (97.4%) with sub-half-second latency! As you can see, our output folder has the annotated PNG, signature crop, JSON, CSV, and landscape DOCX report."*
  > *"Try pausing the Scrimba video right now and editing `schemas.py` to add your own custom field tags!"*

---

## 🚀 Finishing & Publishing Your Scrim on Scrimba

1. Click **Stop Recording** in Scrimba.
2. Edit title to: `Gemini Multimodal Signature Extractor & Dataset Comparator`.
3. Add tags: `python`, `gemini-api`, `ai-vision`, `pydantic`.
4. Click **Publish Scrim** to share your interactive video link!
