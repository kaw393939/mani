import os
import pandas as pd

def convert_xlsx_to_csv():
    # Define input and output directories
    input_dir = 'data/raw'
    output_dir = 'data/processed'

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get all xlsx files in the input directory
    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' not found.")
        return

    files = [f for f in os.listdir(input_dir) if f.endswith('.xlsx') and not f.startswith('~$')]

    if not files:
        print(f"No .xlsx files found in '{input_dir}'.")
        return

    print(f"Found {len(files)} Excel files to process in '{input_dir}'.")

    for file in files:
        try:
            print(f"Processing: {file}")
            file_path = os.path.join(input_dir, file)
            
            # Create a folder name based on the filename (without extension) inside the output directory
            base_name = os.path.splitext(file)[0]
            target_folder = os.path.join(output_dir, base_name)
            
            # Create the directory if it doesn't exist
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
                print(f"  Created directory: {target_folder}")
            
            # Read all sheets from the Excel file
            xls = pd.read_excel(file_path, sheet_name=None)
            
            for sheet_name, df in xls.items():
                # Construct the CSV filename
                # Clean sheet name to be safe for filenames
                safe_sheet_name = "".join([c for c in sheet_name if c.isalnum() or c in (' ', '-', '_')]).strip()
                csv_filename = f"{safe_sheet_name}.csv"
                csv_path = os.path.join(target_folder, csv_filename)
                
                # Export to CSV
                df.to_csv(csv_path, index=False)
                print(f"  Exported sheet '{sheet_name}' to {csv_path}")
                
        except Exception as e:
            print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    convert_xlsx_to_csv()
