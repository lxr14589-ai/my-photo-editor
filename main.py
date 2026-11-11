import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance, ImageTk
image = None  # Global variable to hold the original image
canvas_photo = None
selection_start = None
selection_rect = None
preview_size = (0, 0)
crop_mode = False
history = []


def get_adjusted_image():
    brightness = float(brightness_slider.get()) / 100
    contrast = float(contrast_slider.get()) / 100
    saturation = float(saturation_slider.get()) / 100

    result = ImageEnhance.Brightness(image).enhance(brightness)
    result = ImageEnhance.Contrast(result).enhance(contrast)
    return ImageEnhance.Color(result).enhance(saturation)


def open_image():
    global image
    file_path = filedialog.askopenfilename(
        title="选择图片",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )

    if not file_path:
        return

    image = Image.open(file_path)
    history.clear()
    brightness_slider.set(100)
    contrast_slider.set(100)
    saturation_slider.set(100)
    update_preview()

    preview_image = image.copy()
    preview_image.thumbnail((760, 520))
    print("图片尺寸：", image.size)
    print("图片模式：", image.mode)
    print("预览尺寸：", preview_image.size)


def save_image():
    if image is None:
        return

    file_path = filedialog.asksaveasfilename(
        title="另存为",
        defaultextension=".png",
        filetypes=[
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ]
    )
    if not file_path:
        return

    result = get_adjusted_image()
    try:
        result.save(file_path)
    except (OSError, ValueError) as error:
        messagebox.showerror("保存失败", f"无法保存图片：{error}")


def reset_image():
    brightness_slider.set(100)
    contrast_slider.set(100)
    saturation_slider.set(100)
    update_preview()


def undo_image():
    global image
    if not history:
        return
    image = history.pop()
    update_preview()


def enable_crop_mode():
    global crop_mode
    if image is None:
        return
    crop_mode = True


def update_preview(_value=None):
    global canvas_photo, preview_size
    if image is None:
        return

    result = get_adjusted_image()

    preview_image = result.copy()
    preview_image.thumbnail((760, 520))
    preview_size = preview_image.size
    canvas_photo = ImageTk.PhotoImage(preview_image)
    image_canvas.delete("all")
    image_canvas.create_image(0, 0, anchor=tk.NW, image=canvas_photo)


def start_selection(event):
    global selection_start, selection_rect
    if image is None or not crop_mode:
        return

    selection_start = (event.x, event.y)
    selection_rect = image_canvas.create_rectangle(
        event.x,
        event.y,
        event.x,
        event.y,
        outline="red",
        width=2
    )


def update_selection(event):
    if not crop_mode or selection_start is None or selection_rect is None:
        return

    image_canvas.coords(
        selection_rect,
        selection_start[0],
        selection_start[1],
        event.x,
        event.y
    )


def on_release(event):
    global image, selection_start, selection_rect, crop_mode
    if selection_start is None or image is None or not crop_mode:
        return

    history.append(image.copy())
    
    left = min(selection_start[0], event.x)
    top = min(selection_start[1], event.y)
    right = max(selection_start[0], event.x)
    bottom = max(selection_start[1], event.y)

    preview_width, preview_height = preview_size
    left = max(0, min(left, preview_width))
    top = max(0, min(top, preview_height))
    right = max(0, min(right, preview_width))
    bottom = max(0, min(bottom, preview_height))

    if left == right or top == bottom:
        selection_start = None
        selection_rect = None
        crop_mode = False
        return

    scale_x = image.width / preview_width
    scale_y = image.height / preview_height
    original_box = (
        int(left * scale_x),
        int(top * scale_y),
        int(right * scale_x),
        int(bottom * scale_y)
    )
    image = image.crop(original_box)
    print("原图裁剪坐标：", original_box)
    update_preview()
    selection_start = None
    selection_rect = None
    crop_mode = False


def on_change(value):
    update_preview(value)


root = tk.Tk()
root.title("My Photo Editor")
root.geometry("800x600")

button = tk.Button(
    root,
    text="打开图片",
    command=open_image
)
button.pack()
save_button = tk.Button(
    root,
    text="另存为",
    command=save_image
)
save_button.pack()
reset_button = tk.Button(
    root,
    text="重置",
    command=reset_image
)
reset_button.pack()
crop_button = tk.Button(
    root,
    text="裁剪",
    command=enable_crop_mode
)
crop_button.pack()
undo_button = tk.Button(
    root,
    text="撤销",
    command=undo_image
)
undo_button.pack()
brightness_slider = tk.Scale(
    root,
    from_=0,
    to=200,
    orient=tk.HORIZONTAL,
    label="亮度调整",
    command=on_change
)
brightness_slider.pack()
contrast_slider = tk.Scale(
    root,
    from_=0,
    to=200,
    orient=tk.HORIZONTAL,
    label="对比度调整",
    command=update_preview
)
contrast_slider.set(100)
contrast_slider.pack()
saturation_slider = tk.Scale(
    root,
    from_=0,
    to=200,
    orient=tk.HORIZONTAL,
    label="饱和度调整",
    command=update_preview
)
saturation_slider.set(100)
saturation_slider.pack()
image_canvas = tk.Canvas(root, width=760, height=520, background="white")
image_canvas.pack()
image_canvas.bind("<Button-1>", start_selection)
image_canvas.bind("<B1-Motion>", update_selection)
image_canvas.bind("<ButtonRelease-1>", on_release)

root.mainloop()