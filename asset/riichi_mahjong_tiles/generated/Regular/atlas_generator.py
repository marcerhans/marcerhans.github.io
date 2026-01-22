import os
from PIL import Image

def compose_images(base_img_path, overlay_paths, size=None):
    base = Image.open(base_img_path).convert("RGBA")
    if size:
        base = base.resize(size)

    for overlay_path in overlay_paths:
        overlay = Image.open(overlay_path).convert("RGBA")
        if size:
            size_overlay = (int(size[0] / 1.5), int(size[1] / 1.5))
            overlay = overlay.resize(size_overlay)
            base.alpha_composite(overlay, dest=(int(size[0] / 2.0) - int(size_overlay[0] / 2.0), int(size[1] / 2.0) - int(size_overlay[1] / 2.0)))
        else:
            base.alpha_composite(overlay)

    return base

def create_atlas(base_png, overlays_list, output_path="atlas.png", size=(64, 64), per_row=4):
    """
    base_png: path to base PNG file
    overlays_list: list of lists of overlay PNG paths (each sublist is a frame)
    size: width and height for each composed image
    per_row: number of frames per row in the atlas
    """
    frames = []
    for overlays in overlays_list:
        composed = compose_images(base_png, overlays, size)
        frames.append(composed)

    atlas_cols = per_row
    atlas_rows = (len(frames) + atlas_cols - 1) // atlas_cols
    atlas_width = atlas_cols * size[0]
    atlas_height = atlas_rows * size[1]

    atlas = Image.new("RGBA", (atlas_width, atlas_height), (0, 0, 0, 0))

    for idx, frame in enumerate(frames):
        x = (idx % atlas_cols) * size[0]
        y = (idx // atlas_cols) * size[1]
        atlas.paste(frame, (x, y))

    atlas.save(output_path)
    print(f"Atlas saved as {output_path}")

# === Example Usage ===
if __name__ == "__main__":
    base_png_file = "Back.png"
    overlay_sets = [f for f in os.listdir('.') if os.path.isfile(f) and f.lower().endswith('.png')]
    overlay_sets.remove('Back.png')
    try:
        overlay_sets.remove('character_atlas.png')
    except:
        pass
    overlay_sets = [[x] for x in overlay_sets]
    create_atlas(base_png_file, overlay_sets, output_path="character_atlas.png", size=(300, 400), per_row=10)

