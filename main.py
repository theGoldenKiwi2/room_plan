import cv2
import os
import csv
from PIL import ImageFont, ImageDraw, Image
import tkinter as tk
from tkinter import simpledialog, StringVar, Label, Entry, Button, Radiobutton, W
import string

# paths and settings
IMG_PATH = 'map/AAC_006.jpg'
CSV_PATH = 'coord.csv'
FONT_PATH = 'NotoSans-Bold.ttf'
EXPORT_PATH = 'export.jpg'
DRAW_SHAPE = 'circle'  # "circle" ou "square"

def choose_mode():
    result = {"mode": None, "prefix": ""}

    def validate():
        mode = mode_var.get()
        result["mode"] = mode
        if mode == "préfix":
            prefix = entry_prefix.get().strip()
            if not prefix:
                label_error.config(text="Le préfixe ne peut pas être vide.")
                return
            result["prefix"] = prefix
        window.destroy()

    window = tk.Tk()
    window.title("Choix du mode de numérotation")

    mode_var = StringVar(value="chiffres")

    for m in ["chiffres", "lettres", "manuel", "préfix"]:
        Radiobutton(window, text=m.capitalize(), variable=mode_var, value=m).pack(anchor=W)

    entry_prefix = Entry(window)
    label_prefix = Label(window, text="Préfixe :", anchor=W)
    label_error = Label(window, text="", fg="red")

    def update_entry(*args):
        if mode_var.get() == "préfix":
            label_prefix.pack(anchor=W)
            entry_prefix.pack(anchor=W)
        else:
            label_prefix.pack_forget()
            entry_prefix.pack_forget()
        label_error.config(text="")

    mode_var.trace_add("write", update_entry)

    label_prefix.pack_forget()
    entry_prefix.pack_forget()

    Button(window, text="Valider", command=validate).pack(pady=10)
    label_error.pack()

    window.mainloop()
    return result["mode"], result["prefix"]

mode, prefix_global = choose_mode()

print(f"Mode sélectionné : {mode}")
if mode == "préfix":
    print(f"Préfixe utilisé : {prefix_global}")

counter = 1
letters = list(string.ascii_uppercase)

if os.path.isfile(CSV_PATH):
    os.remove(CSV_PATH)


img_cv2 = cv2.imread(IMG_PATH)
img_display = img_cv2.copy()
img_pil = Image.open(IMG_PATH)

height, width = img_cv2.shape[:2]
screen_width = 1280
screen_height = 800
scale = min(screen_width / width, screen_height / height, 1.0)
img_display_resized = cv2.resize(img_display, (int(width * scale), int(height * scale)))

scale_text = height / 1000
font_size = int(15 * scale_text)
font = ImageFont.truetype(FONT_PATH, font_size)

draw = ImageDraw.Draw(img_pil)

def click_event(event, x, y, flags, params):
    global counter

    if event == cv2.EVENT_LBUTTONDOWN:
        x_original = int(x / scale)
        y_original = int(y / scale)

        if mode == "manuel":
            label = simpledialog.askstring("Saisie manuelle", f"Texte pour le point ({x}, {y}) ?")
            if not label:
                print("Saisie annulée.")
                return
        elif mode == "chiffres":
            label = str(counter)
        elif mode == "lettres":
            if counter > len(letters):
                print("Plus de lettres disponibles.")
                return
            label = letters[counter - 1]
        elif mode == "préfix":
            label = f"{prefix_global}{counter}"

        print(f"Point placé : ({x_original}, {y_original}) -> {label}")

        # Enregistrement CSV
        with open(CSV_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([x_original, y_original, label])

        radius_display = int(22 * scale)
        font_scale = max(0.5, min(2.5, scale_text))
        cv2.circle(img_display_resized, (x, y), radius_display, (0, 0, 255), -1)
        cv2.putText(img_display_resized, label, (x - 10, y + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), int(font_scale * 1.5))

        radius_pil = 22
        if DRAW_SHAPE == "circle":
            draw.ellipse([(x_original - radius_pil, y_original - radius_pil),
                          (x_original + radius_pil, y_original + radius_pil)],
                         fill='white', outline='black', width=2)
        elif DRAW_SHAPE == "square":
            draw.rectangle([(x_original - radius_pil, y_original - radius_pil),
                            (x_original + radius_pil, y_original + radius_pil)],
                           fill='white', outline='black', width=2)

        draw.text((x_original, y_original), label, fill='red', anchor='mm', font=font)

        counter += 1

cv2.namedWindow('Point Coordinates')
cv2.setMouseCallback('Point Coordinates', click_event)

print("Clique sur l'image pour placer les points. Appuie sur ESC pour terminer.")

while True:
    cv2.imshow('Point Coordinates', img_display_resized)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break

cv2.destroyAllWindows()

img_pil.save(EXPORT_PATH)
print(f"Image exportée dans : {EXPORT_PATH}")
