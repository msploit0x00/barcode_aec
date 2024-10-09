import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    return [
        {
            "label": _("Current Budget"),
            "fieldname": "budget",
            "fieldtype": "Link",
            "options": "Budget",
            "width": 250,
        },
        # {"label": _("Budget Against"), "fieldname": "budget_against", "fieldtype": "Data", "width": 250},
        # {"label": _("Monthly Distribution"), "fieldname": "monthly_distribution", "fieldtype": "Data", "width": 250},
        {
            "label": _("Fiscal Year"),
            "fieldname": "fiscal_year",
            "fieldtype": "Data",
            "width": 250,
        },
        {
            "label": _("Expense Account"),
            "fieldname": "expense_account",
            "fieldtype": "Data",
            "width": 250,
        },
        {
            "label": _("Total Amount"),
            "fieldname": "amount",
            "fieldtype": "Data",
            "width": 250,
        },
        {
            "label": _("January"),
            "fieldname": "january",
            "fieldtype": "Float",
            "width": 100,
        },
        {
            "label": _("February"),
            "fieldname": "february",
            "fieldtype": "Float",
            "width": 100,
        },
        {"label": _("March"), "fieldname": "march", 
        "fieldtype": "Float",
            "width": 100,},
        {"label": _("April"), "fieldname": "april", 
         "fieldtype": "Float",
            "width": 100,},
        {"label": _("May"), "fieldname": "may", 
         "fieldtype": "Float",
            "width": 100,},
        {"label": _("June"), "fieldname": "june", 
         "fieldtype": "Float",
            "width": 100,},
        {"label": _("July"), "fieldname": "july", 
         "fieldtype": "Float",
            "width": 100,},
        {"label": _("August"), "fieldname": "august",
         "fieldtype": "Float",
            "width": 100,},
        {
            "label": _("September"),
            "fieldname": "september",
           "fieldtype": "Float",
            "width": 100,
        },
        {
            "label": _("October"),
            "fieldname": "october",
          "fieldtype": "Float",
            "width": 100,
        },
        {
            "label": _("November"),
            "fieldname": "november",
            "fieldtype": "Data",
            "width": 90,
        },
        {
            "label": _("December"),
            "fieldname": "december",
           "fieldtype": "Float",
            "width": 100,
        },
    ]


