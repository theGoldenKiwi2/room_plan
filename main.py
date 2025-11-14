"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, CePro & CMS, 2025"""
import cv2
import os
import csv
from PIL import ImageFont, ImageDraw, Image
import tkinter as tk
from tkinter import simpledialog, StringVar, Label, Entry, Button, Radiobutton, W
import string

# === Paths and basic settings ===
IMG_PATH = 'map/CM_1121.jpg'       # Input image to annotate
CSV_PATH = 'coord.csv'  # CSV file to save coordinates and labels
FONT_PATH = 'NotoSans-Bold.ttf'    # Font used to draw text on the image
EXPORT_PATH = 'export.jpg'         # Output image file
DRAW_SHAPE = 'circle'              # Shape of the marker: "circle" or "square"

def choose_mode():
    result = {"mode": None, "prefix": ""}

    def validate():
        """Called when the user clicks 'Validate'."""
        mode = mode_var.get()
        result["mode"] = mode
        if mode == "préfix":
            # Require a prefix if 'prefix' mode is selected
            prefix = entry_prefix.get().strip()
            if not prefix:
                label_error.config(text="Le préfixe ne peut pas être vide.")
                return
            result["prefix"] = prefix
        window.destroy()  # Close the window after validation

    window = tk.Tk()
    window.title("Choix du mode de numérotation")

    # Default mode is 'chiffres' (numbers)
    mode_var = StringVar(value="chiffres")

    # Create radio buttons for each mode
    for m in ["chiffres", "lettres", "manuel", "préfix"]:
        Radiobutton(window, text=m.capitalize(), variable=mode_var, value=m).pack(anchor=W)

    entry_prefix = Entry(window)
    label_prefix = Label(window, text="Préfixe :", anchor=W)
    label_error = Label(window, text="", fg="red")

    def update_entry(*args):
        """Show or hide the prefix input depending on the selected mode."""
        if mode_var.get() == "préfix":
            label_prefix.pack(anchor=W)
            entry_prefix.pack(anchor=W)
        else:
            label_prefix.pack_forget()
            entry_prefix.pack_forget()
        label_error.config(text="")

    mode_var.trace_add("write", update_entry)

    # Hide prefix input by default
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

counter = 1                     # Used to increment labels
letters = list(string.ascii_uppercase)
points_history = []              # Stores all (x, y, label)

# Remove old CSV file if it exists
if os.path.isfile(CSV_PATH):
    os.remove(CSV_PATH)

img_cv2 = cv2.imread(IMG_PATH)
img_display = img_cv2.copy()
img_pil = Image.open(IMG_PATH)

height, width = img_cv2.shape[:2]

# Resize image for display if too big
screen_width = 1280
screen_height = 800
scale = min(screen_width / width, screen_height / height, 1.0)
img_display_resized = cv2.resize(img_display, (int(width * scale), int(height * scale)))

# Font scaling depending on image height
scale_text = height / 1000
font_size = int(50 * scale_text)
font = ImageFont.truetype(FONT_PATH, font_size)

draw = ImageDraw.Draw(img_pil)


def redraw_all_points():
    """Rebuild the displayed and saved image with all points."""
    global img_display_resized, img_pil, draw

    img_display_resized = cv2.resize(img_cv2.copy(), (int(width * scale), int(height * scale)))
    img_pil = Image.open(IMG_PATH)
    draw = ImageDraw.Draw(img_pil)

    for x, y, label in points_history:
        # Scale coordinates for the OpenCV window
        x_scaled = int(x * scale)
        y_scaled = int(y * scale)

        # Draw filled circle and label in the OpenCV preview
        radius_display = int(20 * scale)
        font_scale = max(0.4, min(1.2, scale_text))
        cv2.circle(img_display_resized, (x_scaled, y_scaled), radius_display, (0, 0, 255), -1)
        cv2.putText(img_display_resized, label, (x_scaled - 10, y_scaled + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), 1)

        # Draw corresponding marker in the saved PIL image
        radius_pil = 52
        if DRAW_SHAPE == "circle":
            draw.ellipse([(x - radius_pil, y - radius_pil),
                          (x + radius_pil, y + radius_pil)])
        elif DRAW_SHAPE == "square":
            draw.rectangle([(x - radius_pil, y - radius_pil),
                            (x + radius_pil, y + radius_pil)])
        draw.text((x, y), label, fill='red', anchor='mm', font=font)

def save_csv():
    """Save only coordinates (x, y) into the CSV file (no label)."""
    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        for x, y, label in points_history:
            writer.writerow([x, y])

def click_event(event, x, y, flags, params):
    """Handle clicks on the image to place labeled points."""
    global counter

    if event == cv2.EVENT_LBUTTONDOWN:
        # Convert click coordinates to original image scale
        x_original = int(x / scale)
        y_original = int(y / scale)

        # Choose the label depending on the selected mode
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

        # Store and save the point
        points_history.append((x_original, y_original, label))
        save_csv()
        redraw_all_points()

        counter += 1


cv2.namedWindow('Point Coordinates')
cv2.setMouseCallback('Point Coordinates', click_event)

print("Clique sur l'image pour placer les points. Appuie sur ESC pour terminer, 'u' pour annuler le dernier point.")

while True:
    cv2.imshow('Point Coordinates', img_display_resized)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord('u'):  # Undo last point
        if points_history:
            removed = points_history.pop()
            counter -= 1
            print(f"Annulé : {removed}")
            save_csv()
            redraw_all_points()
        else:
            print("Aucun point à annuler.")

cv2.destroyAllWindows()

img_pil.save(EXPORT_PATH)
print(f"Image exportée dans : {EXPORT_PATH}")
