import frappe 
from datetime import datetime
from frappe import _
import time

# Define your background function to process the data
@frappe.whitelist()
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
                tax_id_1 = emp.tax_id
                tax_id_2 = emp.custom_tax_id_2
                tax_id_3 = emp.custom_tax_id_3

                tax_ids = [tax_id_1,tax_id_2,tax_id_3]
                member_name = emp.customer_name
                total = 0.0

                if tax_ids:
                    print("mina ::::")
                    get_last_exported_year = volume_of_member_exports_last_year_exported(tax_ids)
                    if len(get_last_exported_year) > 0:  # Check if the list is not empty
                        if get_last_exported_year[0].get('total') is not None:  # Check if 'total' key exists and is not None
                            print(get_last_exported_year)
                            print(get_last_exported_year[0]['total'])

                            group_name = get_customer_group(get_last_exported_year[0]['total'])
                            if len(group_name) == 0:
                                doc.customer_group = 'حجم صادرات اعلي من 100 مليون جنيه'
                                doc.custom_volume_of__exports = get_last_exported_year[0]['total']
                            else:
                                print(group_name)
                                doc.customer_group = group_name[0]['name']
                                doc.custom_volume_of__exports = get_last_exported_year[0]['total']

                    elif not get_last_exported_year:
                        doc.customer_group = 'حجم صادرات اقل من مليون جنيه'
                        
                doc.set('volume_of_member_exports_for_three_years', [])


                
                tot_last_year = volume_of_member_exports_last_year(tax_ids)
                if len(tot_last_year) > 0:
                    doc.append("volume_of_member_exports_for_three_years" , {
                        'season': tot_last_year[0]['season'],
                        'value': tot_last_year[0]['total'],
                        'season_name' :tot_last_year[0]['season_name'],
                        'total_amount_in_usd':tot_last_year[0]['total_amount_in_usd'],
                        'quantity_in_tons' : tot_last_year[0]['quantity_in_tons'],
                        'total_amount_in_egp': tot_last_year[0]['total']
                    })

                tot_two_year = volume_of_member_exports_two_years(tax_ids)
                if len(tot_two_year) > 0:
                    doc.append("volume_of_member_exports_for_three_years" , {
                        'season': tot_two_year[0]['season'],
                        'value': tot_two_year[0]['total'],
                        'season_name' :tot_two_year[0]['season_name'],
                        'total_amount_in_usd':tot_two_year[0]['total_amount_in_usd'],
                        'quantity_in_tons' : tot_two_year[0]['quantity_in_tons'],
                        'total_amount_in_egp': tot_two_year[0]['total']
                    })

                tot_last_three_year = volume_of_member_exports_three_years(tax_ids)
                if len(tot_last_three_year) > 0:
                    doc.append("volume_of_member_exports_for_three_years" , {
                        'season': tot_last_three_year[0]['season'],
                        'value': tot_last_three_year[0]['total'],
                        'season_name' :tot_last_three_year[0]['season_name'],
                        'total_amount_in_usd':tot_last_three_year[0]['total_amount_in_usd'],
                        'quantity_in_tons' : tot_last_three_year[0]['quantity_in_tons'],
                        'total_amount_in_egp': tot_last_three_year[0]['total']
                    })




                last_year_exported = volume_of_member_exports_last_year_exported(tax_ids)
                if last_year_exported:
                    if len(tot_last_year) == 0 and len(tot_two_year)==0 and len(tot_last_three_year)==0:
                        if len(last_year_exported) > 0:
                            print("i don't have last three years")
                            doc.append("volume_of_member_exports_for_three_years" , {
                            'season': last_year_exported[0]['season'],
                            'value': last_year_exported[0]['total'],
                            'season_name' :last_year_exported[0]['season_name'],
                            'total_amount_in_usd':last_year_exported[0]['total_amount_in_usd'],
                            'quantity_in_tons' : last_year_exported[0]['quantity_in_tons'],
                            'total_amount_in_egp': last_year_exported[0]['total']
                        })    
                
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
def volume_of_member_exports_three_years(tax_ids):
    data = frappe.db.sql("""
        SELECT
            `tax__number` AS `tax_id`,
            `season__name` AS `season_name`,
            `season` AS `season`,
            SUM(`total_amount_in_egp`) AS `total`,
            SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
            SUM(`quantity_in_tons`) AS `quantity_in_tons`
        FROM
            `tabVolume Of Member Exports`
        WHERE 
            YEAR(`posring_date`) = YEAR(CURDATE()) - 3
            AND tax__number IN (%s)
        GROUP BY
            `tax__number`, `season__name`, `season`
        """ % ','.join(['%s'] * len(tax_ids)), tuple(tax_ids), as_dict=1)
    return data



