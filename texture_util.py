from PIL import Image, ImageOps
from os import listdir

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

def fix(file):
    img = Image.open(file + ".png")
    out = Image.new('RGBA', (70, 70), (0, 0, 0, 0))

    new_h = round(img.height * (70 / img.width))
    x = img.crop((0, 0, img.width, img.height)).resize((70, new_h))

    out.paste(x, (0, 70 - new_h, 70, 70))
    out.save(file+".png")

def _flip(file):
    img = Image.open(file)
    img = ImageOps.mirror(img)
    if '_' in file:
        print(file)
        a, b = file.split("_")
        img.save(a+"_flipped_"+b)
    else:
        a, b = file.split(".")
        img.save(a+"_flipped."+b)
    

def flip(player_directory):
    for file in listdir(player_directory):
        if file.endswith(".png"):
            _flip(player_directory + file)
