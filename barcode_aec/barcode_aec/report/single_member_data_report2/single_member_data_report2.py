# Copyright (c) 2024, ds and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_coloumns()

	data = get_data(filters)
	return columns, data



def get_coloumns():
	return [
		{"label": _("Member"), "fieldname": "member", "fieldtype": "Link", "options": "Customer", "width": 150},
		{"label": _("Committee Name"), "fieldname": "committee_name", "fieldtype": "Link", "options": "Committee", "width": 200},
		{"label": _("Product Name"), "fieldname": "product_name", "fieldtype": "Data", "width": 150},
		{"label": _("Salutation Type"), "fieldname": "salutation_type", "fieldtype": "Data", "width": 150},
		{"label": _("Membership status"), "fieldname": "custom_customer_status", "fieldtype": "Data", "width": 150},
		{"label": _("Company Type"), "fieldname": "custom_company_type_name", "fieldtype": "Data", "width": 150},
		{"label": _("Membership Activity Type"), "fieldname": "custom_customer_activity_type", "fieldtype": "Data", "width": 150},
		{"label": _("Tax ID"), "fieldname": "tax_id", "fieldtype": "Data", "width": 200},
		{"label": _("Registration Number in Commercial Register"), "fieldname": "registration_number_in_commercial_register", "fieldtype": "Data", "width": 200},
		{"label": _("Membership Primary Contact"), "fieldname": "custom_ceo_mobile", "fieldtype": "Data", "width": 150},
		{"label": _("Email"), "fieldname": "email", "fieldtype": "Email", "width": 150},
		{"label": _("CIO Name"), "fieldname": "name_of_the_cioowner_of_the_company", "fieldtype": "Data", "width": 200},
		{"label": _("CIO Name English"), "fieldname": "name_of_the_cioowner_of_the_company_in_english", "fieldtype": "Data", "width": 200},
		{"label": _("Company Name In Arabic"), "fieldname": "company_name_in_arabic", "fieldtype": "Data", "width": 170},
		{"label": _("Company Name In English"), "fieldname": "company_name_in_english", "fieldtype": "Data", "width": 170},
		{"label": _("Company Code"), "fieldname": "custom_company_code", "fieldtype": "Data", "width": 150},
		{"label": _("Company URL"), "fieldname": "company_url", "fieldtype": "Data", "width": 150},
		{"label": _("Responsible person's name"), "fieldname": "custom_responsible_persons_name", "fieldtype": "Data", "width": 190},
		{"label": _("Responsible name English"), "fieldname": "custom_responsible_persons_name_in_english", "fieldtype": "Data", "width": 190},
		{"label": _("Registration Number in Exporter Register"), "fieldname": "registration_number_in_exporter_register", "fieldtype": "Data", "width": 200},
		{"label": _("Registration Number in Investment Letter"), "fieldname": "registration_number_in_investment_letter", "fieldtype": "Data", "width": 220},
		{"label": _("Reason for Suspending"), "fieldname": "reason_for_suspending", "fieldtype": "Data", "width": 500}
	]

