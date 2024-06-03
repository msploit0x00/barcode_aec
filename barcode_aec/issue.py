import frappe
from frappe import _
from frappe.utils.pdf import get_pdf

@frappe.whitelist(allow_guest=True)
def send_email(name):
    try:
        issue = frappe.get_doc("Issue", name)
        custom_the_contact = issue.custom_the_contact
        attachments = get_attachments(issue)
        content = frappe.render_template(issue.custom_body_mail, {"doc": issue.as_dict()})
        args = issue.as_dict()
        args["message"] = content
        # Default print format if not specified in the issue
        print_format = getattr(issue, 'print_format', 'issue letter')
        
        for contact in custom_the_contact:
            email = contact.get('email')
              
            # Attach print format if needed
            print_format_attachment = attach_print("Issue", name, print_format)
            if print_format_attachment:
                attachments.append(print_format_attachment)

            email_args = {
                "subject": issue.subject,
                "sender": issue.custom_email,
                "recipients": [email],
                "attachments": attachments,
                "template": "newsletter",
                "reference_doctype": issue.doctype,
                "reference_name": name,
                "queue_separately": True,
                "send_priority": 0,
                "delayed": True,
                "args": args
            }
            frappe.sendmail(**email_args)
        else:
            frappe.log_error(f"No email found for contact in Issue {name}", _("Missing email"))

        frappe.msgprint(_("Email(s) sent successfully"))
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error in send_email"))
        frappe.throw(_("An error occurred while sending emails: {0}").format(str(e)))


def get_attachments(doc):
    attachments = []
    for attachment in doc.get("custom_attachments", []):
        file_url = attachment.get("attachment")
        if file_url:
            attachments.append({"file_url": file_url})
    return attachments

def attach_print(doctype, name, print_format=None, style=None, as_pdf=True, no_letterhead=0):
    """
    Generate a print format for a document and return the file name and content.
    
    :param doctype: The doctype of the document
    :param name: The name of the document
    :param print_format: The print format to use
    :param style: The style to apply to the print format
    :param as_pdf: Boolean indicating whether to return the content as PDF
    :param no_letterhead: Boolean indicating whether to exclude the letterhead
    :return: Dictionary containing 'fname' and 'fcontent'
    """
    try:
        if as_pdf:
            content = get_pdf(frappe.get_print(doctype, name, print_format, style=style, no_letterhead=no_letterhead))
            file_name = "{0}.pdf".format(frappe.scrub(name))
        else:
            content = frappe.get_print(doctype, name, print_format, style=style, no_letterhead=no_letterhead)
            file_name = "{0}.html".format(frappe.scrub(name))
        
        return {"fname": file_name, "fcontent": content}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error in attach_print"))
        frappe.throw(_("An error occurred while generating the print format: {0}").format(str(e)))
