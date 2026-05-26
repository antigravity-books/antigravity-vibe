import sys
import json
import csv
import os

def main():
    if len(sys.argv) < 3:
        print("Usage: python json_to_csv.py <target_csv_file> <input_json_file>")
        sys.exit(1)
        
    csv_file = sys.argv[1]
    json_file = sys.argv[2]
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)
        
    if not isinstance(data, list):
        data = [data]
        
    if not data:
        print("No data to write.")
        sys.exit(0)
        
    # JSON 키값들을 헤더로 추출
    headers = list(data[0].keys())
    
    # 대상 파일 존재 여부 확인 (헤더 작성을 위해)
    file_exists = os.path.isfile(csv_file)
    
    try:
        # utf-8-sig 인코딩을 사용하여 엑셀 등에서 한글 깨짐 방지
        with open(csv_file, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            
            # 파일이 처음 생성되는 경우에만 헤더 작성
            if not file_exists:
                writer.writeheader()
                
            writer.writerows(data)
        print(f"Data successfully saved to {csv_file}")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
