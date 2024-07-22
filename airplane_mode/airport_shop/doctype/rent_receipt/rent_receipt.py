# Copyright (c) 2024, Abdullah Salih and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentReceipt(Document):
	def before_save(doc):
		shop = frappe.get_doc("Airport Shop",doc.shop)
		doc.amount_remaining = float(shop.rent_amount) - float(doc.amount_paid)

