import frappe 
from datetime import datetime
from frappe import _
import time
from aec.aec.doctype.service_request.service_request import get_member_exportss
# Define your background function to process the data


@frappe.whitelist()
def exports_years(retries=3, delay=0.5):
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

        while int(retry_count) < int(retries) and not success:
            try:
                doc = frappe.get_doc("Customer", emp.name)
                counter += 1
                frappe.publish_progress(counter * 100 / num, title=_("Updating ..."))
                tax_id_1 = emp.tax_id
                tax_id_2 = emp.custom_tax_id_2
                tax_id_3 = emp.custom_tax_id_3

                # tax_ids = [tax_id_1,tax_id_2,tax_id_3]
                member_name = emp.customer_name
                total = 0.0

                if tax_id_1:
                    print("mina ::::")
                    get_last_exported_year = get_member_exportss(tax_id_1)
                    print(get_last_exported_year)
                    if len(get_last_exported_year) > 0:  
                        
                        
                        doc.set('custom_volume_of_exports_in_years', [])




                    if len(get_last_exported_year) > 0:
                        for year,totals in get_last_exported_year.items():
                            doc.append("custom_volume_of_exports_in_years" , {
                        'year': year,                        
                        'total_amount_in_usd':totals['total_amount_in_usd'],
                        'quantity_in_tons' : totals['quantity_in_tons'],
                        'total_amount_in_egp': totals['total_amount_in_egp']
                    })



                # set_cat_and_vol(emp.name)
   
                
                doc.save()
                frappe.db.commit()
                success = True  
                print("Done")
                set_cat_and_vol(emp.name)

            except frappe.QueryDeadlockError:  
                print("Deadlock encountered, retrying...")
                retry_count += 1
                time.sleep(delay)
                
        if not success:
            print("Failed after retries, skipping this transaction.")




@frappe.whitelist()
def functiongdidaa():
    # Enqueue the background function
    frappe.enqueue(method=exports_years, queue='long')

    # Return a message indicating that the process has started
    return "Data processing started in the background."



@frappe.whitelist()
def get_customer_group(value):
    data = frappe.db.sql("""
        SELECT
            `name`,
            `custom_from`,
            `custom_to`
        FROM
            `tabCustomer Group`
        WHERE 
            %s BETWEEN `custom_from` AND `custom_to`
        """, (value), as_dict=1)

    return data









@frappe.whitelist()
def exports_years_for_current_member(customer):
    doc = frappe.get_doc("Customer", customer)

    tax_id_1 = doc.tax_id

    if tax_id_1:
        print("mina ::::")
        get_last_exported_year = get_member_exportss(tax_id_1)
        print(get_last_exported_year)



        # data_list = list(get_last_exported_year)
        # first = data_list[0]['year']

        # print(first)

        if len(get_last_exported_year) > 0:              
                        
            doc.set('custom_volume_of_exports_in_years', [])

            data_list = list(get_last_exported_year)
            first = data_list[0]['total_amount_in_egp']
            print(first)

        if len(get_last_exported_year) > 0:
            for year,totals in get_last_exported_year.items():
                doc.append("custom_volume_of_exports_in_years" , {
                        'year': year,                        
                        'total_amount_in_usd':totals['total_amount_in_usd'],
                        'quantity_in_tons' : totals['quantity_in_tons'],
                        'total_amount_in_egp': totals['total_amount_in_egp']
                    })



   
                
        doc.save()
        frappe.db.commit()  
        print("Done")







def set_cat_and_vol(customer):
    if customer:
        doc = frappe.get_doc("Customer", customer)

        vol_years = frappe.get_all("Volume of Exports In Years",
                                   filters={'parent': customer,'parenttype': 'Customer'},
                                   order_by='year desc',
                                   fields=['year','total_amount_in_egp'])
        
        if len(vol_years) > 0 :
            last_year_amount = vol_years[0]
            print(f"last_year_amount  {last_year_amount}")
            print(f"year {vol_years[0]['total_amount_in_egp']}")

            if last_year_amount:
                customer_group = get_customer_group(last_year_amount['total_amount_in_egp'])
                customer_group_name = customer_group[0]['name']
                print(customer_group_name)

                doc.customer_group = customer_group_name
                doc.custom_volume_of__exports = vol_years[0]['total_amount_in_egp']
                doc.save()

        else:
            doc.customer_group = 'حجم صادرات اقل من مليون جنيه'
            doc.custom_volume_of__exports = 0
            doc.save()
                



















# @frappe.whitelist()
# def exports_years_for_current_member(customer):
#     # Retrieve the customer document
#     doc = frappe.get_doc("Customer", customer)
#     tax_id = doc.tax_id

#     if tax_id:
#         # print("Processing export years for member with Tax ID:", tax_id)

#         # Get the last exported years using the tax ID
#         get_last_exported_year = get_member_exportss(tax_id)

#         # Print the current state of exports data before clearing
#         # print("Current exports data before clearing:", doc.custom_volume_of_exports_in_years)



#         # Clear existing export data
#         doc.set('custom_volume_of_exports_in_years', [])

#         if get_last_exported_year:
#             # Loop through each year and append data
#             for year, totals in get_last_exported_year.items():
#                 # Ensure totals values are not lists and retrieve them safely
#                 total_amount_in_usd = totals.get('total_amount_in_usd', 0)
#                 quantity_in_tons = totals.get('quantity_in_tons', 0)
#                 total_amount_in_egp = totals.get('total_amount_in_egp', 0)

#                 # Debug output
#                 print(f"Appending for year {year}: USD={total_amount_in_usd}, Tons={quantity_in_tons}, EGP={total_amount_in_egp}")

#                 # Prepare entry to append to the child table
#                 entry = {
#                     'year': year,
#                     'total_amount_in_usd': total_amount_in_usd,
#                     'quantity_in_tons': quantity_in_tons,
#                     'total_amount_in_egp': total_amount_in_egp
#                 }

#                 # Debug: Print the type of each field to ensure no lists are being used
#                 for key, value in entry.items():
#                     print(f"Key: {key}, Value: {value}, Type: {type(value)}")

#                 # Append to the child table
#                 doc.append("custom_volume_of_exports_in_years", entry)

#             # Get the first element to determine the customer group
#             first_key = next(iter(get_last_exported_year), None)  # Get the first key or None
#             if first_key:
#                 first_element = get_last_exported_year[first_key]
#                 # Determine the customer group based on the first element's total amount in EGP
#                 customer_group = get_customer_group(first_element['total_amount_in_egp'])
#                 doc.customer_group = customer_group
#                 doc.custom_volume_of_exports = float(first_element['total_amount_in_egp'])
#             else:
#                 # Handle case where no valid first key was found
#                 doc.customer_group = 'حجم صادرات اقل من مليون جنيه'
#                 doc.custom_volume_of_exports = 0
#         else:
#             # Set defaults if no export years are found
#             doc.customer_group = 'حجم صادرات اقل من مليون جنيه'
#             doc.custom_volume_of_exports = 0
#     else:
#         # Handle case where tax ID is not found
#         doc.customer_group = 'حجم صادرات اقل من مليون جنيه'
#         doc.custom_volume_of_exports = 0

#     # Save and commit changes to the database
#     try:
#         print("Attempting to save customer data...")
#         doc.save()
#         frappe.db.commit()
#         print("Export data updated for customer:", customer)
#     except Exception as e:
#         print(f"Error saving customer data: {e}")
