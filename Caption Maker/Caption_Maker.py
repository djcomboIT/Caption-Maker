import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import random
import os


class App:
    def __init__(self, master):
          
        # Get the current directory
        current_dir = os.getcwd()

        # Set default paths for input, output, and phrases folders
        input_path = os.path.join(current_dir, 'input')
        output_path = os.path.join(current_dir, 'output')
        phrases_path = os.path.join(current_dir, 'phrases')

        # Check if the default paths exist, and create them if not
        for path in [input_path, output_path, phrases_path]:
            if not os.path.exists(path):
                os.makedirs(path)

        self.master = master
        master.title("Image Text Generator")

        self.input_button = tk.Button(master, text="Select Input Folder", command=self.select_input_folder)
        self.input_button.pack()

        self.output_button = tk.Button(master, text="Select Output Folder", command=self.select_output_folder)
        self.output_button.pack()

        self.phrases_button = tk.Button(master, text="Select Phrases Folder", command=self.select_phrases_folder)
        self.phrases_button.pack()

        self.generate_button = tk.Button(master, text="Generate", command=self.generate_images)
        self.generate_button.pack()

        self.input_path = tk.StringVar(value=input_path)
        self.output_path = tk.StringVar(value=output_path)
        self.phrases_path = tk.StringVar(value=phrases_path)
        self.phrases1 = []
        self.phrases2 = []

        self.font_size = 72
        self.font = ImageFont.truetype('impact.ttf', size=self.font_size)        

    def select_input_folder(self):
        initial_dir = os.path.dirname(os.path.abspath(__file__))
        input_path = filedialog.askdirectory(title='Select Input Folder', initialdir=initial_dir)
        self.input_path.set(input_path)

    def select_output_folder(self):
        initial_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = filedialog.askdirectory(title='Select Output Folder', initialdir=initial_dir)
        self.output_path.set(output_path)

    def select_phrases_folder(self):
        initial_dir = os.path.dirname(os.path.abspath(__file__))
        phrases_path = filedialog.askdirectory(title='Select Phrases Folder', initialdir=initial_dir)
        self.phrases_path.set(phrases_path)

    def generate_images(self):
        input_path = self.input_path.get()
        output_path = self.output_path.get()

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        phrases_path = os.path.join(os.getcwd(), self.phrases_path.get())

        with open(os.path.join(phrases_path, 'phrases1.txt')) as f:
            self.phrases1 = f.readlines()

        self.phrases1 = [phrase.strip() for phrase in self.phrases1]

        with open(os.path.join(phrases_path, 'phrases2.txt')) as f:
            self.phrases2 = f.readlines()

        self.phrases2 = [phrase.strip() for phrase in self.phrases2]

    # Define a reference height and a reference font size
        ref_height = 1000
        ref_font_size = 100
        counter = 0
        for filename in os.listdir(input_path):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                filepath = os.path.join(input_path, filename)
                text = random.choice(self.phrases1) + ' ' + random.choice(self.phrases2)
                image = Image.open(filepath)

                draw = ImageDraw.Draw(image)

             # Calculate the ratio between the actual image height and the reference height
                height_ratio = image.height / ref_height

            # Adjust the font size proportional to the ratio
                font_size = round(ref_font_size * height_ratio)
                font = ImageFont.truetype('impact.ttf', size=font_size)

                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                x = (image.width - text_width) // 2
                y = round(10 * height_ratio)

                outline_size = round(3 * height_ratio * font_size / ref_font_size) + 1
                outline_color = 'black'
                draw.text((x-outline_size, y-outline_size), text, font=font, fill=outline_color)
                draw.text((x+outline_size, y-outline_size), text, font=font, fill=outline_color)
                draw.text((x-outline_size, y+outline_size), text, font=font, fill=outline_color)
                draw.text((x+outline_size, y+outline_size), text, font=font, fill=outline_color)

                draw.text((x, y), text, font=font, fill='pink')

                output_filename = os.path.splitext(filename)[0] + '_text.jpg'
                output_filepath = os.path.join(output_path, output_filename)
                image = image.convert('RGB')
                image.save(output_filepath)
                counter += 1
                print(f'Processed {counter} files')



root = tk.Tk()
app = App(root)
root.mainloop()
