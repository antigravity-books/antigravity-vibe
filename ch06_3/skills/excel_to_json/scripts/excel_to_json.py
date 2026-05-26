import argparse
import json
import os
import sys
import openpyxl

def main():
    parser = argparse.ArgumentParser(description="Convert an Excel file to JSON.")
    parser.add_argument("input_file", help="Path to the input Excel file (.xlsx)")
    parser.add_argument("-o", "--output", help="Path to the output JSON file. Defaults to input file name with .json extension.")
    
    args = parser.parse_args()
    
    input_file = args.input_file
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)
        
    output_file = args.output
    if not output_file:
        base_name, _ = os.path.splitext(input_file)
        output_file = f"{base_name}.json"
        
    try:
        # Load the workbook and get the active sheet
        wb = openpyxl.load_workbook(input_file, data_only=True)
        sheet = wb.active
        
        data = []
        headers = []
        
        # Read headers from the first row
        for cell in sheet[1]:
            headers.append(cell.value)
            
        # Read data from the second row onwards
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if any(row):  # skip completely empty rows
                item = dict(zip(headers, row))
                data.append(item)
                
        # Save as JSON with UTF-8 encoding
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully converted '{input_file}' to JSON.")
        print(f"Saved at: '{output_file}'")
        
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
