from PIL import Image, ImageOps
from os import listdir

def slice_image(from_file, to_file, slice_width):
    """Split up the image in the visualizer/textures/ directory with the file name
    <from_file>.png into 'slices' of width <slice_width>,
    and put them in files with names in the form <to_file>_[number].png. """
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

def rescale_image(file):
    """Crop and scale the image in the file with the name <file>.png
    so that it fits within a 70 by 70 pixel image.
    Specifically, scale it so that it has a width of 70 pixels, then
    align it at the top of a new 70-by-70 image file with the same name."""
    img = Image.open(file + ".png")
    out = Image.new('RGBA', (70, 70), (0, 0, 0, 0))

    new_h = round(img.height * (70 / img.width))
    x = img.crop((0, 0, img.width, img.height)).resize((70, new_h))

    out.paste(x, (0, 70 - new_h, 70, 70))
    out.save(file+".png")

def _flip(file):
    """Mirror the image at the location <file>. If the name as in the form <a>_<b>,
    save it as <a>_flipped_<b>; otherwise, append _flipped to the name. """
    img = Image.open(file)
    img = ImageOps.mirror(img)
    try:
        if '_' in file:
            a, b = file.split("_")
            img.save(a+"_flipped_"+b)
        else:
            a, b = file.split(".")
            img.save(a+"_flipped."+b)
        print("flipped", file)
    except Exception as e:
        print("couldn't flip", file, e)
    

def flip(directory):
    """Apply _flip to all PNG files in the given directory."""
    for file in listdir(directory):
        if file.endswith(".png"):
            _flip(directory + file)

def transparify(file):
    """Turns all fully opaque white pixels in an image <file>.png transparent."""
    img = Image.open(file+".png").convert("RGBA")
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    for y in range(img.height):
        for x in range(img.width):
            color = img.getpixel((x, y))
            if color != (255, 255, 255, 255):
                out.putpixel((x, y), color)
    out.save(file+".png", "PNG")
    out.show()