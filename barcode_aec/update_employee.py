import frappe 
from datetime import datetime
from frappe import _
import time

# Define your background function to process the data
@frappe.whitelist()
def process_data():
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
        tax_id = emp.tax_id
        member_name = emp.customer_name
        total = 0.0
        if tax_id:
            print("mina ::::")
            get_last_exported_year = volume_of_member_exports_last_year_exported(tax_id)
            if get_last_exported_year:  # Check if the list is not empty
                if get_last_exported_year[0].get('total') is not None:  # Check if 'total' key exists and is not None
                    print(get_last_exported_year)
                    print(get_last_exported_year[0]['total'])
                    group_name = get_customer_group(get_last_exported_year[0]['total'])
                    print(group_name)
                    doc.customer_group = group_name[0]['name']
                    doc.custom_volume_of__exports = get_last_exported_year[0]['total']

            
            # vol = volume_of_member_exports_last_year(tax_id)
            # total = vol[0]['total']
            # print(total)
            # if not  vol[0]['total']:
            #     vol = volume_of_member_exports_two_years(tax_id)
            #     total = vol[0]['total']
            #     print(f"2 {total}")
            #     if not  vol[0]['total']:
            #         vol = volume_of_member_exports_three_years(tax_id)
            #         total = vol[0]['total']
            #         print(f"3 {total}")    
        #             if not vol:
        #                 frappe.msgprint("This member has no tax id {}".format(member_name))
        # # if len(vol) != 0:
        # if vol:
        #     print(vol)
        #     customer_group_for_last_year = get_customer_group(vol[0]['total'])
        #     print("First Done")
        #     if customer_group_for_last_year:
        #         customer_group_name = customer_group_for_last_year[0]['name']

        #         doc.customer_group = customer_group_name
        #         doc.custom_volume_of__exports =  vol[0]['total']
        #         print(doc.customer_group)
        #         print(doc.custom_volume_of__exports)
        #             # frappe.db.set_value("Customer", emp.name, "customer_group", customer_group_name)
        #             # frappe.db.set_value("Customer", emp.name, "custom_volume_of__exports", vol[0]['total'])
        
        
        doc.set('volume_of_member_exports_for_three_years', [])
        
        tot_last_year = volume_of_member_exports_last_year(tax_id)
        if tot_last_year != 0:
            doc.append("volume_of_member_exports_for_three_years" , {
                'season': tot_last_year[0]['season'],
                'value': tot_last_year[0]['total'],
                'season_name' :tot_last_year[0]['season_name'],
                'total_amount_in_usd':tot_last_year[0]['total_amount_in_usd'],
                'quantity_in_tons' : tot_last_year[0]['quantity_in_tons'],
                'total_amount_in_egp': tot_last_year[0]['total']
            })

        tot_two_year = volume_of_member_exports_two_years(tax_id)
        if tot_two_year != 0:
            doc.append("volume_of_member_exports_for_three_years" , {
                'season': tot_two_year[0]['season'],
                'value': tot_two_year[0]['total'],
                'season_name' :tot_two_year[0]['season_name'],
                'total_amount_in_usd':tot_two_year[0]['total_amount_in_usd'],
                'quantity_in_tons' : tot_two_year[0]['quantity_in_tons'],
                'total_amount_in_egp': tot_two_year[0]['total']
            })
        tot_last_three_year = volume_of_member_exports_three_years(tax_id)
        if tot_last_three_year != 0:
            doc.append("volume_of_member_exports_for_three_years" , {
                'season': tot_last_three_year[0]['season'],
                'value': tot_last_three_year[0]['total'],
                'season_name' :tot_last_three_year[0]['season_name'],
                'total_amount_in_usd':tot_last_three_year[0]['total_amount_in_usd'],
                'quantity_in_tons' : tot_last_three_year[0]['quantity_in_tons'],
                'total_amount_in_egp': tot_last_three_year[0]['total']
            })

       
        doc.save()
        frappe.db.commit()
        time.sleep(0.5)
    # doc.customer_group = get_customer_group(doc.volume_of_member_exports_for_three_years[0]['value'])
    # doc.custom_volume_of__exports = doc.volume_of_member_exports_for_three_years[0]['total_amount_in_egp']
    # doc.save()

@frappe.whitelist()
def functiongdidaa():
    # Enqueue the background function
    frappe.enqueue(method=process_data, queue='long')

    # Return a message indicating that the process has started
    return "Data processing started in the background."


        
@frappe.whitelist()
def update_customer(result , emp ,customer_group ):
    for memo3 in customer_group:
        if result['total'] > memo3.custom_from and result['total'] <= memo3.custom_to and memo3.customer_group_name != 'خدمي' :
            frappe.db.set_value("Customer" , emp.name , "customer_group" , memo3.name)
            frappe.db.set_value("Customer" , emp.name , "custom_volume_of__exports" , result.total)
            
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
def volume_of_member_exports_three_years(tax_id):
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
            AND tax__number = %s ;
        """ , tax_id ,as_dict=1)
    return data

@frappe.whitelist()
def volume_of_member_exports_two_years(tax_id):
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
            AND tax__number =%s ;
        """ , tax_id ,as_dict=1)
    return data


@frappe.whitelist()
def volume_of_member_exports_last_year(tax_id):
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
            AND tax__number =%s ;
        """ , tax_id ,as_dict=1)
    return data


@frappe.whitelist()
def volume_of_member_exports_last_year_exported(tax_id):
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
            tax__number = %s
        GROUP BY
            `tax__number`, `season__name`, `season`
        ORDER BY
            YEAR(MAX(`posring_date`)) DESC
        LIMIT 1;
        """ , tax_id ,as_dict=1)
    return data
