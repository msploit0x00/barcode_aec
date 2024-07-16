import frappe
from datetime import datetime
from frappe import _
import time

############################## Update Customer category ....
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
        doc = frappe.get_doc("Customer", emp.name)
        counter += 1
        frappe.publish_progress(counter * 100 / num, title=_("Updating ..."))
        tax_id_1 = emp.tax_id
        tax_id_2 = emp.custom_tax_id_2
        tax_id_3 = emp.custom_tax_id_3
        tax_ids = [tax_id_1,tax_id_2,tax_id_3]
        if tax_ids:
            print("msg tax ids is Found")
            get_last_exported_year = volume_of_member_exports_last_year_exported(tax_ids)
            print("get_last_exported_year", get_last_exported_year)
            if get_last_exported_year and 'total' in get_last_exported_year[0]:  
                total = get_last_exported_year[0]['total']
                value = get_customer_group(total)
                if value:
                    customer_group_update = value[0]['name']
                    print("Value customer_group_update", customer_group_update)
                    if customer_group_update:
                        doc.customer_group = customer_group_update
                        print(doc.customer_name, doc.customer_group)
                        doc.save()    
                        frappe.db.commit()
                        print("Done")
      
@frappe.whitelist()
def volume_of_member_exports_last_year_exported(tax_ids):
    data = frappe.db.sql("""
        SELECT
            `tax_id` AS `tax_id`,
            `season__name` AS `season_name`,
            `season` AS `season`,
            `year` AS `year`,
            YEAR(MAX(`posring_date`)) AS `max_year_posring_date`,
            SUM(`total_amount_in_egp`) AS `total`,
            SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
            SUM(`quantity_in_tons`) AS `quantity_in_tons`
        FROM
            `tabVolume Of Member Exports`
        WHERE 
            tax_id IN (%s)
            AND `tabVolume Of Member Exports`.`year` = YEAR(CURDATE()) - 1

        LIMIT 1;
        """ % ','.join(['%s'] * len(tax_ids)), tuple(tax_ids), as_dict=1)
    return data
    
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



