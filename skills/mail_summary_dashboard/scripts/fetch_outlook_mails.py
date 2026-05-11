import win32com.client
import datetime
import argparse
import json
import sys
import os

def get_emails_by_date(target_date_str, output_path):
    try:
        target_date = datetime.datetime.strptime(target_date_str, "%Y-%m-%d").date()
    except ValueError:
        error_msg = {"error": "Invalid date format. Use YYYY-MM-DD."}
        write_output(error_msg, output_path)
        sys.exit(1)

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        inbox = namespace.GetDefaultFolder(6) # 6 corresponds to Inbox
        items = inbox.Items
        items.Sort("[ReceivedTime]", True) 
    except Exception as e:
        error_msg = {"error": f"Failed to access Outlook: {str(e)}"}
        write_output(error_msg, output_path)
        sys.exit(1)

    results = []
    
    start_date_str = target_date.strftime("%m/%d/%Y 00:00 AM")
    end_date_str = (target_date + datetime.timedelta(days=1)).strftime("%m/%d/%Y 00:00 AM")
    
    restriction = f"[ReceivedTime] >= '{start_date_str}' AND [ReceivedTime] < '{end_date_str}'"
    
    try:
        filtered_items = items.Restrict(restriction)
    except Exception as e:
        error_msg = {"error": f"Failed to filter emails: {str(e)}"}
        write_output(error_msg, output_path)
        sys.exit(1)

    count = 1
    for item in filtered_items:
        if item.Class == 43: # olMail
            try:
                subject = item.Subject if item.Subject else "(제목 없음)"
                sender = item.SenderName if item.SenderName else "Unknown"
                received_time = item.ReceivedTime.strftime("%Y-%m-%d %H:%M:%S")
                body = item.Body.strip() if item.Body else ""
                
                mail_data = {
                    "id": count,
                    "subject": subject,
                    "sender": sender,
                    "received_time": received_time,
                    "body": body
                }
                results.append(mail_data)
                count += 1
            except Exception as e:
                continue

    output_data = {"date": target_date_str, "count": len(results), "emails": results}
    write_output(output_data, output_path)

def write_output(data, path):
    if path:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        print(json.dumps(data, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Outlook emails for a specific date")
    parser.add_argument("--date", required=True, help="Target date in YYYY-MM-DD format")
    parser.add_argument("--out", required=False, help="Output JSON file path", default="")
    args = parser.parse_args()
    get_emails_by_date(args.date, args.out)
