// Copyright (c) 2025, ds and contributors
// For license information, please see license.txt
/* eslint-disable */





frappe.query_reports["Member volume with cluster and sub cluster"] = {
    filters: [
        {
            fieldname: "season1",
            label: __("Season 1"),
            fieldtype: "Link",
            options: "Export Season",
            reqd: 1  // Make the filter required
        },
        {
            fieldname: "season2",
            label: __("Season 2"),
            fieldtype: "Link",
            options: "Export Season",
            reqd: 1  // Make the filter required
        }
    ]
};