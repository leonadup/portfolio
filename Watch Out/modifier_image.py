from PIL import Image

img = Image.open("lampadaire.png")
img = img.convert("RGB")
img.save("image_lampadaire.bmp")

print("Image convertie en BMP")
