import frappe




@frappe.whitelist(allow_guest=True)
def update_committee(com, emp, salutation):
    doc = frappe.get_doc('Customer', emp)

    # if com:
    #     for row in doc.custom_committees_you_would_like_to_join:
    #         if row.committees != com:
    #             frappe.throw('This Member is not joined to this')

    if salutation == 'عضوية رئيس لجنة':
        for row in doc.custom_committees_you_would_like_to_join:
            if row.committees == com and (row.salutation == 'عضوية لجنة سلعية' or row.salutation == 'عضوية لجنة خدمية'):
                row.salutation = 'عضوية رئيس لجنة'

    elif salutation == 'عضوية وكيل لجنة':
        for row in doc.custom_committees_you_would_like_to_join:
            if row.committees == com and (row.salutation == 'عضوية لجنة سلعية' or row.salutation == 'عضوية لجنة خدمية'):
                row.salutation = 'عضوية وكيل لجنة'
    # Check if the combination of committee and salutation already exists
    # existing_committees = [(row.committees, row.salutation) for row in doc.custom_committees_you_would_like_to_join]
    # if (com, salutation) in existing_committees:
        # return "Duplicate entry. This committee with the same salutation already exists."
    
    # If the combination doesn't exist, append the new row
    # doc.append('custom_committees_you_would_like_to_join', {
    #     'committees': com,
    #     'salutation': salutation
    # })

    doc.save()
    frappe.db.commit()
    return "Inserted"



@frappe.whitelist(allow_guest=True)
def validate_cust(com,cust):
    doc = frappe.get_doc('Customer', cust)
    if com:
        for row in doc.custom_committees_you_would_like_to_join:
            if row.committees != com:
                frappe.throw('This Member is not joined to this')





@frappe.whitelist(allow_guest=True)
def update_committe_after_end_perioud(customer, com, type):
    doc = frappe.get_doc('Customer',customer)
    # return doc
    for row in doc.custom_committees_you_would_like_to_join:
        # if salutation == 'عضوية وكيل لجنة':
        if type == 'مصدر':
            if row.committees == com and (row.salutation == 'عضوية وكيل لجنة' or row.salutation == 'عضوية رئيس لجنة'):
                row.salutation = 'عضوية لجنة سلعية'
        if type == 'خدمي':
            if row.committees == com and (row.salutation == 'عضوية وكيل لجنة' or row.salutation == 'عضوية رئيس لجنة'):
                row.salutation =  'عضوية لجنة خدمية'
    doc.save()
    frappe.db.commit()
    return "FIN"