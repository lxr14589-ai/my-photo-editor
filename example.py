from PIL import Image

image = Image.open(r"D:\Easy Photo Editor\IMG20260911160140.jpg ")

small_image = image.copy

small_image.thumbnail((500,300))

print("Original size:",image.size)
print("Thumbnail size:",small_image.size)

small_image.show()
