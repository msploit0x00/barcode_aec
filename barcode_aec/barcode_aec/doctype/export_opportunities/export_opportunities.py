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
        fields = {
                "committee_name": doc.get("committee"),
                "membership_status": doc.get("membership_status"),
                "country": doc.get("country"),
                # "cluster": doc.get("cluster"),
                "season": doc.get("season"),
                "shipping_port": doc.get("shipping_port"),
                "product_number_local_hs": doc.get("product_number_local_hs"),
                "number_of_records":doc.get("number_of_records")
            }
        if fields["membership_status"]: 
            conditions.append(
                "`tabCustomer`.`custom_customer_status` = %(membership_status)s"
            )
        if fields["committee_name"]:
            conditions.append(
                "`tabCommittees you would like to join`.`committees` = %(committee_name)s"
            )           
        if fields["country"]:
            conditions.append(
                "`tabVolume Of Member Exports`.`country_in_arabic` = %(country)s"
            )
        # if fields["cluster"]:
        #     conditions.append("`tabCountries`.`geographical_clusters_name` = %(cluster)s")
        if fields["season"]:
            conditions.append("`tabVolume Of Member Exports`.`season__name` = %(season)s")
        if fields["shipping_port"]:
            conditions.append("`tabVolume Of Member Exports`.`shipping_port` = %(shipping_port)s")
        if fields["product_number_local_hs"]:
            conditions.append("`tabVolume Of Member Exports`.`customs_product_number` = %(product_number_local_hs)s")  
        if fields["number_of_records"]:
            conditions.append("CAST(`tabVolume Of Member Exports`.`quantity_in_tons` AS Float)  > %(number_of_records)s")  
        conditions_str = " AND ".join(conditions)
        if conditions_str:
            conditions_str = "WHERE " + conditions_str
        sql = f"""
        SELECT
            `tabCustomer`.`name` AS `member`,
            `tabCustomer`.`tax_id`,  
            GROUP_CONCAT(DISTINCT `tabVolume Of Member Exports`.`country_in_arabic` SEPARATOR ', ') AS `country`,
            GROUP_CONCAT(DISTINCT `tabCountries`.`geographical_clusters_name` SEPARATOR ', ') AS `cluster`,
            `tabCustomer`.`custom_name_of_the_cioowner_of_the_company` AS `custom_name_of_the_cioowner_of_the_company`,
            GROUP_CONCAT(DISTINCT `tabCommittees you would like to join`.`committees` SEPARATOR ', ') AS `committee_name`,
            `tabVolume Of Member Exports for Three Years`.`total_amount_in_egp` AS `total_amount_in_egp`,
            CONCAT(FLOOR(`tabVolume Of Member Exports for Three Years`.`total_amount_in_usd`), ' $') AS `total_amount_in_usd`,
            `tabVolume Of Member Exports`.`season__name` AS `season__name`,
            CAST(`tabVolume Of Member Exports`.`quantity_in_tons` AS Float) AS `quantity_in_tons`,
            `tabVolume Of Member Exports`.`customs_product_number` AS `product_number `,
            `tabVolume Of Member Exports`.`shipping_port` AS `shipping_port`,
            `tabCustomer`.`territory` AS `territory_code`,
            `tabCustomer`.`governorate_name` AS `territory`,
            `tabCustomer`.`custom_ceo_mobile` AS `customer_primary_contact`,
            `tabCustomer`.`custom_customer_status` AS `custom_customer_status`,
            `tabCustomer`.`custom_email` AS `email`    
        FROM
            `tabVolume Of Member Exports`
        left JOIN `tabCustomer`
            ON `tabVolume Of Member Exports`.`tax__number` = `tabCustomer`.`tax_id`    
        LEFT JOIN `tabCommittees you would like to join`
            ON `tabCommittees you would like to join`.`parent` = `tabCustomer`.`name`
        LEFT JOIN `tabVolume Of Member Exports for Three Years`
            ON `tabVolume Of Member Exports for Three Years`.`parent` = `tabCustomer`.`name`
        Right JOIN `tabCountries`
            ON `tabCountries`.`name` = `tabVolume Of Member Exports`.`country_code`
        {conditions_str}
        GROUP BY `member`
        ORDER BY `tabVolume Of Member Exports`.`quantity_in_tons` ASC;
    """
        mydata = frappe.db.sql(
        sql,
        {
    
            "season":fields["season"],
            "committee_name": fields["committee_name"],
            "membership_status": fields["membership_status"],
            "country": fields["country"],
            "shipping_port":fields["shipping_port"],
            "product_number_local_hs":fields["product_number_local_hs"],
            "number_of_records":fields["number_of_records"],
        
        },as_dict=True,)

        doc.targeted_members = []

        # Get existing members (if needed for checks)
        existing_members = {row.member_code for row in doc.targeted_members}

        # Append new data to targeted_members
        # Initialize an empty list
        mylist = []

        # Loop through the query results and add each member to the list
        for row in mydata:
            mylist.append({"member_code": row["member"]})
        return mydata
        # # Clear existing targeted_members and append all members from mylist
        # self.get("targeted_members").clear()  # Clear the targeted_members table

        # # Append all members from mylist to the targeted_members child table
        # for member in mylist:
        #     self.append("targeted_members", member)

        # # Save the document to persist changes
        # doc.save()
        # frappe.db.commit()



# GROUP_CONCAT(DISTINCT `tabCountries`.`english_name` SEPARATOR ', ')AS country,
# 			GROUP_CONCAT(DISTINCT `tabCountries`.`geographical_clusters_name` SEPARATOR ', ') AS clusters,


#     inner JOIN `tabCountries`
# 			ON `tabCountries`.`name` = `tabVolume Of Member Exports`.`country_code`