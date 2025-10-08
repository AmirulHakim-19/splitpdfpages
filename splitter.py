import os
from PyPDF2 import PdfReader, PdfWriter

# Input and output folders
input_folder = "data/pdf"
output_folder = "data/split_output"

# Make sure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all PDF files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]

        print(f"Processing: {filename}")

        try:
            reader = PdfReader(pdf_path)
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)

                # Output file name format
                output_filename = f"{base_name}_page_{i+1}.pdf"
                output_path = os.path.join(output_folder, output_filename)

                with open(output_path, "wb") as f:
                    writer.write(f)

            print(f"✅ Split complete for {filename}. ({len(reader.pages)} pages saved)")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

print("\n🎉 All PDFs processed successfully!")
