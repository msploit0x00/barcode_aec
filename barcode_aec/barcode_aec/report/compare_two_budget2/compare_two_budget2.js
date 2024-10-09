// Copyright (c) 2024, ds and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Compare Two Budget2"] = {
	// Copyright (c) 2024, ds and contributors
// For license information, please see license.txt
/* eslint-disable */
	"filters": [
		{
            label: __("Current Budget"),
            fieldname: "current_budget",
            fieldtype: "Link",
            options: "Budget",
            width: 150,
            get_query: function (report) {
                return {
                    filters: [["Budget", "docstatus", "=", "1"]],
                };
            },
        },
        {	
            label: __("Previous Budget"),
            fieldname: "previous_budget",
            fieldtype: "Link",
            options: "Budget",
            width: 150,
            get_query: function (report) {
                return {
                    filters: [["Budget", "docstatus", "!=", "1"]]
                };
            },
        }
	],
	"formatter": function(value, row, column, data, default_formatter) {
        // Call the default formatter first
        value = default_formatter(value, row, column, data);
        
        // Apply background color based on the data.color property
        if (data && data.color) {
            // Setting background color
            return `<div style="background-color: ${data.color};">${value}</div>`;
        }

        return value;
    },

};
