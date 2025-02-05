import frappe
from frappe.utils import nowdate, getdate
from frappe import _
import time

def show_progress(docnames, message, i, description, hide_on_completion =True):
    n = len(docnames)
    frappe.publish_progress(float(i) * 100 / n, title=message, description=description)
    
def validate_customer(retries=3, delay=0.5):
    today = getdate(nowdate())  
    print("Today's date:", today)
    missing_fields = []
    customer_docs = frappe.get_list('Customer', fields=["name", "custom_even_valid4", "custom_even_valid", "custom_even_valid2", "custom_even_valid3"])
    num = len(customer_docs)

    for i, doc in enumerate(customer_docs):
        retry_count = 0
        success = False

        while retry_count < retries and not success:
            try:

                customer_doc = frappe.get_doc('Customer', doc['name'])
                fields = [
                    {"field": customer_doc.custom_even_valid4, "name": "custom_even_valid4"},
                    {"field": customer_doc.custom_even_valid, "name": "custom_even_valid"},
                    {"field": customer_doc.custom_even_valid2, "name": "custom_even_valid2"},
                    {"field": customer_doc.custom_even_valid3, "name": "custom_even_valid3"}
                ]

                validation = []

                for event in fields:
                    if not event['field']:
                        missing_fields.append({"field": event['name']})
                        reasons = frappe.get_all(
                            'Reason of Susbending',
                            filters={
                                'custom_field': event['name'],
                                'custom_exist': 1,
                                'is_alllowed': 1
                            },
                            fields=["name", "custom_field"]
                        )

                        for row in reasons:
                            validation.append({
                                'field': row.custom_field,
                                'reason': row.name
                            })

                    if event['field']:
                        event_date = getdate(event['field']) 
                        if event_date < today:
                            existing_fields = [{"field": event['name']}]
                            reasons = frappe.get_all(
                                'Reason of Susbending',
                                filters={
                                    'custom_field': event['name'],
                                    'is_alllowed': 1,
                                    'custom_exist': 0
                                },
                                fields=["name", "custom_field"]
                            )

                            for row in reasons:
                                validation.append({
                                    'field': row.custom_field,
                                    'reason': row.name
                                })
                customer_doc.set('custom_customer_validation', [])    
                for item in validation:
                    customer_doc.append('custom_customer_validation', {
                        'field': item['field'],
                        'reason': item['reason']
                    })

                if validation:
                    frappe.db.set_value("Customer", customer_doc.name, "custom_customer_status", "Suspended")
                    customer_doc.reload()
                    customer_doc.save()  # Save the customer document
                    frappe.db.commit()    # Commit changes to the database
                show_progress(customer_docs, _("Validating Customers"), i + 1, _("Processed {0}").format(doc['name']))

                success =   True 
                    # return customer_doc.custom_customer_validation
                
            except Exception as e:
                frappe.msgprint(_('Error while processing {0}: {1}').format(doc['name'], str(e)))
                retry_count += 1
                time.sleep(delay)
                
    show_progress(customer_docs, _("Validation Complete!"), num, _("All customers processed"))
    print({"missing_fields": missing_fields}) 
    