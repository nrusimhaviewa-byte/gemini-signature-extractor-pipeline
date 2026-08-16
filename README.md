# 🖋️ Gemini Form Signature Analyser & Reference Dataset Comparator

Inspired by [`ktravin/form_signature_analyser`](https://github.com/ktravin/form_signature_analyser), this project is a production-grade Python solution utilizing **Google Gemini Multimodal Vision API** (`google-genai` SDK) to perform automated signature analysis on document forms and dataset-wide reference comparison.

---

## ⚡ Two-Stage Workflow Architecture

```text
                     Application Form
                            |
                            v
              +----------------------------+
              |   Stage 1: Gemini Vision   |
              | Full-Form Detection & Crop |
              +-------------+--------------+
                            |
                     Signature Found?
                      /            \
                    No              Yes
                    |                |
                    v                v
               Stop Run       Bounding Box & Crop
                                     |
                                     v
                  +----------------------------------+
                  |  Stage 2: Dataset Comparison     |
                  |  Compare against ALL references  |
                  +------------------+---------------+
                                     |
                +--------------------+--------------------+
                |                    |                    |
                v                    v                    v
         Reference Sig 1      Reference Sig 2      Reference Sig 3
                |                    |                    |
                +--------------------+--------------------+
                                     |
                                     v
                  +----------------------------------+
                  |       Multi-Format Outputs       |
                  |  JSON + CSV + Landscape DOCX     |
                  +----------------------------------+
```

---

## 📋 Features

### Stage 1: Document Form Signature Analysis
- **Full Page Signature Detection**: Finds signatures anywhere on the document without assumption of fixed location.
- **Classification**:
  - `wet_signature`: Handwritten on paper.
  - `pasted_image`: Digitally inserted signature snippet.
  - `signature_does_not_exist`: No signature detected.
  - `uncertain`: Insufficient visual evidence.
- **Visual Grounding**: Returns normalized bounding boxes `[ymin, xmin, ymax, xmax]`.
- **Cropping & Annotations**: Crops signature image and creates annotated full-page output with red bounding box overlay.

### Stage 2: Dataset Comparison & Similarity Audit
- **N-to-1 Dataset Evaluation**: Compares cropped signature against every reference signature in `signaturedataset/`.
- **Match Categories**: `PERFECT MATCH`, `PARTIAL MATCH`, `NO MATCH`, `UNCERTAIN`.
- **Confidence Rating**: Score from `1` to `100`.
- **Explainable Evidence**: Generates visual trajectory reasoning, initial strokes, loop structures, and terminal flourishes.

### Output Artifacts
- **Landscape DOCX Audit Report**: Contains side-by-side tables with image crops, dataset reference details, and visual evidence notes.
- **Structured JSON & CSV Export**: Timestamped execution records under `results/analyse&compare-YYYYMMDDHHMISS/`.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/nrusimhaviewa-byte/gemini-signature-extractor-pipeline.git
cd gemini-signature-extractor-pipeline

# Install dependencies
pip install -r requirements.txt

# Set Gemini API Key
export GEMINI_API_KEY="your-google-gemini-api-key"
# On Windows PowerShell:
# $env:GEMINI_API_KEY="your-google-gemini-api-key"
```

---

## 🚀 Execution

```bash
# Run with sample contract and synthetic reference dataset
python main.py

# Run on your custom application form against custom signature dataset
python main.py application_form.jpg --dataset-dir signaturedataset --output-dir results --model gemini-2.5-flash
```
