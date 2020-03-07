from PIL import Image

def animate(from_file, to_file, slice_width):
    from_img = Image.open("visualizer/textures/"+from_file+".png")
    to_img = Image.open("visualizer/textures/"+to_file+".png")

    width = slice_width
    while width < from_img.width:
        new_image = Image.new('RGBA', from_img.size, (0, 0, 0, 0))
        
        from_rect = (width, 0, from_img.width, from_img.height)
        to_rect = (0, 0, width, to_img.height)
        new_image.paste(from_img.crop(from_rect), from_rect)
        new_image.paste(to_img.crop(to_rect), to_rect)

        new_image.save(f"out/{from_file}_to_{to_file}_slice_{width // slice_width}.png", "PNG")

        width += slice_width

animate("door_openTop", "door_closedTop", 1)
animate("door_openMid", "door_closedMid", 1)

def fix(file):
    img = Image.open(file + ".png")
    out = Image.new('RGBA', (70, 70), (0, 0, 0, 0))

    new_h = round(img.height * (70 / img.width))
    x = img.crop((0, 0, img.width, img.height)).resize((70, new_h))

    out.paste(x, (0, 70 - new_h, 70, 70))
    out.save(file+"_fixed.png")
