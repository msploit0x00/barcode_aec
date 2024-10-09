// Copyright (c) 2024, ds and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Single Member Data Report2"] = {
	"filters": [
		{   
            "fieldname": "committee_name",
            "label": __("Please insert Committee"),
            "fieldtype": "Link",
            "options":"Committee",
            "width": "200px"
        
        },
        {
            fieldname: "product_name",
            label: "Please select product",
            fieldtype: "Link",
            options: "Product",
            width: "200px",  // Set the desired width for the label
        
        },
         {
            fieldname: "salutation_type",
            label: "Please select salutation type ",
            fieldtype: "Link",
            options: "Salutation",
            width: "200px",  // Set the desired width for the label
        },    
     
     {
            fieldname: "custom_customer_status",
            label: "Please select Membership Status",
            fieldtype: 'Select',
           
            options: [
                '',
                'Requested',
                'Requested From Website',
                'Active',
                'Inactive',
                'Suspended',
                'استيفاء بيانات'
            ],
            default: ''
           
        },
      
        {
            fieldname: "custom_company_type_",
            label: "Please Select Company Type ",
            fieldtype: "Link",
            options: "Company Type",
            width: "350px"
        },
        
         {
            fieldname: "custom_customer_activity_type",
            label: "Please Select customer activity type",
            fieldtype: "Link",
            options:"Customer Activity Type",
            width: "350px",
           
        },
        
        
        {
            "fieldname": "tax_id",
            "label": __("Please write Tax ID"),
            "fieldtype": "Data",
            "width": "200px"
        },
                {
            "fieldname": "registration_number_in_commercial_register",
            "label": __("Please write registration_number_in_exporter_register ID"),
            "fieldtype": "Data",
            "width": "200px"
        },
         {
             "fieldname": "customer_primary_contact",
             "label": __("Please write Contact"),
             "fieldtype": "Data",
             "width": "200px"
        },     {
             "fieldname": "email",
             "label": __("Please write Email"),
             "fieldtype": "Data",
             "width": "200px"
        },     {
             "fieldname": "name_of_the_cio/owner_of_the_company",
             "label": __("Please write CIO arabic"),
             "fieldtype": "Data",
             "width": "200px"
        },     {
             "fieldname": "name_of_the_cioowner_of_the_company_in_english",
             "label": __("Please write CIO English"),
             "fieldtype": "Data",
             "width": "200px"
        },
        {
             "fieldname": "custom_company_code",
             "label": __("Please write Company code"),
             "fieldtype": "Data",
             "width": "200px"
        },
        // You can add more filters here as per your requirement
    ],
    onload: function(report) {
        report.page.add_inner_button(__("Member Form"), function() {
            var values = report.get_values();
            var customerCode = values.custom_company_code;
            if (customerCode) {
                getCustomerID(customerCode, function(customerID) {
                    if(customerID) {
                        var print_format = 'بيانات عضو';
                        frappe.utils.print(
                        "Customer",                
                        customerCode,            
                        print_format,
                        "العربية"
                    
                );             
                    } else {
                        frappe.msgprint(__("No customer found with the code: ") + customerCode);
                    }
                });
            } else {
                frappe.msgprint(__("Please enter a customer code."));
            }
        });
    report.page.add_inner_button(__("clear filter"), function() {
        frappe.query_report.set_filter_value({
            "committee_name":"",
            "product_name":"",
            "salutation_type":"",
            "custom_customer_status":"",
            "custom_company_type_":"",
            "tax_id":"",
            "custom_customer_activity_type":"",
            "registration_number_in_commercial_register":"",
            "customer_primary_contact":"",
            "email":"",
            "name_of_the_cio/owner_of_the_company":"",
            "name_of_the_cioowner_of_the_company_in_english":"",
            "custom_company_code":"",
        });
        frappe.query_report.refresh();
    });
    },
};

function getCustomerID(customerID, callback) {
    frappe.call({
        method: "frappe.client.get",
        args: {
            "doctype":"Customer",
            "name":customerID
        },
        callback: function(r) {
            if (r.message) {
                callback(r.message);
                 var print_format = 'بيانات عضو';
                frappe.utils.print(
                    frm.doctype,                
                    frm.docname,            
                    print_format,  
                    frm.doc.letter_head,
                    "العربية"
                
                ); 
            } else{
                callback(null);
                
            }
        }
    });
}
