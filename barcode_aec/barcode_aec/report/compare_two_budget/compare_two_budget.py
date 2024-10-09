import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    return [
        {"label": _("Current Budget"), "fieldname": "budget", "fieldtype": "Link", "options": "Budget", "width": 250},
        {"label": _("Budget Against"), "fieldname": "budget_against", "fieldtype": "Data", "width": 250},
        {"label": _("Monthly Distribution"), "fieldname": "monthly_distribution", "fieldtype": "Data", "width": 250},
        {"label": _("Fiscal Year"), "fieldname": "fiscal_year", "fieldtype": "Data", "width": 250},
        {"label": _("Month"), "fieldname": "month", "fieldtype": "Data", "width": 90},
         {"label": _("Percentage Allocation"), "fieldname": "percentage_allocation", "fieldtype": "Data", "width": 200},
        {"label": _("Expense Account"), "fieldname": "expense_account", "fieldtype": "Data", "width": 250},
        {"label": _("Amount"), "fieldname": "amount", "fieldtype": "Data", "width": 250},
    ]

def get_data(filters):
    result = []
    current_budget = filters.get("current_budget")
    previous_budget = filters.get("previous_budget")

    if current_budget:
        # Query for current budget
        data1 = frappe.db.sql("""
            SELECT B.name AS budget, budget_against, 
            B.monthly_distribution, B.fiscal_year, BA.account AS expense_account, BA.budget_amount AS amount 
            ,mdp.month ,mdp.percentage_allocation
            FROM `tabBudget` AS B
            INNER JOIN `tabBudget Account` AS BA ON B.name = BA.parent
            INNER JOIN `tabMonthly Distribution Percentage` AS mdp
            ON mdp.parent =  B.monthly_distribution
            WHERE B.docstatus = 1 AND B.name = %s
            ORDER BY  CASE mdp.month
                WHEN 'January' THEN 1
                WHEN 'February' THEN 2
                WHEN 'March' THEN 3
                WHEN 'April' THEN 4
                WHEN 'May' THEN 5
                WHEN 'June' THEN 6
                WHEN 'July' THEN 7
                WHEN 'August' THEN 8
                WHEN 'September' THEN 9
                WHEN 'October' THEN 10
                WHEN 'November' THEN 11
                WHEN 'December' THEN 12
            END;
        """, (current_budget), as_dict=True)

        # Append color info for data1 (red)
        for row in data1:
            row['color'] = 'chartreuse'
        result.extend(data1)

    if previous_budget:
        # Query for previous budget
        data2 = frappe.db.sql("""
            SELECT B.name AS budget, B.budget_against, B.monthly_distribution, 
            B.fiscal_year, BA.account AS expense_account,
            BA.budget_amount AS amount,
            mdp.month ,mdp.percentage_allocation
            FROM `tabBudget` AS B
            INNER JOIN `tabBudget Account` AS BA ON B.name = BA.parent
            INNER JOIN `tabMonthly Distribution Percentage` AS mdp ON mdp.parent =  B.monthly_distribution
            WHERE B.docstatus IN (0, 2) AND B.name = %s
            ORDER BY  CASE mdp.month
                WHEN 'January' THEN 1
                WHEN 'February' THEN 2
                WHEN 'March' THEN 3
                WHEN 'April' THEN 4
                WHEN 'May' THEN 5
                WHEN 'June' THEN 6
                WHEN 'July' THEN 7
                WHEN 'August' THEN 8
                WHEN 'September' THEN 9
                WHEN 'October' THEN 10
                WHEN 'November' THEN 11
                WHEN 'December' THEN 12
            END;
        """, (previous_budget), as_dict=True)

        # Append color info for data2 (green)
        for row in data2:
            row['color'] = '#FFFF3E'
        result.extend(data2)

    return result
