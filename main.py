import os
import json
import csv
import argparse
from datetime import datetime
from samples.sample_doc_generator import generate_sample_contract, generate_sample_reference_dataset
from form_signature_analyser_pipeline import FormSignatureAnalyserPipeline

def main():
    parser = argparse.ArgumentParser(description="Application Form Signature Analyser & Dataset Comparator")
    parser.add_argument("image", nargs="?", help="Path to application form image")
    parser.add_argument("--dataset-dir", type=str, default="signaturedataset", help="Directory containing reference dataset signatures")
    parser.add_argument("--output-dir", type=str, default="results", help="Base directory for output runs")
    parser.add_argument("--model", type=str, default="gemini-2.5-flash", help="Gemini model name")
    args = parser.parse_args()

    # 1. Setup timestamped execution directory
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    run_dir = os.path.join(args.output_dir, f"analyse&compare-{timestamp}")
    os.makedirs(run_dir, exist_ok=True)

    # 2. Check input image or generate synthetic test sample
    form_img_path = args.image
    if not form_img_path or not os.path.exists(form_img_path):
        print("No input image specified or file not found. Generating synthetic application form for demo...")
        form_img_path = generate_sample_contract(os.path.join(run_dir, "application_form.png"))

    # 3. Check reference dataset directory
    dataset_dir = args.dataset_dir
    ref_images = []
    if os.path.exists(dataset_dir):
        ref_images = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    if not ref_images:
        print("No reference dataset signatures found. Generating synthetic dataset for demo...")
        ref_images = generate_sample_reference_dataset(dataset_dir)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable is not set.")
        print("Please set: export GEMINI_API_KEY='your-key'")
        return

    pipeline = FormSignatureAnalyserPipeline(api_key=api_key, model_name=args.model)

    print("\n======================================================================")
    print("STAGE 1 - APPLICATION FORM SIGNATURE ANALYSIS")
    print("======================================================================")
    print(f"Application form : {form_img_path}")
    print(f"Gemini model     : {args.model}")

    analysis, annotated_img, cropped_sig = pipeline.analyze_form(form_img_path)

    print(f"\nSignature present : {analysis.signature_present}")
    print(f"Classification    : {analysis.classification}")
    print(f"Confidence        : {analysis.confidence * 100:.1f}%")
    print(f"Explanation       : {analysis.explanation}")

    annotated_path = os.path.join(run_dir, "form_with_signature_box.png")
    cropped_path = os.path.join(run_dir, "signature_crop.png")
    annotated_img.save(annotated_path)
    cropped_sig.save(cropped_path)

    # Save Stage 1 JSON
    analysis_json_path = os.path.join(run_dir, f"analysis-{timestamp}.json")
    with open(analysis_json_path, "w") as f:
        json.dump(analysis.model_dump(), f, indent=2)

    if not analysis.signature_present:
        print("\n⚠️ No signature detected. Pipeline stopping after Stage 1.")
        return

    print("\n======================================================================")
    print("STAGE 2 - SIGNATURE DATASET COMPARISON")
    print("======================================================================")
    print(f"Reference images : {len(ref_images)}\n")

    comparison_results = []
    csv_rows = []

    for i, ref_path in enumerate(ref_images, 1):
        filename = os.path.basename(ref_path)
        print(f"[{i}/{len(ref_images)}] Comparing {filename} ...")
        comp = pipeline.compare_with_reference(cropped_sig, ref_path)
        print(f"    Result      : {comp.match_result}")
        print(f"    Confidence  : {comp.confidence}/100")
        print(f"    Explanation : {comp.explanation[:100]}...\n")

        comparison_results.append((comp, ref_path))
        csv_rows.append({
            "cropped_image": "signature_crop.png",
            "dataset_signature": filename,
            "dataset_signature_location": os.path.abspath(ref_path),
            "match_result": comp.match_result,
            "confidence": comp.confidence,
            "explanation": comp.explanation,
            "visual_evidence": "; ".join(comp.visual_evidence),
            "limitations": "; ".join(comp.limitations)
        })

    # Save Stage 2 JSON & CSV
    comp_json_path = os.path.join(run_dir, f"comparison_results-{timestamp}.json")
    with open(comp_json_path, "w") as f:
        json.dump([c[0].model_dump() for c in comparison_results], f, indent=2)

    comp_csv_path = os.path.join(run_dir, f"comparison_results-{timestamp}.csv")
    if csv_rows:
        with open(comp_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
            writer.writeheader()
            writer.writerows(csv_rows)

    # Save Stage 2 Word DOCX Report
    docx_path = os.path.join(run_dir, f"signature_comparison_report-{timestamp}.docx")
    pipeline.generate_docx_report(docx_path, analysis, annotated_path, cropped_path, comparison_results)

    print("======================================================================")
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("======================================================================")
    print(f"Run output folder : {run_dir}")
    print(f"Comparison DOCX   : {docx_path}")

if __name__ == "__main__":
    main()
