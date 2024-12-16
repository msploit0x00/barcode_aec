# Copyright (c) 2024, ds and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class ExportOpportunities(Document):
    @frappe.whitelist()  
    def get_volume_exports(self):
        doc = self.as_dict()
        conditions = []
        committe_condition = []
        fields = {
                "committee_name": doc.get("committee"),
                "membership_status": doc.get("membership_status"),
                "countries_name": doc.get("countries_name"),
                "cluster": doc.get("cluster"),
                "season": doc.get("season"),
                "shipping_port": doc.get("shipping_port"),
                "product_number_local_hs": doc.get("product_number_local_hs"),
                "number_of_records":doc.get("number_of_records")
            }
        # Construct the WHERE conditions based on the fields dictionary


        if fields["membership_status"]:
            conditions.append("`tabCustomer`.`custom_customer_status` = %(membership_status)s")

        if fields["committee_name"]:
            conditions.append("committes.committees_name = %(committee_name)s")

        if fields["countries_name"]:
            conditions.append("`tabVolume Of Member Exports`.`country_in_arabic` = %(countries_name)s")

        if fields["cluster"]:
            conditions.append("`tabCountries`.`geographical_clusters_name` = %(cluster)s")

        if fields["season"]:
            conditions.append("`tabVolume Of Member Exports`.`season__name` = %(season)s")

        if fields["shipping_port"]:
            conditions.append("`tabVolume Of Member Exports`.`shipping_port` = %(shipping_port)s")

        if fields["product_number_local_hs"]:
            conditions.append("`tabVolume Of Member Exports`.`customs_product_number` = %(product_number_local_hs)s")

        # If there's a condition, join them with AND
        conditions_str = " AND ".join(conditions)
        # committe_condition_str = " AND".join(committe_condition)
        # # Add the WHERE clause if conditions exist
        # if committe_condition_str:
        #     committe_condition_str = "WHERE" + committe_condition_str
        # else:
        #     committe_condition_str = ""    
        if conditions_str:
            conditions_str = "WHERE " + conditions_str
        else:
            conditions_str = ""  # No condition, so no WHERE clause

        # Construct the LIMIT clause
        limit_clause = ""
        if fields["number_of_records"]:
            limit_clause = f"LIMIT {fields['number_of_records']}"

        # The final query
        sql = f"""
        SELECT
            GROUP_CONCAT(DISTINCT `tabVolume Of Member Exports`.`customs_product_number` SEPARATOR ', ') AS `products`,   
            GROUP_CONCAT(DISTINCT `tabVolume Of Member Exports`.`country_in_arabic` SEPARATOR ', ') AS `countries`,            
            GROUP_CONCAT(DISTINCT `tabCountries`.`geographical_clusters_name` SEPARATOR ', ') AS `cluster`,
            GROUP_CONCAT(DISTINCT `tabVolume Of Member Exports`.`shipping_port` SEPARATOR ', ' ) AS shipping_port,
            `tabCustomer`.`name` AS `member`,
            `tabCustomer`.`custom_customer_status`,  
            `tabCustomer`.`tax_id`, 
            `tabCustomer`.`custom_email` AS email, 
            `tabCustomer`.`custom_name_of_the_cioowner_of_the_company`,
            `tabVolume Of Member Exports`.`season__name`,
            SUM(CAST(`tabVolume Of Member Exports`.`quantity_in_tons` AS FLOAT)) AS `quantity_in_tons`,
            SUM(`tabVolume Of Member Exports`.`total_amount_in_egp`) AS `total_amount_in_egp`,
            SUM(`tabVolume Of Member Exports`.`total_amount_in_usd`) AS `total_amount_in_usd`,
            committes.committees_name AS committees_name
        FROM
            `tabVolume Of Member Exports`
        LEFT JOIN `tabCustomer`
            ON `tabVolume Of Member Exports`.`tax__number` = `tabCustomer`.`tax_id`
        LEFT JOIN (
            SELECT
                `tabCustomer`.`name` AS customer,
                GROUP_CONCAT(DISTINCT committees.committees SEPARATOR ', ') AS committees_name
            FROM 
                `tabCommittees you would like to join` AS committees
            LEFT JOIN `tabCustomer`
                ON committees.parent = `tabCustomer`.`name`
              
            GROUP BY `tabCustomer`.`name`
        ) AS committes ON committes.customer = `tabCustomer`.`name`
        LEFT JOIN `tabCountries`
            ON `tabCountries`.`arabic_name` = `tabVolume Of Member Exports`.`country_in_arabic`
        {conditions_str}
         AND `tabCustomer`.`tax_id` IS NOT NULL
        GROUP BY 
            `tabCustomer`.`name`
        ORDER BY 
            SUM(`tabVolume Of Member Exports`.`quantity_in_tons`) DESC
        {limit_clause};
        """

        
#         sql = f"""
#             SELECT
#                `tabCustomer`.`name` AS `member`,
#             `tabCustomer`.`tax_id`,  
#           GROUP_CONCAT(DISTINCT `tabVolume Of Member Exports`.`country_in_arabic` SEPARATOR ', ') AS `countries`,            
#           GROUP_CONCAT(DISTINCT `tabCountries`.`geographical_clusters_name` SEPARATOR ', ') AS `cluster`,
#             `tabCustomer`.`custom_name_of_the_cioowner_of_the_company` AS `custom_name_of_the_cioowner_of_the_company`,
#             GROUP_CONCAT(DISTINCT `tabCommittees you would like to join`.`committees` SEPARATOR ', ') AS `committee_name`,
 
