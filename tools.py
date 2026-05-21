from datetime import datetime
from PyPDF2 import PdfReader
import os



def scan_rent_bill(file_path="rent_bill.pdf"):
    """
    Scans for rent bill details from a PDF file.
    Returns a dictionary with bill details.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    try:
        reader = PdfReader(file_path)
        print(f"PDF loaded successfully. Pages: {len(reader.pages)}")
        
        text = ""
        for page_num, page in enumerate(reader.pages):
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        
        if not text.strip():
            print("No text found in PDF. The file might be scanned as an image or encrypted.")
            return None
        
        print(f"Text extracted: {len(text)} characters")
        
        bill_details = {}
        for line in text.split("\n"):
            line = line.strip()
            if ":" in line and len(line) > 3:
                parts = line.split(":", 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ""
                if key and value:
                    bill_details[key] = value
        
        if bill_details:
            print(f"Extracted {len(bill_details)} fields from PDF")
        else:
            print("No key-value pairs found. PDF structure might be different.")
        
        return bill_details if bill_details else None
    
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def check_bill_paid(bill_details):
    """
    Checks if the bill is marked as paid by looking at various possible status fields.
    """
    # List of possible field names that might indicate payment status
    status_fields = [
        "Status", "Payment Status", "Bill Status", "Payment", 
        "Paid", "Paid Status", "Payment_Status", "payment_status"
    ]
    
    # Check each possible field
    for field in status_fields:
        if field in bill_details:
            status_value = bill_details[field].lower()
            if "paid" in status_value or "complete" in status_value or "settled" in status_value:
                return True
            else:
                return False
    
    # If no status field found, check if there's a "Paid Date" field
    paid_date_fields = ["Paid Date", "Payment Date", "Date Paid", "paid_date", "payment_date"]
    for field in paid_date_fields:
        if field in bill_details and bill_details[field].strip():
            return True
    
    # Default to unpaid if no clear status found
    return False

def check_due_date(bill_details):
    """
    Checks how many days are left until the rent is due.
    Returns the number of days left or a message if overdue.
    Looks for multiple possible field names for due date.
    """
    # List of possible field names for due date in tables
    due_date_fields = [
        "Due Date", "Due", "Payment Due", "Payment Due Date",
        "Due Date:", "Due:", "Payment Due Date:",
        "due_date", "due", "payment_due", "payment_due_date",
        "Bill Due Date", "Amount Due Date", "Rent Due Date",
        "DueDate", "PaymentDue", "deadline"
    ]
    
    # Check each possible field name
    for field in due_date_fields:
        if field in bill_details:
            due_date_str = bill_details[field].strip()
            if due_date_str:
                try:
                    # Try multiple date formats
                    date_formats = [
                        "%Y-%m-%d",      # 2026-05-31
                        "%m/%d/%Y",      # 05/31/2026
                        "%d/%m/%Y",      # 31/05/2026
                        "%B %d, %Y",     # May 31, 2026
                        "%b %d, %Y",     # May 31, 2026
                        "%m-%d-%Y",      # 05-31-2026
                        "%d-%m-%Y"       # 31-05-2026
                    ]
                    
                    due_date = None
                    for fmt in date_formats:
                        try:
                            due_date = datetime.strptime(due_date_str, fmt)
                            break
                        except ValueError:
                            continue
                    
                    if due_date:
                        days_left = (due_date - datetime.now()).days
                        if days_left < 0:
                            return f"The rent is overdue by {-days_left} days."
                        elif days_left == 0:
                            return "The rent is due TODAY!"
                        return f"The rent is due in {days_left} days."
                except Exception as e:
                    continue
    
    return "Due date not found in bill."
