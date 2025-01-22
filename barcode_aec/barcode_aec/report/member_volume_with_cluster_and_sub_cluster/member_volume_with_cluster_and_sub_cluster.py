import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    columns = [
        {
            "label": _("Geographical Clusters Name"),
            "fieldname": "geographical_clusters_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Sub Cluster"),
            "fieldname": "sub_cluster",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Country In Arabic"),
            "fieldname": "country_in_arabic",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Quantity In Tons Season 1"),
            "fieldname": "quantity_in_tons_season1",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": _("Total Amount In EGP Season 1"),
            "fieldname": "total_amount_in_egp_season1",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Total Amount In USD Season 1"),
            "fieldname": "total_amount_in_usd_season1",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Quantity In Tons Season 2"),
            "fieldname": "quantity_in_tons_season2",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": _("Total Amount In EGP Season 2"),
            "fieldname": "total_amount_in_egp_season2",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Total Amount In USD Season 2"),
            "fieldname": "total_amount_in_usd_season2",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Difference In Quantity In Tons"),
            "fieldname": "difference_in_quantity_in_tons",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": _("Difference In Total Amount In EGP"),
            "fieldname": "difference_in_total_amount_in_egp",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Difference In Total Amount In USD"),
            "fieldname": "difference_in_total_amount_in_usd",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Percentage Change In Quantity In Tons"),
            "fieldname": "percentage_change_in_quantity_in_tons",
            "fieldtype": "Percent",
            "width": 150
        },
        {
            "label": _("Percentage Change In Total Amount In EGP"),
            "fieldname": "percentage_change_in_total_amount_in_egp",
            "fieldtype": "Percent",
            "width": 150
        },
        {
            "label": _("Percentage Change In Total Amount In USD"),
            "fieldname": "percentage_change_in_total_amount_in_usd",
            "fieldtype": "Percent",
            "width": 150
        }
    ]
    return columns




def get_data(filters):
    # Extract the selected seasons from filters
    selected_season1 = filters.get("season1")
    selected_season2 = filters.get("season2")

    # Fetch data using Frappe ORM
    data = frappe.get_all(
        "Volume Of Member Exports",
        fields=[
            "country_code",
            "country_in_arabic",
            "season",
            "quantity_in_tons",
            "total_amount_in_egp",
            "total_amount_in_usd"
        ],
        filters={"season": ["in", [selected_season1, selected_season2]]},
        debug=True
    )
    

    # Dictionary to store aggregated data
    aggregated_data = {}

    # Process the data to group by geographical_clusters_name, sub_cluster, and country_in_arabic
    for entry in data:
        # Fetch geographical_clusters_name and sub_cluster for the country
        country_details = frappe.get_all(
            "Countries",
            filters={"name": entry.country_code},
            fields=["geographical_clusters_name", "sub_cluster"],
        )

        for count in country_details:
            geographical_clusters_name = count.get("geographical_clusters_name")
            sub_cluster = count.get("sub_cluster")
            country_in_arabic = entry.get("country_in_arabic")

            # Create a unique key for grouping
            key = (geographical_clusters_name, sub_cluster, country_in_arabic)

            # Initialize the dictionary for the key if it doesn't exist
            if key not in aggregated_data:
                aggregated_data[key] = {
                    "geographical_clusters_name": geographical_clusters_name,
                    "sub_cluster": sub_cluster,
                    "country_in_arabic": country_in_arabic,
                    "quantity_in_tons_season1": 0,
                    "total_amount_in_egp_season1": 0,
                    "total_amount_in_usd_season1": 0,
                    "quantity_in_tons_season2": 0,
                    "total_amount_in_egp_season2": 0,
                    "total_amount_in_usd_season2": 0,
                }

            # Add the data to the respective season
            if entry.get("season") == selected_season1:
                aggregated_data[key]["quantity_in_tons_season1"] += float(entry.get("quantity_in_tons", 0))
                aggregated_data[key]["total_amount_in_egp_season1"] += float(entry.get("total_amount_in_egp", 0))
                aggregated_data[key]["total_amount_in_usd_season1"] += float(entry.get("total_amount_in_usd", 0))
            elif entry.get("season") == selected_season2:
                aggregated_data[key]["quantity_in_tons_season2"] += float(entry.get("quantity_in_tons", 0))
                aggregated_data[key]["total_amount_in_egp_season2"] += float(entry.get("total_amount_in_egp", 0))
                aggregated_data[key]["total_amount_in_usd_season2"] += float(entry.get("total_amount_in_usd", 0))

    # Convert the aggregated data into a list
    processed_data = list(aggregated_data.values())

    # Calculate differences and percentages
    for entry in processed_data:
        entry["difference_in_quantity_in_tons"] = entry["quantity_in_tons_season1"] - entry["quantity_in_tons_season2"]
        entry["difference_in_total_amount_in_egp"] = entry["total_amount_in_egp_season1"] - entry["total_amount_in_egp_season2"]
        entry["difference_in_total_amount_in_usd"] = entry["total_amount_in_usd_season1"] - entry["total_amount_in_usd_season2"]

        if entry["quantity_in_tons_season2"] != 0:
            entry["percentage_change_in_quantity_in_tons"] = (entry["difference_in_quantity_in_tons"] / entry["quantity_in_tons_season2"]) * 100
        else:
            entry["percentage_change_in_quantity_in_tons"] = None

        if entry["total_amount_in_egp_season2"] != 0:
            entry["percentage_change_in_total_amount_in_egp"] = (entry["difference_in_total_amount_in_egp"] / entry["total_amount_in_egp_season2"]) * 100
        else:
            entry["percentage_change_in_total_amount_in_egp"] = None

        if entry["total_amount_in_usd_season2"] != 0:
            entry["percentage_change_in_total_amount_in_usd"] = (entry["difference_in_total_amount_in_usd"] / entry["total_amount_in_usd_season2"]) * 100
        else:
            entry["percentage_change_in_total_amount_in_usd"] = None

    return processed_data

