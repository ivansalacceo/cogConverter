import os
import tkinter as tk
from tkinter import filedialog, messagebox
from rio_cogeo.cogeo import cog_translate
from rio_cogeo.profiles import cog_profiles

def convert_to_cog():
    # 1. Ask the user to select an input file
    input_path = filedialog.askopenfilename(
        title="Select GeoTIFF",
        filetypes=[("TIFF files", "*.tif *.tiff")]
    )
    
    if not input_path:
        return # User cancelled

    # 2. Determine output path (appends '_cog' to the original filename)
    file_dir, file_name = os.path.split(input_path)
    base_name, ext = os.path.splitext(file_name)
    output_path = os.path.join(file_dir, f"{base_name}_cog.tif")

    try:
        # Update UI to show processing state
        btn_convert.config(text="Processing... Please wait", state=tk.DISABLED)
        root.update()

        # 3. Setup rio-cogeo profile with DEFLATE compression
        dst_profile = cog_profiles.get("deflate")
        
        # 4. Perform the conversion
        cog_translate(
            input_path,
            output_path,
            dst_profile,
            in_memory=True, # Processes in memory (faster if RAM allows)
            quiet=True
        )

        messagebox.showinfo("Success", f"COG created successfully!\n\nSaved at:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during conversion:\n\n{str(e)}")
    
    finally:
        # Reset UI
        btn_convert.config(text="Select GeoTIFF to Convert", state=tk.NORMAL)

# --- Build the UI ---
root = tk.Tk()
root.title("COG Converter")
root.geometry("400x200")
root.eval('tk::PlaceWindow . center')

lbl_title = tk.Label(root, text="Cloud Optimized GeoTIFF Converter", font=("Arial", 10, "bold"))
lbl_title.pack(pady=20)

btn_convert = tk.Button(root, text="Select GeoTIFF to Convert", command=convert_to_cog, padx=20, pady=10, bg="#4CAF50", fg="black", font=("Arial", 10))
btn_convert.pack(pady=10)

root.mainloop()