def get_data(filters):
    result = []
    current_budget = filters.get("current_budget")
    previous_budget = filters.get("previous_budget")

    if current_budget:
        # Query for current budget
        data1 = frappe.db.sql(
            """
            SELECT B.name AS budget, budget_against, 
            B.monthly_distribution,
            B.fiscal_year,
            BA.account AS expense_account,
            BA.budget_amount AS amount,
            MAX(CASE WHEN mdp.month = 'January' THEN mdp.percentage_allocation*  BA.budget_amount /100 ELSE 0 END) AS january,
			MAX(CASE WHEN mdp.month = 'February' THEN mdp.percentage_allocation*  BA.budget_amount /100 ELSE 0 END) AS february,
			MAX(CASE WHEN mdp.month = 'March' THEN mdp.percentage_allocation*  BA.budget_amount /100 ELSE 0 END) AS march,
			MAX(CASE WHEN mdp.month = 'April' THEN mdp.percentage_allocation*  BA.budget_amount /100 ELSE 0 END) AS april,
			MAX(CASE WHEN mdp.month = 'May' THEN mdp.percentage_allocation*  BA.budget_amount /100 ELSE 0 END) AS may,
			MAX(CASE WHEN mdp.month = 'June' THEN mdp.percentage_allocation*  BA.budget_amount /100 ELSE 0 END) AS june,
			MAX(CASE WHEN mdp.month = 'July' THEN mdp.percentage_allocation*  BA.budget_amount /100 ELSE 0 END) AS july,
			MAX(CASE WHEN mdp.month = 'August' THEN mdp.percentage_allocation*  BA.budget_amount /100 ELSE 0 END) AS august,
			MAX(CASE WHEN mdp.month = 'September' THEN mdp.percentage_allocation*  BA.budget_amount /100 ELSE 0 END) AS september,
			MAX(CASE WHEN mdp.month = 'October' THEN mdp.percentage_allocation*  BA.budget_amount /100 ELSE 0 END) AS october,
			MAX(CASE WHEN mdp.month = 'November' THEN mdp.percentage_allocation*  BA.budget_amount /100 ELSE 0 END) AS november,
			MAX(CASE WHEN mdp.month = 'December' THEN mdp.percentage_allocation*  BA.budget_amount /100 ELSE 0 END) AS december 
            FROM `tabBudget` AS B
            INNER JOIN `tabBudget Account` AS BA ON B.name = BA.parent
            INNER JOIN `tabMonthly Distribution Percentage` AS mdp
            ON mdp.parent =  B.monthly_distribution
            WHERE B.docstatus = 1 AND B.name = %s
            group BY B.name,BA.account;
        """,
            (current_budget),
            as_dict=True,
        )

        # Append color info for data1 (red)
        for row in data1:
            row["color"] = "#c7dcfc"
        result.extend(data1)

    if previous_budget:
        # Query for previous budget
        data2 = frappe.db.sql(
            """
           SELECT 
    B.name AS budget, 
    B.budget_against, 
    B.monthly_distribution, 
    B.fiscal_year, 
    BA.account AS expense_account,  -- Only one expense_account field
    BA.budget_amount AS amount,
    
    -- Monthly distribution based on percentage allocation
    MAX(CASE WHEN mdp.month = 'january' THEN mdp.percentage_allocation * BA.budget_amount / 100 ELSE 0 END) AS january,
    MAX(CASE WHEN mdp.month = 'february' THEN mdp.percentage_allocation * BA.budget_amount / 100 ELSE 0 END) AS february,
    MAX(CASE WHEN mdp.month = 'March' THEN mdp.percentage_allocation * BA.budget_amount / 100 ELSE 0 END) AS march,
    MAX(CASE WHEN mdp.month = 'April' THEN mdp.percentage_allocation * BA.budget_amount / 100 ELSE 0 END) AS april,
    MAX(CASE WHEN mdp.month = 'May' THEN mdp.percentage_allocation * BA.budget_amount / 100 ELSE 0 END) AS may,
    MAX(CASE WHEN mdp.month = 'June' THEN mdp.percentage_allocation * BA.budget_amount / 100 ELSE 0 END) AS june,
    MAX(CASE WHEN mdp.month = 'July' THEN mdp.percentage_allocation * BA.budget_amount / 100 ELSE 0 END) AS july,
    MAX(CASE WHEN mdp.month = 'August' THEN mdp.percentage_allocation * BA.budget_amount / 100 ELSE 0 END) AS august,
    MAX(CASE WHEN mdp.month = 'September' THEN mdp.percentage_allocation * BA.budget_amount / 100 ELSE 0 END) AS september,
    MAX(CASE WHEN mdp.month = 'October' THEN mdp.percentage_allocation * BA.budget_amount / 100 ELSE 0 END) AS october,
    MAX(CASE WHEN mdp.month = 'November' THEN mdp.percentage_allocation * BA.budget_amount / 100 ELSE 0 END) AS november,
    MAX(CASE WHEN mdp.month = 'December' THEN mdp.percentage_allocation * BA.budget_amount / 100 ELSE 0 END) AS december 

FROM `tabBudget` AS B
INNER JOIN `tabBudget Account` AS BA ON B.name = BA.parent
INNER JOIN `tabMonthly Distribution Percentage` AS mdp ON mdp.parent = B.monthly_distribution
WHERE B.docstatus IN (0, 2) 
AND B.name = %s
group BY B.name, BA.account;

        """,
            (previous_budget),
            as_dict=True,
        )

        # Append color info for data2 (green)
        for row in data2:
            row["color"] = "#fcc7c7"
        result.extend(data2)

    return result
