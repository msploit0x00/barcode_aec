import frappe 
from datetime import datetime

@frappe.whitelist()
def functiongdidaa():
    all_customers = frappe.db.sql("""
        SELECT
            `name`,
            `customer_name`,
            `tax_id`
        FROM
            `tabCustomer`
        WHERE
            `tax_id` IS NOT NULL
    """, as_dict=1)

    for customer in all_customers:
        tax_id = customer.tax_id
        customer_name = customer.customer_name
        volume_data, season_data = get_volume_of_member_exports(tax_id)
        
        if not volume_data:
            frappe.msgprint(f"This member has no tax id: {customer_name}")
            continue
        
        set_customer_data(customer.name, volume_data, season_data)

def get_volume_of_member_exports(tax_id):
    volume_query = """
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
            YEAR(`posring_date`) BETWEEN YEAR(CURDATE()) - 3 AND YEAR(CURDATE()) - 1
            AND `tax__number` = %s
        GROUP BY
            `tax__number`, `season__name`, `season`
    """
    volume_data = frappe.db.sql(volume_query, tax_id, as_dict=1)
    return volume_data, []

def set_customer_data(customer_id, volume_data, season_data):
    customer_group_query = """
        SELECT
            `name`
        FROM
            `tabCustomer Group`
        WHERE 
            %(total)s BETWEEN `custom_from` AND `custom_to`
    """
    for volume in volume_data:
        customer_group_data = frappe.db.sql(customer_group_query, {'total': volume['total']}, as_dict=1)
        
        if customer_group_data:
            customer_group_name = customer_group_data[0]['name']
            frappe.db.set_value("Customer", customer_id, "customer_group", customer_group_name)
            frappe.db.set_value("Customer", customer_id, "custom_volume_of__exports", volume['total'])
            
            # Append volume of member exports for three years
            frappe.db.append("Customer", customer_id, "volume_of_member_exports_for_three_years", {
                'season': volume['season'],
                'value': volume['total'],
                'season_name': volume['season_name'],
                'total_amount_in_usd': volume['total_amount_in_usd'],
                'quantity_in_tons': volume['quantity_in_tons'],
                'total_amount_in_egp': volume['total']
            })

