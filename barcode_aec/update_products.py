import frappe 
from datetime import datetime
from frappe import _
import time

@frappe.whitelist()
def process_data(retries=3, delay=0.5):
    all_products = frappe.db.sql("""
        SELECT
            `name`
        FROM
            `tabProduct`
        """, as_dict=1)

    num = len(all_products)
    counter = 0
    
    for prod in all_products:
        print(prod.name)
        retry_count = 0
        success = False

        while retry_count < retries and not success:
            try:
                doc = frappe.get_doc("Product", prod.name)
                counter += 1
                frappe.publish_progress(counter * 100 / num, title=_("Updating ..."))
                # member_name = emp.customer_name
                total = 0.0

                if doc.name:
                    print("mina ::::")


                    exports = get_products_exports(doc.name)
                    print(exports)
                    if len(exports) > 0:
                        for export in exports:
                            doc.append("custom_products_export_volume" , {
                        'season': export['season_name'],
                        'total_in_egp': export['total_in_egp'],
                        'total_in_usd' :export['total_amount_in_usd'],
                        'quantity_in_tons':export['quantity_in_tons']
                        
                    })
                    # get_last_exported_year = volume_of_member_exports_last_year_exported(tax_id)
                    # if get_last_exported_year:  # Check if the list is not empty
                    #     if get_last_exported_year[0].get('total') is not None:  # Check if 'total' key exists and is not None
                    #         print(get_last_exported_year)
                    #         print(get_last_exported_year[0]['total'])

                    #         group_name = get_customer_group(get_last_exported_year[0]['total'])
                    #         if len(group_name) == 0:
                    #             doc.customer_group = 'حجم صادرات اعلي من 100 مليون جنيه'
                    #             doc.custom_volume_of__exports = get_last_exported_year[0]['total']
                    #         else:
                    #             print(group_name)
                    #             doc.customer_group = group_name[0]['name']
                    #             doc.custom_volume_of__exports = get_last_exported_year[0]['total']

                    # elif not get_last_exported_year:
                    #     doc.customer_group = 'حجم صادرات اقل من مليون جنيه'
                        
                # doc.set('volume_of_member_exports_for_three_years', [])



      

                
                # tot_last_year = volume_of_member_exports_last_year(tax_id)
                # if tot_last_year != 0:
                #     doc.append("volume_of_member_exports_for_three_years" , {
                #         'season': tot_last_year[0]['season'],
                #         'value': tot_last_year[0]['total'],
                #         'season_name' :tot_last_year[0]['season_name'],
                #         'total_amount_in_usd':tot_last_year[0]['total_amount_in_usd'],
                #         'quantity_in_tons' : tot_last_year[0]['quantity_in_tons'],
                #         'total_amount_in_egp': tot_last_year[0]['total']
                #     })

                # tot_two_year = volume_of_member_exports_two_years(tax_id)
                # if tot_two_year != 0:
                #     doc.append("volume_of_member_exports_for_three_years" , {
                #         'season': tot_two_year[0]['season'],
                #         'value': tot_two_year[0]['total'],
                #         'season_name' :tot_two_year[0]['season_name'],
                #         'total_amount_in_usd':tot_two_year[0]['total_amount_in_usd'],
                #         'quantity_in_tons' : tot_two_year[0]['quantity_in_tons'],
                #         'total_amount_in_egp': tot_two_year[0]['total']
                #     })
                # tot_last_three_year = volume_of_member_exports_three_years(tax_id)
                # if tot_last_three_year != 0:
                #     doc.append("volume_of_member_exports_for_three_years" , {
                #         'season': tot_last_three_year[0]['season'],
                #         'value': tot_last_three_year[0]['total'],
                #         'season_name' :tot_last_three_year[0]['season_name'],
                #         'total_amount_in_usd':tot_last_three_year[0]['total_amount_in_usd'],
                #         'quantity_in_tons' : tot_last_three_year[0]['quantity_in_tons'],
                #         'total_amount_in_egp': tot_last_three_year[0]['total']
                #     })




                # last_year_exported = volume_of_member_exports_last_year_exported(tax_id)
                # if len(tot_last_year) == 0 and len(tot_two_year)==0 and len(tot_last_three_year)==0:
                #     if len(last_year_exported) != 0:
                #         print("i don't have last three years")
                #     doc.append("volume_of_member_exports_for_three_years" , {
                #         'season': last_year_exported[0]['season'],
                #         'value': last_year_exported[0]['total'],
                #         'season_name' :last_year_exported[0]['season_name'],
                #         'total_amount_in_usd':last_year_exported[0]['total_amount_in_usd'],
                #         'quantity_in_tons' : last_year_exported[0]['quantity_in_tons'],
                #         'total_amount_in_egp': last_year_exported[0]['total']
                #     })    
                
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




















@frappe.whitelist(allow_guest=True)
def get_products_exports(name):
    data = frappe.db.sql("""

        SELECT
    `season__name` AS `season_name`,
    SUM(`total_amount_in_egp`) AS `total_in_egp`,
    SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
    SUM(`quantity_in_tons`) AS `quantity_in_tons`
FROM
    `tabVolume Of Member Exports`
WHERE 
    `products_name` = %s
GROUP BY
    `season__name`;





""",name,as_dict=1)
    return data