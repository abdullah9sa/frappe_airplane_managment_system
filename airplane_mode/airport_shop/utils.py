import frappe
from frappe.utils import now
from frappe.core.doctype.communication.email import make

def create_monthly_rent_payments():
    # Log the start of the job
    frappe.logger().info(f"Monthly rent payment job started at {now()}")

    # Fetch all active shops
    shops = frappe.get_all('Airport Shop', filters={'is_rented': 1}, fields=['name', 'rent_amount', 'shop_owner'])

    # Create a Rent Payment document for each shop and send email reminder
    for shop in shops:
        create_rent_payment(shop['name'], shop['rent_amount'])
        settings = frappe.get_single("Shops Settings")
        
        if (settings.enable_rent_reminders == 1):
            send_rent_reminder(shop['shop_owner'], shop['rent_amount'])

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

def send_rent_reminder(shop_owner, rent_amount):
    try:
        # Fetch the email of the shop owner
        owner = frappe.get_doc('Shop Owner', shop_owner)
        if owner.email:
            # Compose the email
            subject = "Monthly Rent Due"
            message = f"Dear {owner.first_name},<br><br>Your monthly rent of {rent_amount} is due. Please make the payment at your earliest convenience.<br><br>Thank you."
            
            # Send the email
            make(
                recipients=owner.email,
                sender=frappe.session.user,
                subject=subject,
                content=message,
                doctype="Shop Owner",
                name=shop_owner
            )
            frappe.logger().info(f"Rent reminder sent to {owner.email}")

    except Exception as e:
        # Log any errors that occur
        frappe.logger().error(f"Failed to send rent reminder to {shop_owner}: {str(e)}")
