
import frappe
from frappe.model.document import Document
import string
import random

class RentPayment(Document):
    def before_insert(self):
        self.receipt_number = self.generate_unique_receipt_number()
        
    def generate_unique_receipt_number(self):        
        abbreviation = "RP"
        unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"{abbreviation}-{unique_id}"
    
    
@frappe.whitelist()
def process_payment(docname, payment_method, paid_amount):
    try:
        # Fetch the Rent Payment document
        rent_payment = frappe.get_doc("Rent Payment", docname)
        
        # Change the status, update the payment method, and paid amount
        rent_payment.payment_status = "Completed"
        rent_payment.payment_method = payment_method
        rent_payment.payment_amount = paid_amount
        
        # Submit the Rent Payment document
        rent_payment.submit()
        
        # Generate and submit the receipt
        create_and_submit_receipt(rent_payment)

        return True
    except Exception as e:
        frappe.log_error(f"Error processing payment: {str(e)}")
        return False

def create_and_submit_receipt(rent_payment):
	try:
		# Create the Rent Receipt document
		receipt = frappe.get_doc({
			"doctype": "Rent Receipt",
			"shop": rent_payment.shop,
			"payment": rent_payment.name,
			"receipt_date": frappe.utils.now(),
			"receipt_number": rent_payment.receipt_number,
			"amount_paid": rent_payment.paid_amount,
			"payment_method": rent_payment.payment_method,
			"issued_by": frappe.session.user
		})
		# Insert and submit the receipt
		receipt.insert()
		receipt.submit()
	except Exception as e:
		frappe.log_error(f"Error creating receipt: {str(e)}")
		raise e