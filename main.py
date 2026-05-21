from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from tools import scan_rent_bill, check_bill_paid, check_due_date
import os


load_dotenv()

class BillingResponse(BaseModel):
    bill_amount: str
    status: str
    due_date_info: str
    recommendation: str

def billing_assistant():
    """
    Billing Assistant: Upload a bill, extract details, and use OpenAI to provide analysis.
    """
    # Get file path from user
    file_path = input("Enter the path to your rent bill PDF: ").strip().strip('"').strip("'")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return
    
    print(f"\nProcessing file: {file_path}")
    
    # Scan the bill
    bill_details = scan_rent_bill(file_path)

    if not bill_details:
        print("No bill details found. The PDF might be empty or in an unsupported format.")
        return

    print("\n--- Bill Details Extracted ---")
    for key, value in bill_details.items():
        print(f"  {key}: {value}")

    # Check payment status and due date
    payment_status = "Paid" if check_bill_paid(bill_details) else "Unpaid"
    due_date_info = check_due_date(bill_details)

    print(f"\nPayment Status: {payment_status}")
    print(f"Due Date Status: {due_date_info}")

    # Create a prompt for the AI to analyze the billing information
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an intelligent billing assistant. Analyze the provided bill details and give the user helpful advice about their rent payment.
                Provide:
                1. A summary of the bill
                2. Payment status analysis
                3. Recommendations based on the due date
                Keep your response concise and actionable.""",
            ),
            (
                "human",
                """Please analyze this rent bill:
                Bill Details: {bill_details}
                Payment Status: {payment_status}
                Due Date Info: {due_date_info}
                
                Provide a detailed summary and recommendations for the user.""",
            ),
        ]
    )

    # Initialize Ollama model (Free, runs locally)
    print("\nAnalyzing bill with Ollama (Local AI)...")
    try:
        llm = OllamaLLM(model="orca-mini")
        chain = prompt | llm
        response = chain.invoke({
            "bill_details": str(bill_details),
            "payment_status": payment_status,
            "due_date_info": due_date_info
        })

        print("\n--- Ollama Billing Analysis ---")
        print(response)
    except Exception as e:
        if "connection" in str(e).lower() or "refused" in str(e).lower():
            print("Error: Ollama is not running.")
            print("Please start Ollama by running: ollama serve")
            print("\n--- Bill Summary (Without AI Analysis) ---")
            print(f"Payment Status: {payment_status}")
            print(f"Due Date Status: {due_date_info}")
            print(f"Total Fields Extracted: {len(bill_details)}")
        else:
            print(f"Error invoking Ollama: {e}")
            print("Make sure Ollama is installed and running: ollama serve")

if __name__ == "__main__":
    billing_assistant()