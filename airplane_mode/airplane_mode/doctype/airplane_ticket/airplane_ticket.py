import frappe
from frappe.model.document import Document
from frappe import _
import random
import string

class AirplaneTicket(Document):
	def validate(self):
		if self.add_ons:
			unique_items = set()
			duplicates = []
			for add_on in self.add_ons:
				if add_on.item in unique_items:
					duplicates.append(add_on)
				else:
					unique_items.add(add_on.item)

			# Remove duplicates from add_ons
			for duplicate in duplicates:
				self.remove(duplicate)

			# Calculate total amount
			total_amount = sum([i.amount for i in self.add_ons])
			self.total_amount = self.flight_price + total_amount if self.flight_price else total_amount

	def before_save(self):

		if not len(self.add_ons) > 0:
			self.total_amount = self.flight_price

		if self.add_ons:
			total_amount = 0
			for i in self.add_ons:
				total_amount += i.amount
				if self.flight_price:
					self.total_amount = self.flight_price + total_amount
				else:
					self.total_amount = total_amount

	
	def before_insert(self):
		if not self.seat:
			random_integer = random.randint(1, 99)
			random_letter = random.choice(string.ascii_uppercase[:5])
			seat_number = f"{random_integer}{random_letter}"
			self.seat = seat_number
   

		# Get the flight document
		flight = frappe.get_doc("Airplane Flight", self.flight)

		# Get the airplane document
		airplane = frappe.get_doc("Airplane", flight.airplane)

		# Count all tickets with the same flight
		ticket_count = frappe.db.count("Airplane Ticket", filters={"flight": self.flight})

		# Throw an error if the airplane capacity cannot hold the new ticket
		if ticket_count >= airplane.capacity:
			frappe.throw(f"The airplane has reached its capacity of {airplane.capacity} passengers. Cannot issue a new ticket.")

	def on_submit(self):
		if self.doctype == "Airplane Ticket":
			airplane_flight = frappe.get_doc("Airplane Flight", self.flight)
			if airplane_flight:
				airplane_flight.status = "Completed"
				airplane_flight.save()
    

def before_submit(self,method):
	if self.status != "Boarded":
		frappe.throw(_('Airplane Ticket Status Must be "Boarded" in order to Submit this document'))

