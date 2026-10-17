import argparse
import os
import shutil

def run_pipeline(input_dir, output_dir):
    print(f"Running ETL from: '{input_dir}' -> Target: '{output_dir}'")
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory '{input_dir}' does not exist.")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Process files
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            src = os.path.join(input_dir, filename)
            dest = os.path.join(output_dir, f"processed_{filename}")
            shutil.copyfile(src, dest)
            print(f"Processed: {filename} -> {dest}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CLI Runner for Ingestion ETL")
    parser.add_argument("--input_dir", required=True, help="Path to input directory containing CSVs")
    parser.add_argument("--output_dir", required=True, help="Target directory for processed deliverables")
    args = parser.parse_args()
    
    run_pipeline(args.input_dir, args.output_dir)