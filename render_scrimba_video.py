import os
import cv2
from PIL import Image

def generate_mp4_video(frames_dir="scrimba_frames", output_mp4="Scrimba_Gemini_Signature_Explainer.mp4"):
    images = [os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".png")]
    images.sort()

    if not images:
        raise FileNotFoundError("No frames found to render video.")

    frame = Image.open(images[0])
    width, height = frame.size

    # VideoWriter using mp4v codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_mp4, fourcc, 0.5, (width, height)) # 0.5 fps = 2 seconds per frame

    for img_path in images:
        img_cv = cv2.imread(img_path)
        for _ in range(3):
            video.write(img_cv)

    video.release()
    print(f"Video generated successfully: {output_mp4}")
    return output_mp4

if __name__ == "__main__":
    generate_mp4_video()
