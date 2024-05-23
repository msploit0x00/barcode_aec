# Copyright (c) 2024, ds and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from datetime import datetime



class Meeting(Document):
        
		@frappe.whitelist()
		def send_email_internal(self):
			# recipients = [customer.email for customer in self.committe_member]
			for customer in self.committee_member:
				args = self.as_dict()
				args["message"] = self.get_message_internal()
				email_args = {
					"subject": self.subject,
					"sender": self.custom_email,
					"recipients": customer.email,
					# "attachments": self.get_attachments(),
					"template": "newsletter",
					"reference_doctype": self.doctype,
					"reference_name": self.name,
					"queue_separately": True,
					"send_priority": 0,
					"args": args
				}
				frappe.sendmail(**email_args)
			frappe.msgprint(_("Email sent successfully"))




		@frappe.whitelist()
		def send_email_to_deputy(self):
			# recipients = [customer.email for customer in self.committe_member]
			if not self.custom_deputy_mail:
				frappe.throw("Please add Deputy Mail")
			else:
				args = self.as_dict()
				args["message"] = self.get_message_deputy()
				email_args = {
					"subject": self.subject,
					"sender": self.custom_email,
					"recipients": self.custom_deputy_mail,
					# "attachments": self.get_attachments(),
					"template": "newsletter",
					"reference_doctype": self.doctype,
					"reference_name": self.name,
					"queue_separately": True,
					"send_priority": 0,
					"args": args
				}
				frappe.sendmail(**email_args)
				frappe.msgprint(_("Email sent successfully"))


		@frappe.whitelist()
		def send_email_to_president(self):
			# recipients = [customer.email for customer in self.committe_member]
			if not self.custom_president_mail:
				frappe.throw("Please add President Mail")
			else:
				args = self.as_dict()
				args["message"] = self.get_message_president()
				email_args = {
					"subject": self.subject,
					"sender": self.custom_email,
					"recipients": self.custom_president_mail,
					# "attachments": self.get_attachments(),
					"template": "newsletter",
					"reference_doctype": self.doctype,
					"reference_name": self.name,
					"queue_separately": True,
					"send_priority": 0,
					"args": args
				}
				frappe.sendmail(**email_args)
				frappe.msgprint(_("Email sent successfully"))










		@frappe.whitelist()
		def send_email_council(self):
			# recipients = [customer.email for customer in self.committe_member]
			for customer in self.council_entities:
				args = self.as_dict()
				args["message"] = self.get_message_council()
				email_args = {
					"subject": self.subject,
					"sender": self.custom_email,
					"recipients": customer.email,
					# "attachments": self.get_attachments(),
					"template": "newsletter",
					"reference_doctype": self.doctype,
					"reference_name": self.name,
					"queue_separately": True,
					"send_priority": 0,
					"args": args
				}
				frappe.sendmail(**email_args)
			frappe.msgprint(_("Email sent successfully"))



		@frappe.whitelist()
		def send_email_external(self):
			# recipients = [customer.email for customer in self.committe_member]
			for customer in self.external_authority:
				args = self.as_dict()
				args["message"] = self.get_message_member()
				email_args = {
					"subject": self.subject,
					"sender": self.custom_email,
					"recipients": customer.email,
					# "attachments": self.get_attachments(),
					"template": "newsletter",
					"reference_doctype": self.doctype,
					"reference_name": self.name,
					"queue_separately": True,
					"send_priority": 0,
					"args": args
				}
				frappe.sendmail(**email_args)
			frappe.msgprint(_("Email sent successfully"))


		@frappe.whitelist()
		def external_entity_mail(self,body,email):
			# recipients = [customer.email for customer in self.committe_member]
			content = frappe.render_template(body, {"doc": self.as_dict()})
			args = self.as_dict()
			args["message"] = content
			email_args = {
					"subject": self.subject,
					"sender": self.custom_email,
					"recipients": email,
					# "attachments": self.get_attachments(),
					"template": "newsletter",
					"reference_doctype": self.doctype,
					"reference_name": self.name,
					"queue_separately": True,
					"send_priority": 0,
					"args": args
				}
			frappe.sendmail(**email_args)
			frappe.msgprint(_("Email sent successfully"))









		def get_message_internal(self):
			content = frappe.render_template(self.custom_invitation_template_for_internal_members, {"doc": self.as_dict()})
			return content

		def get_message_external(self):
			content = frappe.render_template(self.custom_invitation_template_for_external_members, {"doc": self.as_dict()})
			return content


		def get_message_deputy(self):
			content = frappe.render_template(self.custom_invitation_mail_template_for_deputy, {"doc": self.as_dict()})
			return content
		
		def get_message_president(self):
			content = frappe.render_template(self.custom_invitation_mail_template_for_president, {"doc": self.as_dict()})
			return content


		def get_message_council(self):
			content = frappe.render_template(self.custom_invitation_template_for_council_entities, {"doc": self.as_dict()})
			return content



		def get_attachments(self):
			return [{"file_url": row.attachment} for row in self.attachs]

