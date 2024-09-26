# import frappe
# from frappe.utils import nowdate, getdate
# from datetime import datetime
# from frappe import _
# import time
# from frappe.desk.doctype.bulk_update.bulk_update import show_progress
# @frappe.whitelist()
# def validate_customer(retries=3, delay=0.5):

#     today = getdate(nowdate())  # Get today's date as a date object
#     missing_fields = []
#     counter = 0
#     customer_docs = frappe.get_list('Customer',fields=["name","custom_even_valid4","custom_even_valid","custom_even_valid2","custom_even_valid3"])
#     num =len(customer_docs)
#     total = num * 2
#     # customer_names = [doc['name'] for doc in customer_docs]
#     frappe.show_progress(title=_("Validating Customers..."), count=0, total=total)
#     for doc in customer_docs:
#         retry_count = 0
#         success = False
#         while retry_count < retries and not success:
#             try:
#                 customer_doc = frappe.get_doc('Customer',doc['name'] )
#                 counter += 2
#                 print(counter)
#                 frappe.show_progress(title=_("Validating Customers..."), count=counter, total=total)
                
#                 success = True
                
#                 # customer_doc.set('custom_customer_validation', [])
#                 # return customer_doc.custom_even_valid4
#                 # fields = [
#                 #     {"field": customer_doc.custom_even_valid4, "name": "custom_even_valid4"},
#                 #     {"field": customer_doc.custom_even_valid, "name": "custom_even_valid"},
#                 #     {"field": customer_doc.custom_even_valid2, "name": "custom_even_valid2"},
#                 #     {"field": customer_doc.custom_even_valid3, "name": "custom_even_valid3"}
#                 # ]
            
#                 # custom_customer_validation = []

#                 # for event in fields:
#                 #     if not event['field']:
#                 # #         # event['field'] and isinstance(event['field'], str) and event_date < today
#                 #         missing_fields.append({"field": event['name']})
#                 #         # return missing_fields
#                 #         reasons = frappe.get_all(
#                 #             'Reason of Susbending',
#                 #             filters={
#                 #                 'custom_field': event['name'],
#                 #                 'custom_exist': 1,
#                 #                 'is_alllowed': 1
#                 #             },
#                 #             fields=["name", "custom_field"]
#                 #         )

#                 #         for row in reasons:
#                 #             # return row
#                 #             custom_customer_validation.append({
#                 #                 'field': row.custom_field,
#                 #                 'reason': row.name
#                 #             })
                        
#                 #     if event['field']:
#                 #         existing_fields = []
#                 #         event_date = getdate(event['field']) 
#                 #         if event_date < today:
#                 #             # return event_date < today
#                 #             existing_fields.append({"field": event['name']})
#                 #             reasons = frappe.get_all(
#                 #                 'Reason of Susbending',
#                 #                 filters={
#                 #                     'custom_field': event['name'],
#                 #                     'is_alllowed': 1,
#                 #                     'custom_exist': 0
#                 #                 },
#                 #                 fields=["name", "custom_field"]
#                 #             )

#                 #             for row in reasons:
#                 #                 custom_customer_validation.append({
#                 #                     'field': row.custom_field,
#                 #                     'reason': row.name
#                 #                 })
#                 # customer_doc.set('custom_customer_validation', custom_customer_validation)
#                 # customer_doc.save()
#                 # frappe.db.commit()
#             except:
#                     frappe.msgprint('there are Error')
#                     retry_count += 1
#                     time.sleep(delay) 
#         if not success:
#             print("Failed after retries, skipping this transaction.")            
        
#     # print({"missing_fields": missing_fields,"existing_fields":existing_fields, "custom_customer_validation": custom_customer_validation})
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

                customer_doc = frappe.get_doc('Customer', doc.name)

                fields = [
                    {"field": customer_doc.custom_even_valid4, "name": "custom_even_valid4"},
                    {"field": customer_doc.custom_even_valid, "name": "custom_even_valid"},
                    {"field": customer_doc.custom_even_valid2, "name": "custom_even_valid2"},
                    {"field": customer_doc.custom_even_valid3, "name": "custom_even_valid3"}
                ]

                custom_customer_validation = []

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
                            custom_customer_validation.append({
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
                                custom_customer_validation.append({
                                    'field': row.custom_field,
                                    'reason': row.name
                                })
                print(customer_doc)
                customer_doc.set('custom_customer_validation', custom_customer_validation)
                customer_doc.save()
                frappe.db.commit()

                show_progress(customer_docs, _("Validating Customers"), i + 1, _("Processed {0}").format(doc['name']))

                success = True 

            except Exception as e:
                frappe.msgprint(_('Error while processing {0}: {1}').format(doc['name'], str(e)))
                retry_count += 1
                time.sleep(delay)
                
    show_progress(customer_docs, _("Validation Complete!"), num, _("All customers processed"))
    print({"missing_fields": missing_fields}) 
    