import frappe
from frappe import _
import json
from frappe.utils.jinja import get_email_from_template

@frappe.whitelist()
def get_customer(name):
    try:
        customer = frappe.get_doc("Customer", name)
        return customer.as_dict()
    except frappe.DoesNotExistError:
        frappe.throw(_("Customer {0} not found").format(name))
    except Exception as e:
        frappe.log_error(_("Error updating field: {0}").format(e))
        frappe.throw(_("Error retrieving customer"))

@frappe.whitelist()
def add_contact(customer_id, first_name, designation, email, phone):
    contact = frappe.new_doc("Contact")
    contact.first_name = first_name
    contact.designation = designation
    contact.append("email_ids", {"email_id": email, "is_primary": 1})
    if phone != "":
        contact.append("phone_nos", {"phone": phone, "is_primary_phone": 1})
    contact.append("links", {"link_doctype": "Customer", "link_name": customer_id})
    contact.insert()
    frappe.db.commit()
    return contact

@frappe.whitelist()
def delete_contact(doc_name):
    try: 
        frappe.delete_doc("Contact", doc_name)
        frappe.db.commit()
        return {'status': 'success', 'message': 'Contact deleted successfully'}
    except frappe.DoesNotExistError:
        frappe.throw(_("Contact {0} not found").format(doc_name))

@frappe.whitelist()
def edit_contact(doc_name, first_name, last_name, designation, email, phone):
    try: 
        contact = frappe.get_doc("Contact", doc_name)
        contact.first_name = first_name
        contact.last_name = last_name
        contact.designation = designation
        
        # Update email in the child table 'Email'
        if email:
            email_record = contact.append('email_ids', {})
            email_record.email_id = email
            
        # Update phone in the child table 'Phone'
        if phone:
            phone_record = contact.append('phone_nos', {})
            phone_record.phone = phone

        contact.save()
        frappe.db.commit()
        return {'status': 'success', 'message': 'Contact deleted successfully'}
    except frappe.DoesNotExistError:
        frappe.throw(_("Contact {0} not found").format(doc_name))

@frappe.whitelist()
def get_contacts_for_customer(customer_name):
    all_contacts = frappe.get_all(
        "Contact",
        fields=["name", "first_name", "last_name", "email_id", "phone", "designation"]
    )

    filtered_contacts = []
    for contact in all_contacts:
        if is_linked_to_customer(contact, customer_name):
            filtered_contacts.append(contact)

    return filtered_contacts

def is_linked_to_customer(contact, customer_name):
    links = frappe.get_all(
        "Dynamic Link",
        filters={"parent": contact.get("name"), "link_doctype": "Customer", "link_name": customer_name}
    )
    return len(links) > 0

@frappe.whitelist()
def get_total_clusters(clusters):
    if not isinstance(clusters, list):
        clusters = json.loads(clusters)

    total_clusters = set()
    for cluster in clusters:
        doc = frappe.get_doc("Blocs of Targeted Countries", cluster)
        child_table_data = doc.get('blocs_of_targeted_countries')
        
        for row in child_table_data:
            total_clusters.add(row.country)
    
    return list(total_clusters)

@frappe.whitelist()
def get_product_details(product):
    doc = frappe.get_doc("Product", product)
    return doc

@frappe.whitelist()
def sendmail(
	recipients=None,
	sender="",
	subject="",
	message="",
	as_markdown=False,
	delayed=False,
	reference_doctype=None,
	reference_name=None,
	unsubscribe_method=None,
	unsubscribe_params=None,
	unsubscribe_message=None,
	add_unsubscribe_link=1,
	attachments=None,
	content=None,
	doctype=None,
	name=None,
	reply_to=None,
	queue_separately=False,
	cc=None,
	bcc=None,
	message_id=None,
	in_reply_to=None,
	send_after=None,
	expose_recipients=None,
	send_priority=1,
	communication=None,
	retry=1,
	now=None,
	read_receipt=None,
	is_notification=False,
	inline_images=None,
	template=None,
	args=None,
	header=None,
	print_letterhead=False,
	with_container=False,
):
	"""Send email using user's default **Email Account** or global default **Email Account**.


	:param recipients: List of recipients.
	:param sender: Email sender. Default is current user or default outgoing account.
	:param subject: Email Subject.
	:param message: (or `content`) Email Content.
	:param as_markdown: Convert content markdown to HTML.
	:param delayed: Send via scheduled email sender **Email Queue**. Don't send immediately. Default is true
	:param send_priority: Priority for Email Queue, default 1.
	:param reference_doctype: (or `doctype`) Append as communication to this DocType.
	:param reference_name: (or `name`) Append as communication to this document name.
	:param unsubscribe_method: Unsubscribe url with options email, doctype, name. e.g. `/api/method/unsubscribe`
	:param unsubscribe_params: Unsubscribe paramaters to be loaded on the unsubscribe_method [optional] (dict).
	:param attachments: List of attachments.
	:param reply_to: Reply-To Email Address.
	:param message_id: Used for threading. If a reply is received to this email, Message-Id is sent back as In-Reply-To in received email.
	:param in_reply_to: Used to send the Message-Id of a received email back as In-Reply-To.
	:param send_after: Send after the given datetime.
	:param expose_recipients: Display all recipients in the footer message - "This email was sent to"
	:param communication: Communication link to be set in Email Queue record
	:param inline_images: List of inline images as {"filename", "filecontent"}. All src properties will be replaced with random Content-Id
	:param template: Name of html template from templates/emails folder
	:param args: Arguments for rendering the template
	:param header: Append header in email
	:param with_container: Wraps email inside a styled container
	"""

	if recipients is None:
		recipients = []
	if cc is None:
		cc = []
	if bcc is None:
		bcc = []

	text_content = None
	if template:
		message, text_content = get_email_from_template(template, args)

	message = content or message

	if as_markdown:
		from frappe.utils import md_to_html

		message = md_to_html(message)

	if not delayed:
		now = True

	from frappe.email.doctype.email_queue.email_queue import QueueBuilder
     
	if sender:
		actual_sender = sender
	else:
		actual_sender = frappe.session.user

	builder = QueueBuilder(
		recipients=recipients,
		sender=actual_sender,
		subject=subject,
		message=message,
		text_content=text_content,
		reference_doctype=doctype or reference_doctype,
		reference_name=name or reference_name,
		add_unsubscribe_link=add_unsubscribe_link,
		unsubscribe_method=unsubscribe_method,
		unsubscribe_params=unsubscribe_params,
		unsubscribe_message=unsubscribe_message,
		attachments=attachments,
		reply_to=reply_to,
		cc=cc,
		bcc=bcc,
		message_id=message_id,
		in_reply_to=in_reply_to,
		send_after=send_after,
		expose_recipients=expose_recipients,
		send_priority=send_priority,
		queue_separately=queue_separately,
		communication=communication,
		read_receipt=read_receipt,
		is_notification=is_notification,
		inline_images=inline_images,
		header=header,
		print_letterhead=print_letterhead,
		with_container=with_container,
	)

	# build email queue and send the email if send_now is True.
	try:
		builder.process(send_now=now)
		return {'message' : 'sent success'}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), _("Failed to send email"))
		return {}
# GET email    
@frappe.whitelist()
def get_Email_account():
    all_emails = frappe.get_all(
        "Email Account",
        fields=["email_id"]
    )
    return all_emails  # Directly return the list of email dictionaries

