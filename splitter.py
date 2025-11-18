import os
import shutil
from PyPDF2 import PdfReader, PdfWriter

# Input and output folders
input_folder = "data/pdf"
output_folder = "data/split_output"

one_page_folder = os.path.join(output_folder, "one_page")
split_pages_folder = os.path.join(output_folder, "split_pages")
multi_originals_folder = os.path.join(output_folder, "multi_originals")

# Make sure the output folders exist
for d in (output_folder, one_page_folder, split_pages_folder, multi_originals_folder):
    os.makedirs(d, exist_ok=True)

# Loop through all PDF files in the input folder
for filename in os.listdir(input_folder):
    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(input_folder, filename)
    base_name = os.path.splitext(filename)[0]

    print(f"Processing: {filename}")

    try:
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)

        # If PDF has only 1 page -> move the original file to one_page_folder
        if num_pages == 1:
            dest_path = os.path.join(one_page_folder, filename)
            # If destination exists, add suffix to avoid overwrite
            if os.path.exists(dest_path):
                name, ext = os.path.splitext(filename)
                i = 1
                while os.path.exists(os.path.join(one_page_folder, f"{name}_{i}{ext}")):
                    i += 1
                dest_path = os.path.join(one_page_folder, f"{name}_{i}{ext}")
            shutil.move(pdf_path, dest_path)
            print(f"→ Moved single-page PDF to: {dest_path} (1 page)")

        # If more than 1 page -> move original to multi_originals_folder and split into pages
        elif num_pages > 1:
            # Move original
            orig_dest = os.path.join(multi_originals_folder, filename)
            if os.path.exists(orig_dest):
                name, ext = os.path.splitext(filename)
                i = 1
                while os.path.exists(os.path.join(multi_originals_folder, f"{name}_{i}{ext}")):
                    i += 1
                orig_dest = os.path.join(multi_originals_folder, f"{name}_{i}{ext}")
            shutil.move(pdf_path, orig_dest)
            print(f"Moved multi-page original to: {orig_dest}")

            # Split pages into split_pages_folder (optionally grouped by basename)
            # You can either dump all split pages in the split_pages_folder, or create a subfolder per PDF.
            target_subfolder = os.path.join(split_pages_folder, base_name)
            os.makedirs(target_subfolder, exist_ok=True)

            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                output_filename = f"{base_name}_page_{i+1:03d}.pdf"
                output_path = os.path.join(target_subfolder, output_filename)

                # avoid overwrite by incrementing suffix if exists
                if os.path.exists(output_path):
                    name, ext = os.path.splitext(output_filename)
                    j = 1
                    while os.path.exists(os.path.join(target_subfolder, f"{name}_{j}{ext}")):
                        j += 1
                    output_path = os.path.join(target_subfolder, f"{name}_{j}{ext}")

                with open(output_path, "wb") as f:
                    writer.write(f)

            print(f"Split complete for {filename}. ({num_pages} pages saved to {target_subfolder})")

        # Edge case: zero pages (shouldn't normally happen)
        else:
            print(f"Skipping {filename}: parsed 0 pages.")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("\nDone processing all PDFs.")
