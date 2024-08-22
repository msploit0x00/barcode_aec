# Copyright (c) 2024, ds and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, today
from datetime import datetime

class GeneralizationQueuing(Document):
	@frappe.whitelist()
	def send_email(self):
		current_date = today()
		current_time = datetime.now().strftime('%H:%M:%S') 
		print("dddddddddddddddddddddddddd",current_date == str(self.date),current_time == self.time)	
		if current_date == str(self.date) and current_time == self.time:
			recipients = [customer.email for customer in self.customer_email]
			args = self.as_dict()
			args["message"] = self.get_message()
			email_args = {
				"subject":self.subject,
				"sender":self.sender_email,
				"recipients":recipients,
				"attachments":self.get_attachments,
				"template": "newsletter",
				"reference_doctype": self.doctype,
				"reference_name": self.name,
				"queue_separately": True,
				"send_priority": 0,

			}
			frappe.sendmail(**email_args)


		def get_attachments(self):
			return [{"file_url":row.attachment} for row in self.attachs]

		def get_message(self):
			content = frappe.render_template(self.body, {"doc": args})
			return content	