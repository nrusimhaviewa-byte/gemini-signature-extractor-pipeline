import os
from PIL import Image, ImageDraw, ImageFont

def generate_sample_contract(output_path: str = "sample_contract.png"):
    """
    Creates a realistic synthetic document image with text, document fields, and a signature line.
    """
    width, height = 800, 1000
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((250, 40), "NON-DISCLOSURE AGREEMENT", fill="black")
    draw.line([(50, 80), (750, 80)], fill="black", width=2)

    # Body text
    body = [
        "This Agreement is entered into by and between Company A and the undersigned party.",
        "1. Confidential Information: Both parties agree to protect proprietary data.",
        "2. Term: This agreement shall remain valid for a period of two (2) years.",
        "3. Governing Law: This agreement shall be governed by the laws of the State.",
        "",
        "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date below."
    ]
    y_pos = 120
    for line in body:
        draw.text((60, y_pos), line, fill="darkgray" if line.startswith("IN WITNESS") else "black")
        y_pos += 30

    # Signature Block 1 (Blank Line)
    draw.text((60, 600), "Party A Authorized Signatory:", fill="black")
    draw.line([(60, 670), (350, 670)], fill="black", width=1)
    draw.text((60, 680), "Date: __________________", fill="black")

    # Signature Block 2 (Signed with simulated cursive signature)
    draw.text((450, 600), "Party B Signatory (John Doe):", fill="black")
    draw.line([(450, 670), (740, 670)], fill="black", width=1)
    draw.text((450, 680), "Date: August 16, 2026", fill="black")

    # Draw simulated handwriting signature
    points = [
        (460, 660), (480, 620), (510, 665), (530, 630), 
        (560, 650), (590, 615), (630, 660), (670, 625), (710, 655)
    ]
    draw.line(points, fill="blue", width=3, joint="curve")
    draw.text((500, 630), "J. Doe", fill="navy")

    img.save(output_path)
    return output_path

def generate_sample_reference_dataset(dataset_dir: str = "signaturedataset"):
    """
    Generates sample reference signature dataset images for testing Stage 2 comparison.
    """
    os.makedirs(dataset_dir, exist_ok=True)
    
    # Signature 1: Matching signature (John Doe style)
    img1 = Image.new("RGB", (300, 150), color="white")
    draw1 = ImageDraw.Draw(img1)
    points1 = [(20, 100), (50, 40), (80, 110), (110, 50), (150, 90), (200, 30), (250, 100)]
    draw1.line(points1, fill="blue", width=3, joint="curve")
    draw1.text((70, 60), "J. Doe", fill="navy")
    img1_path = os.path.join(dataset_dir, "signature_01_john_doe_match.png")
    img1.save(img1_path)

    # Signature 2: Non-matching signature (Jane Smith style)
    img2 = Image.new("RGB", (300, 150), color="white")
    draw2 = ImageDraw.Draw(img2)
    draw2.ellipse([(30, 30), (120, 120)], outline="black", width=3)
    draw2.line([(120, 75), (270, 75)], fill="black", width=4)
    draw2.text((140, 50), "Jane S.", fill="black")
    img2_path = os.path.join(dataset_dir, "signature_02_jane_smith_nomatch.png")
    img2.save(img2_path)

    # Signature 3: Partial match / Initial
    img3 = Image.new("RGB", (300, 150), color="white")
    draw3 = ImageDraw.Draw(img3)
    draw3.line([(40, 120), (80, 20), (140, 120)], fill="blue", width=4)
    draw3.line([(55, 70), (120, 70)], fill="blue", width=3)
    img3_path = os.path.join(dataset_dir, "signature_03_john_initials_partial.png")
    img3.save(img3_path)

    return [img1_path, img2_path, img3_path]