# def get_data(filters):
#     # Extract the selected seasons from filters
#     selected_season1 = filters.get("season1")
#     selected_season2 = filters.get("season2")

#     # Fetch data using Frappe ORM
#     data = frappe.get_all(
#         "Volume Of Member Exports",
#         fields=[
#             "country_code",
#             "country_in_arabic",
#             "season",
#             "quantity_in_tons",
#             "total_amount_in_egp",
#             "total_amount_in_usd"
#         ],
#         filters={"season": ["in", [selected_season1, selected_season2]]},
#         debug=True
#     )

#     # Dictionary to store aggregated data
#     aggregated_data = {}

#     # Process the data to group by geographical_clusters_name, sub_cluster, and country_in_arabic
#     for entry in data:
#         # Fetch geographical_clusters_name and sub_cluster for the country
#         country_details = frappe.get_all(
#             "Countries",
#             filters={"name": entry.country_code},
#             fields=["geographical_clusters_name", "sub_cluster"],
#         )

#         for count in country_details:
#             geographical_clusters_name = count.get("geographical_clusters_name")
#             sub_cluster = count.get("sub_cluster")
#             country_in_arabic = entry.get("country_in_arabic")

#             # Create a unique key for grouping
           

#             # Initialize the dictionary for the key if it doesn't exist
           
#             aggregated_data = {
#                     "geographical_clusters_name": geographical_clusters_name,
#                     "sub_cluster": sub_cluster,
#                     "country_in_arabic": country_in_arabic,
#                     "quantity_in_tons_season1": 0,
#                     "total_amount_in_egp_season1": 0,
#                     "total_amount_in_usd_season1": 0,
#                     "quantity_in_tons_season2": 0,
#                     "total_amount_in_egp_season2": 0,
#                     "total_amount_in_usd_season2": 0,
#                 }

#             # Add the data to the respective season
#             if entry.get("season") == selected_season1:
#                 aggregated_data["quantity_in_tons_season1"] += float(entry.get("quantity_in_tons", 0))
#                 aggregated_data["total_amount_in_egp_season1"] += float(entry.get("total_amount_in_egp", 0))
#                 aggregated_data["total_amount_in_usd_season1"] += float(entry.get("total_amount_in_usd", 0))
#             elif entry.get("season") == selected_season2:
#                 aggregated_data["quantity_in_tons_season2"] += float(entry.get("quantity_in_tons", 0))
#                 aggregated_data["total_amount_in_egp_season2"] += float(entry.get("total_amount_in_egp", 0))
#                 aggregated_data["total_amount_in_usd_season2"] += float(entry.get("total_amount_in_usd", 0))

#     # Convert the aggregated data into a list
#     processed_data = list(aggregated_data.values())

#     # Calculate differences and percentages
#     for entry in processed_data:
#         entry["difference_in_quantity_in_tons"] = entry["quantity_in_tons_season1"] - entry["quantity_in_tons_season2"]
#         entry["difference_in_total_amount_in_egp"] = entry["total_amount_in_egp_season1"] - entry["total_amount_in_egp_season2"]
#         entry["difference_in_total_amount_in_usd"] = entry["total_amount_in_usd_season1"] - entry["total_amount_in_usd_season2"]

#         if entry["quantity_in_tons_season2"] != 0:
#             entry["percentage_change_in_quantity_in_tons"] = (entry["difference_in_quantity_in_tons"] / entry["quantity_in_tons_season2"]) * 100
#         else:
#             entry["percentage_change_in_quantity_in_tons"] = None

#         if entry["total_amount_in_egp_season2"] != 0:
#             entry["percentage_change_in_total_amount_in_egp"] = (entry["difference_in_total_amount_in_egp"] / entry["total_amount_in_egp_season2"]) * 100
#         else:
#             entry["percentage_change_in_total_amount_in_egp"] = None

#         if entry["total_amount_in_usd_season2"] != 0:
#             entry["percentage_change_in_total_amount_in_usd"] = (entry["difference_in_total_amount_in_usd"] / entry["total_amount_in_usd_season2"]) * 100
#         else:
#             entry["percentage_change_in_total_amount_in_usd"] = None

#     return processed_data



