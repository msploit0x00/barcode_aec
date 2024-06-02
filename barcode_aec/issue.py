# Copyright (c) 2024, ds and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime


@frappe.whitelist(allow_guest=True)
def send_email(name):
    doc = frappe.get_doc("Issue", name)
    custom_the_contact = doc.custom_the_contact
    
    for email in custom_the_contact:
        args = doc.as_dict()
        args["message"] = custom_body_mail(doc)
        email_args = {
            "subject": doc.subject,
            "attachments": get_attachments(doc),
            "sender": doc.custom_email,
            "recipients": email.email,
            "reference_doctype": doc.doctype,
            "reference_name": name,
            "queue_separately": True,
            "send_priority": 0,
            "args": args
        }
        frappe.sendmail(**email_args)
    frappe.msgprint(_("Email sent successfully"))

def custom_body_mail(doc):
    content = frappe.render_template(doc.custom_body_mail, {"doc": doc.as_dict()})
    return content

def get_attachments(doc):
    return [{"file_url": row.attachment} for row in doc.custom_attachments]

def subject(doc):
    return doc.subject

