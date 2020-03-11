from PIL import Image

def transparify(file):
    img = Image.open(file+".png").convert("RGBA")

    out = Image.new("RGBA", img.size, (0, 0, 0, 0))

    for y in range(img.height):
        for x in range(img.width):
            color = img.getpixel((x, y))
            if color != (255, 255, 255, 255):
                out.putpixel((x, y), color)

    out.save(file+".png", "PNG")
    out.show()

transparify("assets/teleporters/teleporter3")
