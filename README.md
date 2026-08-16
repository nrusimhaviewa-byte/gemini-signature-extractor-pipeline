# 🖋️ Gemini Form Signature Analyser & Reference Dataset Comparator

A production-grade Python solution utilizing **Google Gemini Multimodal Vision API** (`google-genai` SDK) to perform automated signature detection, visual grounding (bounding boxes), metadata extraction, and dataset-wide reference comparison.

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

## 📋 Key Features & Innovations

### Stage 1: Document Form Signature Analysis
- **Full Page Signature Detection**: Finds signatures anywhere on the document without assuming a fixed layout.
- **Classification Engine**:
  - `wet_signature`: Authentic handwritten signature on paper.
  - `pasted_image`: Digitally inserted signature snippet.
  - `signature_does_not_exist`: Unsigned or blank signature line.
  - `uncertain`: Insufficient image resolution or heavy occlusion.
- **Visual Grounding**: Returns normalized bounding boxes `[ymin, xmin, ymax, xmax]` (0-1000 scale).
- **Cropping & Annotations**: Crops signature snippets and produces bounding box overlays.

### Stage 2: Reference Dataset Comparison
- **N-to-1 Dataset Evaluation**: Compares cropped signature against every reference signature in `signaturedataset/`.
- **Match Categories**: `PERFECT MATCH`, `PARTIAL MATCH`, `NO MATCH`, `UNCERTAIN`.
- **Confidence Rating**: Visual confidence integer from `1` to `100`.
- **Explainable Evidence**: Generates visual trajectory reasoning, initial strokes, loop structures, and terminal flourishes.

---

## 📊 Industry Benchmark Comparison

| System / Repository | Signature Detection | Bounding Box Grounding | Metadata Extraction | Forensic Dataset Comparison | Automated Landscape DOCX Report | Zero-Training Required |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **OpenCV Connected Components** (`ahmetozlu/signature_extractor`) | ⚠️ Rule-based | ❌ Coarse Mask | ❌ No | ❌ No | ❌ No | ⚠️ High Tuning |
| **YOLOv8 Detection** (`khizar-anjum/signature_extraction`) | ✅ Object Model | ✅ Pixel Box | ❌ No | ❌ No | ❌ No | ❌ Needs Training Data |
| **Siamese SigNet** (`BADMG/SignatureVerification`) | ❌ No | ❌ No | ❌ No | ✅ Distance Embeddings | ❌ No | ❌ Needs Triplet Loss Data |
| **Gemini Signature Pipeline (This Project)** | **✅ Multimodal VLM** | **✅ `[0-1000]` Normalized** | **✅ Signatory, Role & Date** | **✅ Visual Stroke Trajectory** | **✅ Built-in (.docx)** | **✅ Prompt & Schema** |

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

---

## 📄 Output Artifacts Generated

Every execution creates a timestamped run folder under `results/analyse&compare-YYYYMMDDHHMISS/`:
- `analysis-YYYYMMDDHHMISS.json`: Full Stage 1 detection JSON.
- `form_with_signature_box.png`: Document with red bounding box overlay.
- `signature_crop.png`: Extracted signature crop image.
- `comparison_results-YYYYMMDDHHMISS.json`: Full Stage 2 comparative JSON.
- `comparison_results-YYYYMMDDHHMISS.csv`: Tabular CSV of dataset comparison results.
- `signature_comparison_report-YYYYMMDDHHMISS.docx`: Formatted landscape Word report with side-by-side tables.
