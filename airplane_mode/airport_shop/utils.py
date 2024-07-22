# your_app_name/module_name.py

import frappe
from frappe.utils import now

def create_monthly_rent_payments():
    # Log the start of the job
    frappe.logger().info(f"Monthly rent payment job started at {now()}")

    # Fetch all active shops
    shops = frappe.get_all('Airport Shop', filters={'is_rented': 1}, fields=['name', 'rent_amount'])

    # Create a Rent Payment document for each shop
    for shop in shops:
        create_rent_payment(shop['name'], shop['rent_amount'])

    # Log the completion of the job
    frappe.logger().info(f"Monthly rent payment job completed at {now()}")

def create_rent_payment(shop_name, rent_amount):
    try:
        # Create the Rent Payment document
        rent_payment = frappe.get_doc({
            "doctype": "Rent Payment",
            "shop": shop_name,
            "payment_date": now(),
            "payment_amount": rent_amount,
            "payment_status": "Pending"
        })
        # Insert the document into the database
        rent_payment.insert()
        frappe.db.commit()
        
        # Log the successful creation of the document
        frappe.logger().info(f"Rent Payment created for {shop_name} with amount {rent_amount}")

    except Exception as e:
        # Log any errors that occur
        frappe.logger().error(f"Failed to create Rent Payment for {shop_name}: {str(e)}")