#             `tabVolume Of Member Exports`.`season__name` AS `season__name`,
#             SUM(CAST(`tabVolume Of Member Exports`.`quantity_in_tons` AS Float)) AS `quantity_in_tons`,
#             SUM(`tabVolume Of Member Exports`.`total_amount_in_egp`) AS `total_amount_in_egp`,
#               SUM(`tabVolume Of Member Exports`.`total_amount_in_usd`) AS `total_amount_in_usd`,
#             GROUP_CONCAT(DISTINCT `tabVolume Of Member Exports`.`customs_product_number` SEPARATOR ', ') AS `product_number `,
#             GROUP_CONCAT(DISTINCT `tabVolume Of Member Exports`.`shipping_port` SEPARATOR ', ') AS `shipping_port`,
#             `tabCustomer`.`territory` AS `territory_code`,
#             `tabCustomer`.`governorate_name` AS `territory`,
#             `tabCustomer`.`custom_ceo_mobile` AS `customer_primary_contact`,
#             `tabCustomer`.`custom_customer_status` AS `custom_customer_status`,
#             `tabCustomer`.`custom_email` AS `email`    
# FROM
#     `tabVolume Of Member Exports`
# LEFT JOIN `tabCustomer`
#     ON `tabVolume Of Member Exports`.`tax__number` = `tabCustomer`.`tax_id`    
# LEFT JOIN `tabCommittees you would like to join`
#             ON `tabCommittees you would like to join`.`parent` = `tabCustomer`.`name`    
# LEFT JOIN  `tabCountries`
# ON `tabCountries`.`arabic_name` = `tabVolume Of Member Exports`.`country_in_arabic`           
#         {conditions_str}
#         AND `tabCustomer`.`tax_id` IS NOT NULL
#         GROUP BY `member`
#         ORDER BY SUM(`tabVolume Of Member Exports`.`quantity_in_tons`) DESC
#         {limit_clause};
#     """

#         sql = """
#               Select
#             GROUP_CONCAT(DISTINCT `tabVolume Of Member Exports`.`customs_product_number` SEPARATOR ', ') AS `products`,   
#           GROUP_CONCAT(DISTINCT `tabVolume Of Member Exports`.`country_in_arabic` SEPARATOR ', ') AS `countries`,            
#           GROUP_CONCAT(DISTINCT `tabCountries`.`geographical_clusters_name` SEPARATOR ', ') AS `cluster`,
#     `tabCustomer`.`name` AS `member`,
#     `tabCustomer`.`tax_id`,  
#     `tabCustomer`.`custom_name_of_the_cioowner_of_the_company` AS `custom_name_of_the_cioowner_of_the_company`,
#     `tabVolume Of Member Exports`.`season__name` AS `season__name`,
#     SUM(CAST(`tabVolume Of Member Exports`.`quantity_in_tons` AS Float)) AS `quantity_in_tons`,
#     SUM(`tabVolume Of Member Exports`.`total_amount_in_egp`) AS `total_amount_in_egp`,
#     SUM(`tabVolume Of Member Exports`.`total_amount_in_usd`) AS `total_amount_in_usd`,
#     committes.committees_name
# FROM
#     `tabVolume Of Member Exports`
# LEFT JOIN `tabCustomer`
#     ON `tabVolume Of Member Exports`.`tax__number` = `tabCustomer`.`tax_id`
# left join(
#     SELECT
#     `tabCustomer`.`name` as customer,
#     GROUP_CONCAT(DISTINCT committees.committees SEPARATOR ', ') as committees_name
# FROM 

#   `tabCommittees you would like to join` as committees 

# LEFT JOIN 
#          `tabCustomer`
#     ON committees.parent = `tabCustomer`.`name`

# GROUP BY
#     `tabCustomer`.`name`
    
#     )AS committes ON committes.customer = `tabCustomer`.`name` 
    
# LEFT JOIN  `tabCountries`
# ON `tabCountries`.`arabic_name` = `tabVolume Of Member Exports`.`country_in_arabic`       
# WHERE 
#     # `tabCustomer`.`tax_id` = '341876119'
#     # AND
#      `tabVolume Of Member Exports`.`season__name` = '2022-2023'
#     AND `tabCustomer`.`tax_id` IS NOT NULL
# GROUP BY 

#     `tabCustomer`.`name`

# ORDER BY 
#     SUM(`tabVolume Of Member Exports`.`quantity_in_tons`) DESC
# LIMIT 3; 
#         """  
        mydata = frappe.db.sql(
        sql,
        {
    
            "season":fields["season"],
            "committee_name": fields["committee_name"],
            "membership_status": fields["membership_status"],
            "countries_name": fields["countries_name"],
            "cluster": fields["cluster"],
            "shipping_port":fields["shipping_port"],
            "product_number_local_hs":fields["product_number_local_hs"],
            "number_of_records":fields["number_of_records"],
        
        },as_dict=True,)

        
        mydata_sorted = sorted(mydata, key=lambda x: x['quantity_in_tons'], reverse=True)
        return mydata

  
        
