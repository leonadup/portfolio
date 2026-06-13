from PIL import Image
import matplotlib.pyplot as plt

img = Image.open("images/image_chemin_foret.bmp")

plt.imshow(img)
plt.axis("on")

def on_click(event):
    x, y = int(event.xdata), int(event.ydata)
    pixel = img.load()[x, y]
    print(f"Pixel ({x},{y}) = {pixel}")

plt.connect("button_press_event", on_click)
plt.show()
