# Copyright (c) 2024, ds and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now, today
from datetime import datetime

def send_email():
    # current Date and time
    current_date = today()
    current_time_in_hour_min = datetime.now().strftime('%H:%M') 
    # get all generalization Queuing
    # print("current Date and time",current_date,current_time_in_hour_min)
    queue_time = frappe.get_single_value("Generalization Settings",)
    docs =frappe.get_all("Generalization Queuing")
    print("Generalization Queuing",docs)
    for doc in docs:
        generalization_queuing = frappe.get_doc("Generalization Queuing", doc.name)
        total_seconds = generalization_queuing.time.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        doc_time = f"{hours:02}:{minutes:02}"
        print("Generalization  doc_time ", doc_time)

        if current_date == str(generalization_queuing.date):
            if current_time_in_hour_min == doc_time:
                print("yes")
                recipients = [customer.email for customer in generalization_queuing.customer_email]
                args = generalization_queuing.as_dict()
                args["message"] = get_message(generalization_queuing,args)

                email_args = {
                    "subject":generalization_queuing.subject,
                    "sender":generalization_queuing.sender_email,
                    "recipients":recipients,
                    "attachments":get_attachments(generalization_queuing),
                    "template": "newsletter",
                    "reference_doctype": generalization_queuing.doctype,
                    "reference_name": generalization_queuing.name,
                    "queue_separately": True,
                    "send_priority": 0,

                }
                print("yes2")
                frappe.sendmail(**email_args)
                print("yes3")
                generalization_queuing.status = 'Sent'

                frappe.db.commit()



                        
        else:
            print("current Date and time not matched")    
 
def get_attachments(generalization_queuing):
    return [{"file_url":row.attachment} for row in generalization_queuing.attachs]

def get_message(generalization_queuing,args):
    content = frappe.render_template(generalization_queuing.body, {"doc": args})
    return content	                
