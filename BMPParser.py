import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
from typing import Tuple, Dict
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

class MyGUI:
    def __init__(self, root):
        self.root = root
        # self.root.geometry("1000x1000")  # Looks bad adjust later if needed
        self.root.title("BMP Image Viewer")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # self.style.theme_use('default')


        # Variables for storing metadata and information about the img to be displayed
        self.image_data = None
        self.original_width = 0
        self.original_height = 0
        self.width = 0
        self.height = 0
        self.bits_per_pixel = 0
        self.original_image_data = None
        self.color_table = None

        # Thread pool for parallel processing
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.update_queue = Queue()
        self.processing = False

        # Start update monitoring thread
        self.update_thread = Thread(target=self._monitor_updates, daemon=True)
        self.update_thread.start()

        # Calling GUI function for Creating the whole GUI
        self.__init__ui()

    '''
     1. Creating the components of the UI;
     2. Important notes col:200 is the center of the UI
     3. For future UI: Use padx = 20 for medium padding from the very left and 10 for minimal padding
     4. For slider used tl.Label instead opf label in tk.Scale as couldn't Adjust the location of the label
     '''
    def __init__ui(self):

        # Used https://docs.python.org/3/library/tkinter.ttk.html for implementing the GUI

        # Main Container
        main_container = ttk.Frame(self.root, padding=10)
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        #Title of the BMP APP con the ttk frame
        title_label = ttk.Label(main_container , text="BMP Image Viewer Application", font=("Helvetica", 16, "bold"))
        title_label.grid(column=0, row=0, columnspan=3, pady=10)


        # Frame for the foile selection
        file_frame = ttk.LabelFrame(main_container, text="File Selection", padding="5")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # Path of BMP file
        ttk.Label(file_frame, text="Path of BMP file",font=("Helvetica", 16, "bold")).grid(column=0, row=0, pady=5, padx=5)
        self.file_path_entry = ttk.Entry(file_frame, width=50)
        self.file_path_entry.grid(row=0, column=1, padx=5)
        # Path of BMP file : Path entry and button
        ttk.Button(file_frame, text="Browse", command=self.browse_bmpfile).grid(row=0, column=2, padx=5)

        # Create two columns: left for controls, right for image
        controls_frame = ttk.Frame(main_container)
        controls_frame.grid(row=2, column=0, sticky=(tk.N, tk.S), padx=10)

        #  Metadata section
        metadata_frame = ttk.LabelFrame(controls_frame, text="Metadata", padding="5")
        metadata_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        # Default Metadata that displays if no bmp file is selected or if the function fails
        # Update the config later fot changing the text
        self.metadata_labels = {
            "File Size": ttk.Label(metadata_frame, text="File Size: N/A"),
            "Width": ttk.Label(metadata_frame, text="Width: N/A"),
            "Height": ttk.Label(metadata_frame, text="Height: N/A"),
            "Bits Per Pixel": ttk.Label(metadata_frame, text="Bits Per Pixel: N/A")
        }

        for i, (key, label) in enumerate(self.metadata_labels.items()):
            label.grid(row=i, column=0, sticky="w", pady=2)

        # Image display
        # Height and width to be adjusted: Ask David about this IMPORTANT!
        self.canvas = tk.Canvas(main_container, width=600, height=400, bg="lightgray")
        self.canvas.grid(row=2, column=1, padx=10, pady=10)

        # Controls section
        controls_label_frame = ttk.LabelFrame(controls_frame, text="Controls", padding="5")
        controls_label_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        '''
         Using the command arguement on the slider called the function continously resulting in Unnecessary function calls
         So instead added an event when the user release the slider at particular brightness.  
        '''

        # Slider for the Brightness
        ttk.Label(controls_label_frame, text="Brightness").grid(row=0, column=0, sticky=tk.W)
        self.brightness_var = tk.IntVar(value=50)
        self.brightness_slider = ttk.Scale(controls_label_frame, from_=0, to=100, orient="horizontal", variable=self.brightness_var)
        self.brightness_slider.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        # Another slider for the scaling
        # Scale control
        ttk.Label(controls_label_frame, text="Scale:").grid(row=2, column=0, sticky=tk.W)
        self.scale_var = tk.IntVar(value=100)
        self.scale_slider = ttk.Scale(controls_label_frame, from_=10, to=100, orient="horizontal", variable=self.scale_var)
        self.scale_slider.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        self.brightness_slider.bind("<ButtonRelease-1>", lambda event: self._update_display())
        self.scale_slider.bind("<ButtonRelease-1>", lambda event: self._update_display())

        # RGB Channel Toggles

        # Frame for RGB checkboxes
        rgb_frame = ttk.LabelFrame(controls_label_frame, text="RGB Channels", padding="5")
        rgb_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)

        self.r_var = tk.BooleanVar(value=True)
        self.g_var = tk.BooleanVar(value=True)
        self.b_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(rgb_frame, text="Red", variable=self.r_var, command=self.toggle_channels).grid(row=0, column=0, padx=5)
        ttk.Checkbutton(rgb_frame, text="Green", variable=self.g_var, command=self.toggle_channels).grid(row=0, column=1, padx=5)
        ttk.Checkbutton(rgb_frame, text="Blue", variable=self.b_var, command=self.toggle_channels).grid(row=0, column=2, padx=5)

    def browse_bmpfile(self):
        file_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.BMP")])
        if not file_path:
            return
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, file_path)
        try:
            with open(file_path, "rb") as file:
                bmp_bytes = file.read()
            # Check if the file is a BMP file
            if bmp_bytes[:2] != b'BM':
                messagebox.showwarning("Warning", "BMP file must be BMP file.")
                return
            
            self.parse_metadata(bmp_bytes)
            self.load_image_data(bmp_bytes)
        except Exception as e:
            messagebox.showwarning("Warning", str(e))
            return


    def parse_metadata(self, bmp_bytes):
        try:
            file_size = int.from_bytes(bmp_bytes[2:6],"little")
            self.width = int.from_bytes(bmp_bytes[18:22],"little")
            self.height = int.from_bytes(bmp_bytes[22:26],"little")
            self.bits_per_pixel = int.from_bytes(bmp_bytes[28:30],"little")

            self.metadata_labels["File Size"].config(text=f"File Size: {file_size} bytes")
            self.metadata_labels["Width"].config(text=f"Width: {self.width} pixels")
            self.metadata_labels["Height"].config(text=f"Height: {self.height} pixels")
            self.metadata_labels["Bits Per Pixel"].config(text=f"Bits Per Pixel: {self.bits_per_pixel}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        return

    def _read_color_table(self, bmp_bytes: bytes) -> list:
        """Read color table for images with ≤ 8 bits per pixel."""
        colors = []
        color_table_offset = 54  # Standard header size
        entries = 2 ** self.bits_per_pixel

        for i in range(entries):
            offset = color_table_offset + (i * 4)
            b = bmp_bytes[offset]
            g = bmp_bytes[offset + 1]
            r = bmp_bytes[offset + 2]
            colors.append((r, g, b))

        return colors

    def _read_pixel_data(self, bmp_bytes: bytes, data_offset: int) -> list:
        """Read and parse pixel data from BMP file."""
        pixels = []
        row_size = ((self.bits_per_pixel * self.width + 31) // 32) * 4

        for y in range(self.height):
            row = []
            row_offset = data_offset + (y * row_size)

            if self.bits_per_pixel == 24:
                for x in range(self.width):
                    pixel_offset = row_offset + (x * 3)
                    b = bmp_bytes[pixel_offset]
                    g = bmp_bytes[pixel_offset + 1]
                    r = bmp_bytes[pixel_offset + 2]
                    row.append((r, g, b))
            elif self.bits_per_pixel <= 8:
                for x in range(self.width):
                    byte_offset = row_offset + (x * self.bits_per_pixel // 8)
                    pixel_value = bmp_bytes[byte_offset]
                    if self.bits_per_pixel < 8:
                        bits_to_shift = 8 - ((x % (8 // self.bits_per_pixel) + 1) * self.bits_per_pixel)
                        mask = (1 << self.bits_per_pixel) - 1
                        pixel_value = (pixel_value >> bits_to_shift) & mask
                    row.append(self.color_table[pixel_value])

            pixels.insert(0, row)  # BMP stores rows bottom-to-top

        return pixels

    def _monitor_updates(self):
        # Adding a monitor for possible updates to run in threads
        while True:
            try:
                pixels = self.update_queue.get()
                if pixels is not None:
                    self.root.after(0, self._update_canvas, pixels)
                self.update_queue.task_done()
            except:
                continue

    def display_image(self):
        if self.image_data is None:
            return

        pixels = self.scale_image(self.image_data)  # Apply scaling

        # Create a PhotoImage from pixel data
        photo_image = self._create_photo_image(pixels)

        # Update canvas to display the image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)
        self.canvas.image = photo_image  # Keep reference to avoid garbage collection

    def _update_display(self, _=None):
        if self.original_image_data is None:
            return

        # Apply all transformations in sequence
        pixels = self.original_image_data

        # Scaling
        scale = self.scale_var.get() / 100
        pixels = self.scale_image(pixels, scale)

        # Brightness
        brightness = self.brightness_var.get()
        pixels = self._adjust_brightness_single_pass(pixels, brightness)

        # RGB Channels
        pixels = self._apply_rgb_channels(pixels)

        # Display
        self.image_data = pixels
        self.display_image()

    def _adjust_brightness_single_pass(self, pixels, brightness_value):
        brightness_scale = brightness_value / 50.0

        def adjust_row(row):
            new_row = []
            for (r, g, b) in row:
                y, u, v = self._rgb_to_yuv(r, g, b)
                y = y * brightness_scale
                y = max(0, min(255, y))  # Clamp Y value
                new_r, new_g, new_b = self._yuv_to_rgb(y, u, v)
                new_r = max(0, min(255, new_r))
                new_g = max(0, min(255, new_g))
                new_b = max(0, min(255, new_b))
                new_row.append((new_r, new_g, new_b))
            return new_row

        with ThreadPoolExecutor() as executor:
            adjusted = list(executor.map(adjust_row, pixels))

        return adjusted

    def _apply_rgb_channels(self, pixels):
        r_enabled = self.r_var.get()
        g_enabled = self.g_var.get()
        b_enabled = self.b_var.get()

        def filter_row(row):
            return [
                (r if r_enabled else 0,
                 g if g_enabled else 0,
                 b if b_enabled else 0)
                for (r, g, b) in row
            ]

        with ThreadPoolExecutor() as executor:
            filtered = list(executor.map(filter_row, pixels))

        return filtered

    # def adjust_brightness(self, value=None):
    #     if value is None:
    #         value = self.brightness_var.get()
    #
    #     if self.original_image_data is None:
    #         return
    #
    #     brightness_scale = value / 50.0
    #
    #     def adjust_row(row):
    #         new_row = []
    #         for (r, g, b) in row:
    #             y, u, v = self._rgb_to_yuv(r, g, b)
    #             y = y * brightness_scale
    #             y = max(0, min(255, y))  # Clamp Y value
    #             new_r, new_g, new_b = self._yuv_to_rgb(y, u, v)
    #             new_r = max(0, min(255, new_r))
    #             new_g = max(0, min(255, new_g))
    #             new_b = max(0, min(255, new_b))
    #             new_row.append((new_r, new_g, new_b))
    #         return new_row
    #
    #     with ThreadPoolExecutor() as executor:
    #         adjusted = list(executor.map(adjust_row, self.original_image_data))
    #
    #     self.image_data = adjusted
    #     self.display_image()

    #
    # def toggle_channels(self):
    #     # print("Hello from toggle channels")
    #     if self.image_data is None:
    #         return
    #
    #     def filter_row(row):
    #         return [
    #             (r if self.r_var.get() else 0,
    #              g if self.g_var.get() else 0,
    #              b if self.b_var.get() else 0)
    #             for (r, g, b) in row
    #         ]
    #
    #     with ThreadPoolExecutor() as executor:
    #         filtered = list(executor.map(filter_row, self.image_data))
    #
    #     self.image_data = filtered
    #     self.display_image()

    def _create_photo_image(self, pixels: list) -> tk.PhotoImage:
        width = len(pixels[0])
        height = len(pixels)

        ppm = f'P6\n{width} {height}\n255\n'

        for row in pixels:
            for (r, g, b) in row:
                ppm += chr(r) + chr(g) + chr(b)

        return tk.PhotoImage(data=ppm)


    def scale_image(self, pixels: list = None, scale: float = None) -> list:
        """Scale the image using nearest neighbor interpolation."""
        if pixels is None:
            pixels = self.image_data
        if scale is None:
            scale = self.scale_var.get() / 100

        try:
            if scale == 1:
                return pixels

            new_height = int(len(pixels) * scale)
            new_width = int(len(pixels[0]) * scale)

            def scale_row(y):
                row = []
                orig_y = min(int(y / scale), len(pixels) - 1)
                for x in range(new_width):
                    orig_x = min(int(x / scale), len(pixels[0]) - 1)
                    row.append(pixels[orig_y][orig_x])
                return row

            with ThreadPoolExecutor() as executor:
                scaled = list(executor.map(scale_row, range(new_height)))

            return scaled

        except Exception as e:
            messagebox.showerror("Error encountered during scaling:", str(e))
            return pixels


    def load_image_data (self, bmp_bytes):
        # print("Hello from load_image_data")
        try:
            # Parse header
            data_offset = int.from_bytes(bmp_bytes[10:14], 'little')

            # Read color table if needed
            if self.bits_per_pixel <= 8:
                self.color_table = self._read_color_table(bmp_bytes)

            # Read pixel data
            self.original_image_data = self._read_pixel_data(bmp_bytes, data_offset)
            self.image_data = self.original_image_data

            # Initial display
            self.display_image()

        except Exception as e:
            messagebox.showerror("Error while retrieving image data: ", str(e))

    # def adjust_brightness_event(self, event):
    #     value = self.brightness_slider.get()
    #     self.adjust_brightness(value)
    #
    # def scale_image_event(self, event):
    #     value = self.scale_slider.get()
    #     self.scale_image()

    def adjust_brightness_event(self, event):
        self._update_display()

    def scale_image_event(self, event):
        self._update_display()

    def toggle_channels(self):
        self._update_display()

    def _rgb_to_yuv(self, r, g, b):
        # Convert RGB to YUV
        y = 0.299 * r + 0.587 * g + 0.114 * b
        u = -0.299 * r - 0.587 * g + 0.886 * b
        v = 0.701 * r - 0.587 * g - 0.114 * b
        return y, u, v

    def _yuv_to_rgb(self, y, u, v):
        # Convert YUV to RGB
        r = y + v
        g = y - 0.195 * u - 0.510 * v
        b = y + u
        r = max(0, min(255, int(round(r))))
        g = max(0, min(255, int(round(g))))
        b = max(0, min(255, int(round(b))))
        return r, g, b

    def _update_canvas(self, pixels):
        """Update the canvas with processed pixels."""
        if pixels is None:
            return

        photo = self._create_photo_image(pixels)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo


if __name__ == '__main__':
    root = tk.Tk()
    MyGUI(root)
    root.mainloop()