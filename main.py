import tkinter as tk
from io import BytesIO
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests
from tkmacosx import Button

#you can choose the background color

TITLE="Image Watermarker"
FONT_NAME = "Courier"
COLOR1 = "#9F8383" # entries frame
COLOR2 = "#574964" # text in entries, labels
COLOR3 = "#C8AAAA" # entry background
COLOR4 = "#FFDAB3"  # window background, buttons

#-------------------------WATERMARK APP--------------------------------------------
class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title(TITLE)
        self.root.config(padx=100,pady=50,bg=COLOR4)

        # URL Entry
        self.url_label = tk.Label(root, text="Image URL:", font=(FONT_NAME, 20, "bold"), fg=COLOR2, bg=COLOR4)
        self.url_label.grid(column=3, row=0)
        self.url_entry = tk.Entry(root, width=50, font=(FONT_NAME, 14, "italic"),highlightbackground=COLOR1, bg=COLOR3, fg=COLOR2)
        self.url_entry.grid(column=1, row=1, columnspan=4)
        
        # Button to load image
        
        self.load_button = Button(root, text="Load image from url", font=FONT_NAME, background=COLOR4, foreground=COLOR2, borderless=1, activebackground=COLOR3, activeforeground=COLOR4,focuscolor=COLOR2, command=self.load_image)
        self.open_button = Button(root, text="Open image from PC",font=FONT_NAME, background=COLOR4, foreground=COLOR2, borderless=1,activebackground=COLOR3, activeforeground=COLOR4,focuscolor=COLOR2, command=self.open_image)
        
        self.load_button.grid(column=3, row=2)
        self.open_button.grid(column=3, row=3)
        
        # Canvas to display image
        self.canvas = tk.Canvas(root, width=500, height=500, bg=COLOR4, highlightthickness=0)
        self.canvas.grid(column=3,row=4)

        # Watermark Entry
        self.watermark_label = tk.Label(root, text="Watermark Text:", font=(FONT_NAME, 20, "bold"), fg=COLOR2, bg=COLOR4)
        self.watermark_label.grid(column=3, row=5)
        self.watermark_entry = tk.Entry(root, width=50, font=(FONT_NAME, 14, "italic"), highlightbackground=COLOR1, bg=COLOR3, fg=COLOR2)
        self.watermark_entry.grid(column=1, row=6, columnspan=4)

        # Button to apply watermark
        self.watermark_button = Button(root, text="Apply Watermark", font=FONT_NAME, background=COLOR4, foreground=COLOR2, borderless=1,activebackground=COLOR3, activeforeground=COLOR4,highlightbackground=COLOR4, relief="flat", focuscolor=COLOR2,command=self.apply_watermark, state=tk.NORMAL)
        self.watermark_button.grid(column=3, row=7)

        # Button to save image
        self.save_button = Button(root, text="Save Image",bg=COLOR4,font=FONT_NAME, background=COLOR4, foreground=COLOR2, borderless=1,activebackground=COLOR3, activeforeground=COLOR4,focuscolor=COLOR2, command=self.save_image, state=tk.DISABLED)
        self.save_button.grid(column=3, row=8)
        
        self.image = None
        self.tk_image = None
        
#--------------------------FUNCTIONS---------------------------------------------------
    def load_image(self):
        url = self.url_entry.get()
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content)).convert("RGBA")
                self.image = img
                self.display_image(img)
            except Exception as e:
                print(f"Error loading image: {e}")
                
    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            try:
                img = Image.open(file_path).convert("RGBA")
                self.image = img
                self.display_image(img)
            except Exception as e:
                print(f"Error opening image: {e}")
    
    def display_image(self, img):
        img.thumbnail((400, 400))
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(250, 250, anchor=tk.CENTER, image=self.tk_image)

    def apply_watermark(self):
        if self.image is None:
            return

        watermark_text = self.watermark_entry.get()
        if not watermark_text:
            return

        img = self.image.copy()
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Load font (uses default if custom font is unavailable)
        try:
            font = ImageFont.truetype(FONT_NAME, int(height * 0.05))
        except:
            font = ImageFont.load_default()

        bbox=draw.textbbox((0,0), watermark_text, font=font) # bbox=(x_min, y_min, x_max, y_max) so bbox[2] is x_max and bbox[3] is y_max
        text_width= bbox[2] - bbox [0] #x_max - x_min ; 150 - 0 = 150 px wide (right boundary of the text is 150px, the width of the watermark text
        text_height = bbox[3] - bbox[1] #y_max - y_min ; 50 - 0 = 50 px tall
        position = (width - text_width - 10, height - text_height - 10) # Bottom-right corner; 10 px from the bottom edge and right edge

        # Apply watermark
        draw.text(position, watermark_text, fill=(255, 0, 255, 64), font=font) #(RGB T)

        self.image = img
        self.display_image(img)
        self.save_button.config(state=tk.NORMAL)
        self.watermark_button.config(state=tk.DISABLED)

    def save_image(self):
        if self.image is None:
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All Files", "*.*")])
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Image Saved", f"Image saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()