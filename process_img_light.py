from PIL import Image
import os

images = [
    r"c:\Users\sreya\Desktop\Project\CyberAttackPrediction\static\images\five_pillars_HD.png",
    r"c:\Users\sreya\Desktop\Project\CyberAttackPrediction\static\images\roadmap_HD.png"
]

for img_path in images:
    if os.path.exists(img_path):
        img = Image.open(img_path).convert("RGBA")
        # Create a solid white background
        background = Image.new("RGBA", img.size, (255, 255, 255, 255))
        # Composite the image onto the white background
        lighter_img = Image.alpha_composite(background, img)
        
        # We save as _light.png
        out_path = img_path.replace(".png", "_light.png")
        lighter_img.save(out_path, format="PNG")
        print(f"Saved {out_path}")
    else:
        print(f"Missing: {img_path}")