@frappe.whitelist()
def volume_of_member_exports_two_years(tax_ids):
    data = frappe.db.sql("""
        SELECT
            `tax__number` AS `tax_id`,
            `season__name` AS `season_name`,
            `season` AS `season`,
            SUM(`total_amount_in_egp`) AS `total`,
            SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
            SUM(`quantity_in_tons`) AS `quantity_in_tons`
        FROM
            `tabVolume Of Member Exports`
        WHERE 
            YEAR(`posring_date`) = YEAR(CURDATE()) - 2
            AND tax__number IN (%s)
        GROUP BY
            `tax__number`, `season__name`, `season`
        """ % ','.join(['%s'] * len(tax_ids)), tuple(tax_ids), as_dict=1)
    return data




@frappe.whitelist()
def volume_of_member_exports_last_year(tax_ids):
    data = frappe.db.sql("""
        SELECT
            `tax__number` AS `tax_id`,
            `season__name` AS `season_name`,
            `season` AS `season`,
            SUM(`total_amount_in_egp`) AS `total`,
            SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
            SUM(`quantity_in_tons`) AS `quantity_in_tons`
        FROM
            `tabVolume Of Member Exports`
        WHERE 
            YEAR(`posring_date`) = YEAR(CURDATE()) - 1
            AND tax__number IN (%s)
        GROUP BY
            `tax__number`, `season__name`, `season`
        """ % ','.join(['%s'] * len(tax_ids)), tuple(tax_ids), as_dict=1)
    return data




@frappe.whitelist()
def volume_of_member_exports_last_year_exported(tax_ids):
    data = frappe.db.sql("""
        SELECT
            `tax__number` AS `tax_id`,
            `season__name` AS `season_name`,
            `season` AS `season`,
            YEAR(MAX(`posring_date`)) AS `max_year_posring_date`,
            SUM(`total_amount_in_egp`) AS `total`,
            SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
            SUM(`quantity_in_tons`) AS `quantity_in_tons`
        FROM
            `tabVolume Of Member Exports`
        WHERE 
            tax__number IN (%s)
        GROUP BY
            `tax__number`, `season__name`, `season`
        ORDER BY
            YEAR(MAX(`posring_date`)) DESC
        LIMIT 1;
        """ % ','.join(['%s'] * len(tax_ids)), tuple(tax_ids), as_dict=1)
    return data




@frappe.whitelist()
def get_exported_products(tax_ids):
    data = frappe.db.sql("""
        SELECT
            `tax__number` AS `tax_id`,
            `season__name` AS `season_name`,
            `season` AS `season`,
            SUM(`total_amount_in_egp`) AS `total`,
            SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
            SUM(`quantity_in_tons`) AS `quantity_in_tons`
        FROM
            `tabVolume Of Member Exports`
        WHERE 
            # YEAR(`posring_date`) = YEAR(CURDATE()) - 3
            AND tax__number IN (%s)
        GROUP BY
            `tax__number`, `season__name`, `season`,`customs_product_number`, `products_name`
        """ % ','.join(['%s'] * len(tax_ids)), tuple(tax_ids), as_dict=1)
    return data

