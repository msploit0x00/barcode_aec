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
        con = []
        committe_condition = []
        fields = {
                "committee_name": doc.get("committee"),
                "membership_status": doc.get("membership_status"),
                "countries_name": doc.get("countries_name"),
                "cluster": doc.get("cluster"),
                "season": doc.get("season"),
                "shipping_port": doc.get("shipping_port"),
                "product_number_local_hs": doc.get("product_number_local_hs"),
                "number_of_records":doc.get("number_of_records"),
                "export_volume_categories":doc.get("export_volume_categories"),
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
        if fields["export_volume_categories"]:
            con.append(" AND `tabExport Volume Categories`.`name` = %(export_volume_categories)s")
  

        conditions_str = " AND ".join(conditions)   
        if conditions_str:
            conditions_str = "WHERE " + conditions_str
        else:
            conditions_str = ""   

        con_str = " ".join(con)
        # Construct the LIMIT clause
        limit_clause = ""
        if fields["number_of_records"]:
            limit_clause = f"LIMIT {fields['number_of_records']}"
        print("commmmmmmmmmmmmmm",con_str,fields["export_volume_categories"])
        # The final query
        sql = f"""
      SELECT 
        `tabExport Volume Categories`.`name` AS `category_name`,
        `tabExport Volume Categories`.`from_volume`,
        `tabExport Volume Categories`.`to_volume`,
        vols.`member`,
        vols.`custom_customer_status`,  
        vols.`tax_id`, 
        vols.email, 
        vols.`custom_name_of_the_cioowner_of_the_company`,
        vols.`customer_name`,
        vols.`season__name`,
        vols.`quantity_in_tons`,
        vols.`committees_name`,
        vols.`products`,
        vols.`countries`,
        vols.`cluster`,
        vols.`shipping_port`,
        vols.`total_amount_in_egp`,
        vols.`total_amount_in_usd`
      FROM  
          `tabExport Volume Categories`
      RIGHT JOIN (
          SELECT
              `tabCustomer`.`custom_name_of_the_cioowner_of_the_company`,
              `tabCustomer`.`custom_customer_status`,  
              `tabCustomer`.`tax_id`, 
              `tabCustomer`.`custom_email` AS email, 
              `tabCustomer`.`name` AS `member`,
              `tabCustomer`.`customer_name`, 
              `tabVolume Of Member Exports`.`season__name`,
              SUM(ROUND(`tabVolume Of Member Exports`.`quantity_in_tons`, 2)) AS `quantity_in_tons`,
              SUM(ROUND(`tabVolume Of Member Exports`.`total_amount_in_egp`, 2)) AS `total_amount_in_egp`,
              SUM(ROUND(`tabVolume Of Member Exports`.`total_amount_in_usd`, 2)) AS `total_amount_in_usd`,
              GROUP_CONCAT(DISTINCT `tabVolume Of Member Exports`.`customs_product_number` SEPARATOR ', ') AS `products`,   
              GROUP_CONCAT(DISTINCT `tabVolume Of Member Exports`.`country_in_arabic` SEPARATOR ', ') AS `countries`,            
              GROUP_CONCAT(DISTINCT `tabCountries`.`geographical_clusters_name` SEPARATOR ', ') AS `cluster`,
              GROUP_CONCAT(DISTINCT `tabVolume Of Member Exports`.`shipping_port` SEPARATOR ', ') AS `shipping_port`,
              committes.committees_name AS committees_name
          FROM  
              `tabVolume Of Member Exports`
          LEFT JOIN `tabCustomer`
              ON `tabVolume Of Member Exports`.`tax__number` = `tabCustomer`.`tax_id`
          LEFT JOIN `tabCountries`
              ON `tabCountries`.`arabic_name` = `tabVolume Of Member Exports`.`country_in_arabic`
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
        {conditions_str}
         AND `tabCustomer`.`tax_id` IS NOT NULL
          GROUP BY 
              `tabCustomer`.`name`
      ) AS vols
          ON vols.`quantity_in_tons` BETWEEN `tabExport Volume Categories`.`from_volume` AND `tabExport Volume Categories`.`to_volume`
             WHERE
    `tabExport Volume Categories`.`name` IS NOT NULL
      {con_str}
           AND `tabExport Volume Categories`.`name` IS NOT NULL
      ORDER BY 
          vols.`quantity_in_tons` DESC
          {limit_clause}
        ;
        """

      
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
            "export_volume_categories": fields["export_volume_categories"]
        
        },as_dict=True,)

        
        mydata_sorted = sorted(mydata, key=lambda x: x['quantity_in_tons'], reverse=True)
        return mydata

  
        
