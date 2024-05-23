import frappe
from frappe import _
    
@frappe.whitelist(allow_guest=True)
def add_country(cluster_name, country_name):
    try:
        # Retrieve the cluster document
        cluster_doc = frappe.get_doc("Geographical Clusters List", cluster_name)
        
        # Check if the country already exists in the list
        country_exists = False
        for x in cluster_doc.blocs_of_targeted_countries:
            if x.country == country_name:
                country_exists = True
                break
        
        if not country_exists:
            # If country doesn't exist, append it to the list
            cluster_doc.append("blocs_of_targeted_countries", {"country": country_name})
            cluster_doc.save()
            frappe.msgprint(_("Country {} added to cluster {} successfully").format(country_name, cluster_name))
        else:
            frappe.msgprint(_("Country {} already exists in cluster {}").format(country_name, cluster_name))
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Failed to add country to cluster"))
        frappe.throw(_("Failed to add country to cluster: {}").format(str(e)))
