from PIL import Image,ImageEnhance

image = Image.open(r"D:\Easy Photo Editor\IMG20260911160140.jpg ")

enhancer = ImageEnhance.Brightness(image)

result = enhancer.enhance(1.5)

result.show()