def get_data(filters):

	# Get values from filters or set them to None
	tax_id = filters.get("tax_id")
	custom_company_code = filters.get("custom_company_code")
	committee_name = filters.get("committee_name")
	product_name = filters.get("product_name")
	salutation_type = filters.get("salutation_type")
	custom_customer_status = filters.get("custom_customer_status")
	custom_company_type_ = filters.get("custom_company_type_")
	custom_customer_activity_type = filters.get("custom_customer_activity_type")
	registration_number_in_commercial_register = filters.get("registration_number_in_commercial_register")
	customer_primary_contact = filters.get("customer_primary_contact")
	email = filters.get("email")
	name_of_the_cioowner_of_the_company = filters.get("name_of_the_cioowner_of_the_company")
	name_of_the_cioowner_of_the_company_in_english = filters.get("name_of_the_cioowner_of_the_company_in_english")
	#def show_report(filters=None):
	mysql = """
    SELECT
        `tabCommittees you would like to join`.`committees` AS `committee_name`,
        `tabCrops that are export`.`product` AS `product_name`,
        `tabCommittees you would like to join`.`salutation` AS `salutation_type`,
        `tabCustomer`.`custom_customer_status`,
        `tabCustomer`.`custom_company_type_name`,
        `tabCustomer`.`custom_customer_activity_type`,
        `tabCustomer`.`tax_id`,
        `tabCustomer`.`custom_registration_number_in_commercial_register` AS `registration_number_in_commercial_register`,
        `tabCustomer`.`custom_ceo_mobile` AS `custom_ceo_mobile`,
        `tabCustomer`.`custom_email` AS `email`,
        `tabCustomer`.`custom_name_of_the_cioowner_of_the_company` AS `name_of_the_cioowner_of_the_company`,
        `tabCustomer`.`custom_name_of_the_cioowner_of_the_company_in_english` AS `name_of_the_cioowner_of_the_company_in_english`,
        `tabCustomer`.`custom_company_code` AS `custom_company_code`,
        `tabCustomer`.`name` AS `member`,
        `tabCustomer`.`customer_name` AS `company_name_in_arabic`,
        `tabCustomer`.`custom_customer_name_in_english` AS `company_name_in_english`,
        `tabCustomer`.`custom_company_url` AS `company_url`,
        `tabCustomer`.`custom_responsible_persons_name` AS `custom_responsible_persons_name`,
        `tabCustomer`.`custom_responsible_persons_name_in_english` AS `custom_responsible_persons_name_in_english`,
        `tabCustomer`.`custom_date_of_registration` AS `date_of_registration`,
        `tabCustomer`.`custom_even_valid` AS `even_valid`,
        `tabCustomer`.`custom_registration_number_in_exporter_register` AS `registration_number_in_exporter_register`,
        `tabCustomer`.`custom_date_of_registration2` AS `date_of_registration2`,
        `tabCustomer`.`custom_even_valid2` AS `even_valid2`,
        `tabCustomer`.`custom_registration_number_in_investment_letter` AS `registration_number_in_investment_letter`,
        `tabCustomer`.`custom_date_registration3` AS `date_registration3`,
        `tabCustomer`.`custom_even_valid3` AS `even_valid3`,
        `tabCustomer`.`custom_date_registration4` AS `date_registration4`,
        `tabCustomer`.`custom_even_valid4` AS `even_valid4`,
        `tabCustomer`.`custom_customer_status` AS `customer_status`,
        group_concat(`tabCustomer Validation`.`reason` separator ' , ')  AS `reason_for_suspending`
        
    FROM
        `tabCustomer`
    left join `tabCustomer Validation`
    on `tabCustomer Validation`.`parent` = `tabCustomer`.`name`
    LEFT JOIN `tabCommittees you would like to join`
        ON `tabCommittees you would like to join`.`parent` = `tabCustomer`.`name`  
    LEFT JOIN `tabCrops that are export`
        ON `tabCrops that are export`.`parent` = `tabCustomer`.`name`    
    WHERE
        (%(tax_id)s IS NULL OR `tabCustomer`.`tax_id` LIKE %(tax_id)s)
        AND (%(committee_name)s IS NULL OR `tabCommittees you would like to join`.`committees` LIKE %(committee_name)s)
        AND (%(product_name)s IS NULL OR `tabCrops that are export`.`product` LIKE %(product_name)s)
        AND (%(salutation_type)s IS NULL OR `tabCommittees you would like to join`.`salutation` LIKE %(salutation_type)s)
        AND (%(custom_customer_status)s IS NULL OR `tabCustomer`.`custom_customer_status` LIKE %(custom_customer_status)s)
        AND (%(custom_company_type_)s IS NULL OR `tabCustomer`.`custom_company_type_` LIKE %(custom_company_type_)s)
        AND (%(custom_customer_activity_type)s IS NULL OR `tabCustomer`.`custom_customer_activity_type` LIKE %(custom_customer_activity_type)s)
        AND (%(registration_number_in_commercial_register)s IS NULL OR `tabCustomer`.`custom_registration_number_in_commercial_register` LIKE %(registration_number_in_commercial_register)s)
        AND  (%(customer_primary_contact)s IS NULL OR `tabCustomer`.`customer_primary_contact` LIKE %(customer_primary_contact)s) 
        AND (%(email)s IS NULL OR `tabCustomer`.`custom_email` LIKE %(email)s)
        AND (%(name_of_the_cioowner_of_the_company)s IS NULL OR `tabCustomer`.`custom_name_of_the_cioowner_of_the_company` LIKE %(name_of_the_cioowner_of_the_company)s)
        AND (%(name_of_the_cioowner_of_the_company_in_english)s IS NULL OR  `tabCustomer`.`custom_name_of_the_cioowner_of_the_company_in_english` LIKE %(name_of_the_cioowner_of_the_company_in_english)s)
        AND (%(custom_company_code)s IS NULL OR `tabCustomer`.`custom_company_code` LIKE %(custom_company_code)s)
            group by member;
"""

   
	mydata = frappe.db.sql(
    mysql,
    {
        "tax_id": f"%{tax_id}%" if tax_id else None,
        "custom_company_code": f"%{custom_company_code}%" if custom_company_code else None,    
        "committee_name": f"%{committee_name}%" if committee_name else None,   
        "product_name": f"%{product_name}%" if product_name else None,
        "salutation_type": f"%{salutation_type}%" if salutation_type else None,
        "custom_customer_status": f"%{custom_customer_status}%" if custom_customer_status else None,
        "custom_company_type_": f"%{custom_company_type_}%" if custom_company_type_ else None,
        "custom_customer_activity_type": f"%{custom_customer_activity_type}%" if custom_customer_activity_type else None,
        "registration_number_in_commercial_register": f"%{registration_number_in_commercial_register}%" if registration_number_in_commercial_register else None,
        "customer_primary_contact": f"%{customer_primary_contact}%" if customer_primary_contact else None,
        "email": f"%{email}%" if email else None,
        "name_of_the_cioowner_of_the_company": f"%{name_of_the_cioowner_of_the_company}%" if name_of_the_cioowner_of_the_company else None,
        "name_of_the_cioowner_of_the_company_in_english": f"%{name_of_the_cioowner_of_the_company_in_english}%" if name_of_the_cioowner_of_the_company_in_english else None,
          
    },
    as_dict=True)
	return mydata
 	


