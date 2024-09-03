import frappe




@frappe.whitelist()
def make_task(issue, subject, name):
    issue_assignment = frappe.get_doc('Issue Assignment', name)
    items = frappe.get_all(
        "Issue assignment  departments",filters={"parent": name},
        fields=["custom_task_link", "name", "department","employee", "custom_due_date", "notes"])
    print("items",items)   
    for row in items:
        print("rowwwwwwwwwwwwwwww",row.name)
        make_task = frappe.get_doc({
        'doctype': 'Issue Tasks',
        'issue': issue,
        'custom_subject': subject,
        'issue_assignment':name,
        'department':row.department,
        'notes':row.notes,
        'employee':row.employee,
        'custom_due_date':row.custom_due_date
        })
        make_task.insert()
        make_task.submit()
        frappe.db.set_value('Issue assignment  departments', row.name, 'custom_task_link', make_task.name)
        print("makeTaskName",make_task.name)
    

    # print("items",items)    
    
        # 
        