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

## 📊 Industry & Model Benchmark Comparison

For full details, see [`BENCHMARK.md`](https://github.com/nrusimhaviewa-byte/gemini-signature-extractor-pipeline/blob/main/BENCHMARK.md).

| System / Model | Provider / Architecture | DocVQA Accuracy | Bounding Box Precision | Signature Detection | Latency | Price / 1M Tokens |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gemini 3.7 Flash** | Google API | **97.4%** | **Extreme (`[0-1000]`)** | **98.2%** | ~0.4s | \$0.10 |
| **Gemini 3.6 Flash** | Google API | **96.5%** | **High (`[0-1000]`)** | **97.4%** | **~0.3s** | **\$0.075** |
| **Gemini 3.1 Pro** | Google API | **97.8%** | **Extreme (`[0-1000]`)** | **98.5%** | ~1.5s | \$1.25 |
| **Qwen2.5-VL-72B** | Open-Weights | 96.4% | High | 96.5% | ~0.6s | Self-Hosted |
| **GPT-4o** | OpenAI API | 96.1% | Medium-High | 96.2% | ~0.8s | \$2.50 |
| **YOLOv8-Signature** | Object Model | N/A | Extreme (Box Only) | 98.2% | ~0.005s | Self-Hosted |

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

## 🚀 Execution Commands

```bash
# Run default pipeline with Gemini 3.6 Flash
python main.py

# Run with Gemini 3.7 Flash (State-of-the-Art)
python main.py application_form.jpg --model gemini-3.7-flash

# Run with Gemini 3.5 Flash-Lite (Low-Cost Screening)
python main.py application_form.jpg --model gemini-3.5-flash-lite
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
