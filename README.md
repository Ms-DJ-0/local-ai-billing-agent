# Rent Bill Billing Assistant

A Python-based AI assistant that automatically extracts and analyzes rent bills from PDF files, checks payment status, and provides payment recommendations.

---

## **What It Does**

1. **Scans PDF Bills** - Extracts text and data from rent bill PDFs
2. **Detects Payment Status** - Determines if the bill is paid or unpaid
3. **Calculates Due Date** - Shows how many days until payment is due (or if overdue)
4. **AI Analysis** - Uses local AI (Ollama) to provide billing insights and recommendations

---

## **How It Works - Step by Step**

### **Step 1: User Inputs Bill Path**
User provides the path to their rent bill PDF file
```
Enter the path to your rent bill PDF: C:\Downloads\bill.pdf
```

### **Step 2: PDF Scanning**
- Opens the PDF file using PyPDF2
- Extracts all text from every page
- Parses text to find key-value pairs (e.g., "Amount: 5000")

### **Step 3: Data Extraction**
- Identifies bill details: Amount, Due Date, Status, etc.
- Stores data in dictionary format
- Displays extracted information to user

### **Step 4: Payment Status Check**
- Searches for payment status fields (Status, Payment Status, Paid Date, etc.)
- Returns: **"Paid"** or **"Unpaid"**

### **Step 5: Due Date Calculation**
- Finds due date field from multiple possible names (Due, Due Date, Payment Due, etc.)
- Parses multiple date formats (YYYY-MM-DD, MM/DD/YYYY, etc.)
- Calculates days remaining: `due_date - today's_date`
- Returns: "Due in X days" or "Overdue by X days"

### **Step 6: AI Analysis**
- Sends bill details + status + due date to local AI (Ollama)
- AI generates summary and recommendations
- Displays results to user

---

## **Tech Stack**

| Component | Purpose |
|-----------|---------|
| **PyPDF2** | Extract text from PDF files |
| **Ollama (neural-chat)** | Free local AI analysis |
| **LangChain** | Connect AI models to Python |
| **Python 3.x** | Core programming language |

---

## **Setup Instructions**

### **1. Install Ollama Model**
```powershell
ollama pull orca-mini
```

### **2. Install Python Dependencies**
```powershell
pip install -r requirements.txt
```

### **3. Start Ollama Server**
```powershell
ollama serve
```

### **4. Run the Assistant** (in new terminal)
```powershell
python main.py
```

---

## **File Structure**

```
Code/
├── main.py              # Main billing assistant logic
├── tools.py             # Helper functions (PDF scan, status check, due date calc)
├── requirements.txt     # Python dependencies
├── .env                 # API keys (never commit!)
├── .gitignore          # Files to ignore in Git
└── README.md           # This file
```

---

## **Key Functions**

### **`scan_rent_bill(file_path)`**
Extracts all text from PDF and returns key-value pairs

### **`check_bill_paid(bill_details)`**
Searches for payment status across multiple field names

### **`check_due_date(bill_details)`**
Finds due date, parses multiple formats, calculates days remaining

### **`billing_assistant()`**
Main function that orchestrates all steps and displays results

---

## **Supported Date Formats**

- `2026-05-31` (YYYY-MM-DD)
- `05/31/2026` (MM/DD/YYYY)
- `31/05/2026` (DD/MM/YYYY)
- `May 31, 2026` (Full date)
- `05-31-2026` (MM-DD-YYYY)

---

## **Features**

Extracts bills from PDF files  
Detects payment status (Paid/Unpaid)  
Calculates days until due or overdue  
Provides AI-powered recommendations  
Works offline (uses local Ollama AI)  
No API costs (completely free)  
Handles multiple PDF formats  

---

## **Example Output**

```
Processing file: C:\Downloads\bill.pdf
PDF loaded successfully. Pages: 1
Text extracted: 2543 characters
Extracted 12 fields from PDF

--- Bill Details Extracted ---
  Amount: 5000.00
  Due Date: 2026-05-31
  Status: Unpaid

Payment Status: Unpaid
Due Date Status: The rent is due in 10 days.

Analyzing bill with Ollama (Local AI)...

--- Ollama Billing Analysis ---
Your rent bill of 5000.00 is currently unpaid and due in 10 days.
Recommendation: Pay as soon as possible to avoid late fees.
```

---

## **Troubleshooting**

| Issue | Solution |
|-------|----------|
| "File not found" | Check PDF path is correct |
| "No text found in PDF" | PDF might be scanned as image |
| "Due date not found" | PDF column name might be different |
| "Ollama is not running" | Start server: `ollama serve` |
| "Model not found" | Download model: `ollama pull orca-mini` |

---

## **License**

Open source - Free to use and modify

---

**Created:** May 21, 2026  
**Status:** Active Development
