import frappe 
from datetime import datetime
from frappe import _
import time






@frappe.whitelist(allow_guest=True)
def process_data(retries=3, delay=0.5):
    all_customer = frappe.db.sql("""
        SELECT
            `name`,
            `customer_name` , 
            `tax_id`,
            `custom_volume_of__exports`,
            `customer_group`
        FROM
            `tabCustomer`
        """, as_dict=1)
    
    num = len(all_customer)
    counter = 0
    
    for emp in all_customer:
        print(emp.name)
        retry_count = 0
        success = False

        while retry_count < retries and not success:
            try:
                doc = frappe.get_doc("Customer", emp.name)
                counter += 1
                frappe.publish_progress(counter * 100 / num, title=_("Updating ..."))

                if doc.custom_board_of_directors_member_ == 'Yes':
                    doc.custom_board_of_directors_member_ = ''


                doc.save()
                frappe.db.commit()
                success = True  # If the transaction succeeds, set success to True to exit the retry loop
                print("Done")
            except frappe.QueryDeadlockError:  # Catch the deadlock error
                print("Deadlock encountered, retrying...")
                retry_count += 1
                time.sleep(delay)
                
        if not success:
            print("Failed after retries, skipping this transaction.")

@frappe.whitelist()
def functiongdidaa():
    # Enqueue the background function
    frappe.enqueue(method=process_data, queue='long')

    # Return a message indicating that the process has started
    return "Data processing started in the background."
