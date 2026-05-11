import sys
import json
import win32com.client as win32
import os

def send_outlook_mail(data):
    try:
        # Outlook Application Object
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)

        # Parse data
        mail.To = data.get('to', '')
        mail.CC = data.get('cc', '')
        mail.Subject = data.get('subject', '')
        mail.Body = data.get('body', '')

        # Add attachments if any
        attachments = data.get('attachments', [])
        for attachment in attachments:
            if os.path.exists(attachment):
                mail.Attachments.Add(attachment)
            else:
                print(f"Warning: Attachment not found: {attachment}")

        # Send mail
        mail.Send()
        print(json.dumps({"status": "success", "message": "Email sent successfully."}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    json_input = ""
    # Standard input or argument
    if len(sys.argv) > 1:
        json_input = sys.argv[1]
    else:
        json_input = sys.stdin.read()
    
    try:
        data = json.loads(json_input)
        send_outlook_mail(data)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "message": f"Invalid JSON input: {str(e)}"}))
