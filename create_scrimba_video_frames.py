import os
import time
from PIL import Image, ImageDraw, ImageFont

def create_scrimba_explainer_frames(output_dir="scrimba_frames"):
    os.makedirs(output_dir, exist_ok=True)
    width, height = 1280, 720
    
    frames_meta = [
        {
            "title": "Gemini Multimodal Signature Extractor",
            "subtitle": "Scrimba Interactive Explainer Walkthrough",
            "file": "README.md",
            "code": "# Gemini 2.5 / 3.7 Form Signature Analyser\n\n- Stage 1: Document Detection & Grounding\n- Stage 2: Reference Dataset Comparison\n- Outputs: JSON, CSV, Landscape DOCX Report",
            "status": "Step 1: Introduction & Architecture Overview"
        },
        {
            "title": "Stage 1: Pydantic Schema Validation",
            "subtitle": "Guaranteed Structured JSON Outputs",
            "file": "schemas.py",
            "code": "class BoundingBox(BaseModel):\n    ymin: int  # Normalized 0-1000\n    xmin: int\n    ymax: int\n    xmax: int\n\nclass Stage1SignatureAnalysis(BaseModel):\n    signature_present: bool\n    classification: str # wet_signature | pasted_image\n    bounding_box: BoundingBox",
            "status": "Step 2: Defining Pydantic Schemas"
        },
        {
            "title": "Stage 1: Gemini Multimodal Vision API",
            "subtitle": "Visual Grounding & Bounding Box Overlays",
            "file": "form_signature_analyser_pipeline.py",
            "code": "response = self.client.models.generate_content(\n    model='gemini-3.7-flash',\n    contents=[img, prompt],\n    config=types.GenerateContentConfig(\n        response_mime_type='application/json',\n        response_schema=Stage1SignatureAnalysis\n    )\n)",
            "status": "Step 3: Executing Gemini Vision VLM"
        },
        {
            "title": "Stage 2: Dataset Comparison & Landscape DOCX",
            "subtitle": "Forensic Stroke Trajectory Comparison",
            "file": "form_signature_analyser_pipeline.py",
            "code": "for ref_img in reference_dataset:\n    comparison = compare_with_reference(cropped_sig, ref_img)\n    # Results: PERFECT MATCH (96/100), PARTIAL MATCH, NO MATCH\n\ngenerate_docx_report(output_docx, analysis, comparison_results)",
            "status": "Step 4: N-to-1 Reference Dataset Comparison"
        },
        {
            "title": "Live Execution & Model Benchmarks",
            "subtitle": "Gemini 3.7 Flash vs GPT-4o vs Qwen2.5-VL",
            "file": "terminal",
            "code": "$ python main.py --model gemini-3.7-flash\n[1/2] Stage 1 Analysis: wet_signature (98.2% confidence)\n[2/2] Stage 2 Comparison: PERFECT MATCH (96/100)\n📄 Landscape DOCX Generated: results/signature_report.docx",
            "status": "Step 5: Terminal Execution & Output Verification"
        }
    ]

    frame_paths = []
    for idx, meta in enumerate(frames_meta):
        img = Image.new("RGB", (width, height), color="#1e1e2e")
        draw = ImageDraw.Draw(img)

        # Header Bar (Scrimba Style)
        draw.rectangle([(0, 0), (width, 60)], fill="#181825")
        draw.text((30, 20), "Scrimba Interactive Code Studio - nrusimhaviewa-byte", fill="#cba6f7")
        draw.text((width - 300, 20), "● RECORDING LIVE", fill="#f38ba8")

        # Sidebar (Files List)
        draw.rectangle([(0, 60), (280, height)], fill="#11111b")
        draw.text((20, 80), "FILES", fill="#a6adc8")
        files = ["README.md", "schemas.py", "pipeline.py", "main.py", "BENCHMARK.md"]
        for f_idx, fname in enumerate(files):
            is_active = (fname in meta["file"] or fname == meta["file"])
            color = "#89b4fa" if is_active else "#6c7086"
            prefix = "▶ " if is_active else "  "
            draw.text((20, 120 + f_idx * 35), f"{prefix}{fname}", fill=color)

        # Code Editor Main Window
        draw.rectangle([(290, 70), (width - 20), 450], fill="#1e1e2e", outline="#313244", width=2)
        draw.rectangle([(290, 70), (width - 20), 110], fill="#313244")
        draw.text((310, 82), f"Active File: {meta['file']}  |  {meta['title']}", fill="#cdd6f4")

        # Code Lines
        code_lines = meta["code"].split("\n")
        for c_idx, line in enumerate(code_lines):
            draw.text((310, 130 + c_idx * 24), line, fill="#a6e3a1" if line.startswith("$") or line.startswith("class") else "#cdd6f4")

        # Terminal / Output Panel
        draw.rectangle([(290, 460), (width - 20), height - 20], fill="#11111b", outline="#45475a", width=2)
        draw.rectangle([(290, 460), (width - 20), 490], fill="#181825")
        draw.text((310, 470), "SCRIMBA TERMINAL & EXPLAINER STATUS", fill="#fab387")
        draw.text((310, 510), f"STATUS: {meta['status']}", fill="#f9e2af")
        draw.text((310, 540), f"SUBTITLE: {meta['subtitle']}", fill="#bac2de")

        frame_path = os.path.join(output_dir, f"frame_{idx:02d}.png")
        img.save(frame_path)
        frame_paths.append(frame_path)

    print(f"Generated {len(frame_paths)} explainer frames.")
    return frame_paths

if __name__ == "__main__":
    create_scrimba_explainer_frames()
