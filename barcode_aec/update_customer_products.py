import frappe 
from datetime import datetime
from frappe import _
import time


# @frappe.whitelist()
# def last_year_product_export(tax_ids,product_number):
#     data = frappe.db.sql("""
#         SELECT
#             `tax__number` AS `tax_id`,
#             `season__name` AS `season_name`,
#             `season` AS `season`,
#             `customs_product_number` AS `product_number`,
#             YEAR(MAX(`posring_date`)) AS `max_year_posring_date`,
#             SUM(`total_amount_in_egp`) AS `total`,
#             SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
#             SUM(`quantity_in_tons`) AS `quantity_in_tons`
#         FROM
#             `tabVolume Of Member Exports`
#         WHERE 
#             tax__number IN (%s) AND customs_product_number IN (%s)
#         GROUP BY
#             `tax__number`, `season__name`, `season`
#         ORDER BY
#             YEAR(MAX(`posring_date`)) DESC
#         LIMIT 1;
#         """ % ','.join(['%s'] * len(tax_ids)), (tuple(tax_ids),product_number), as_dict=1)
#     return data

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

                tax_id = doc.tax_id

                # products = last_year_product_export(tax_id)

                exported_table = doc.custom_crops_that_are_exported

                for row in exported_table:
                    if row.product:
                        products = last_year_product_export(tax_id,row.product)
                        # products = last_year_product_export('244809119','703100010')
                        print(products)
                        if len(products) > 0:
                            row.season_name = products[0]['season_name']
                            row.total_amount_in_egp = products[0]['total']
                            row.total_amount_in_usd = products[0]['total_amount_in_usd']
                            row.quantity_in_tons = products[0]['quantity_in_tons']

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







@frappe.whitelist()
def last_year_product_export(tax_ids, product_number):
    data = frappe.db.sql("""
        SELECT
            `tax__number` AS `tax_id`,
            `season__name` AS `season_name`,
            `season` AS `season`,
            `customs_product_number` AS `product_number`,
            YEAR(MAX(`posring_date`)) AS `max_year_posring_date`,
            SUM(`total_amount_in_egp`) AS `total`,
            SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
            SUM(`quantity_in_tons`) AS `quantity_in_tons`
        FROM
            `tabVolume Of Member Exports`
        WHERE 
            tax__number IN (%s) AND customs_product_number IN (%s)
        GROUP BY
            `tax__number`, `season__name`, `season`
        ORDER BY
            YEAR(MAX(`posring_date`)) DESC
        LIMIT 1;
        """, (tax_ids, product_number), as_dict=True)
    return data
