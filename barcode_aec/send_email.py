import frappe
from frappe import _

@frappe.whitelist()
def send_email(name, body):
    print("Sending email...")

    # Fetch the document based on 'name'
    doc = frappe.get_doc('Generalization Queuing', name)
    
    recipients = [customer.email for customer in doc.customer_email]
    args = doc.as_dict()
    args["message"] = get_message(doc, body)
    
    email_args = {
        "subject": doc.subject,
        "sender": doc.sender_email,
        "recipients": recipients,
        "attachments": get_attachments(doc),
        "template": "newsletter",
        "reference_doctype": doc.doctype,
        "reference_name": doc.name,
        "queue_separately": True,
        "send_priority": 0,
        "args": args
    }
    
    frappe.sendmail(**email_args)
    frappe.msgprint(_("Your ..................................................Email sent successfully"))

def get_message(doc, body):
    content = frappe.render_template(body, {"doc": doc.as_dict()})
    return content

def get_attachments(doc):
    return [{"file_url": row.attachment} for row in doc.attachs]
