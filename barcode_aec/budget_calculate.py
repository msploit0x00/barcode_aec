import frappe
from frappe.utils import getdate, add_days

@frappe.whitelist()
def get_po_totals(filters):
    results = {}

    filters = frappe.parse_json(filters)
    purchase_orders = frappe.get_all('Purchase Order', fields=['name'], filters=filters)

    if purchase_orders:
        for po in purchase_orders:
            po_items = frappe.get_all('Purchase Order Item', fields=['amount', 'expense_account'], filters={
                'parent': po.name
            })

            for item in po_items:
                expense_account = item.expense_account or ''
                amount = item.amount or 0

                if expense_account:
                    if expense_account not in results:
                        results[expense_account] = {'total_amount': 0}
                    results[expense_account]['total_amount'] += amount

    return results

@frappe.whitelist()
def get_po_totals(month, fiscal_year, expense_account, cost_center):
    sql = """
        SELECT 
            po.name AS poname, 
            po.transaction_date, 
            SUM(po.total) AS total1,
            poi.expense_account,
            SUM(poi.amount) AS total,
            poi.cost_center AS costcenter
        FROM 
            `tabPurchase Order` po
        LEFT JOIN 
            `tabPurchase Order Item` poi 
        ON 
            poi.parent = po.name
        WHERE 
            MONTH(po.transaction_date) = %(month)s
        AND YEAR(po.transaction_date) = %(fiscal_year)s    
        AND poi.expense_account = %(expense_account)s
        AND poi.cost_center = %(cost_center)s
        AND po.docstatus = '1';
            
    """
    data = frappe.db.sql(
        sql,
        {
            "month": month,
            "fiscal_year": fiscal_year,
            "expense_account": expense_account,
            "cost_center": cost_center,
        },
        as_dict=True,
    )
    return data


# @frappe.whitelist()
# def get_po_totals(filters):
#     results = {}
#     # get all PO name which are
#     filters = frappe.parse_json(filters)
#     purchase_orders = frappe.get_all(
#         "Purchase Order", limit_page_length=500000, fields=["name"], filters=filters
#     )

#     if purchase_orders:
#         for po in purchase_orders:
#             po_items = frappe.get_all(
#                 "Purchase Order Item",
#                 fields=["amount", "expense_account"],
#                 filters={"parent": po.name},
#             )

#             for item in po_items:
#                 expense_account = item.expense_account or ""
#                 amount = item.amount or 0

#                 if expense_account:
#                     if expense_account not in results:
#                         results[expense_account] = {"total_amount": 0}
#                     results[expense_account]["total_amount"] += amount

#     return results


@frappe.whitelist()
def get_budget_details(fiscal_year):
    budget_details = []

    budgets = frappe.get_all('Budget', fields=['name', 'cost_center'], filters={
        'docstatus': 1,
        'fiscal_year': fiscal_year
    })

    for budget in budgets:
        budget_doc = frappe.get_doc('Budget', budget.name)
        for account in budget_doc.accounts:
            budget_details.append({
                'account': account.account,
                'budget_amount': account.budget_amount,
                'monthly_distribution': account.monthly_distribution,
                'cost_center': budget.cost_center,
                'parent': budget.name
            })

    return budget_details

    budgets = frappe.get_all(
        "Budget",
        fields=["name", "cost_center"],
        filters={"docstatus": 1, "fiscal_year": fiscal_year},
    )

    for budget in budgets:
        budget_doc = frappe.get_doc("Budget", budget.name)
        for account in budget_doc.accounts:
            budget_details.append(
                {
                    "account": account.account,
                    "budget_amount": account.budget_amount,
                    "monthly_distribution": account.monthly_distribution,
                    "cost_center": budget.cost_center,
                    "parent": budget.name,
                }
            )

    return budget_details


@frappe.whitelist()
def get_monthly_distribution(fiscal_year, cost_center, expense_account, month):
    # return fiscal_year, cost_center, expense_account, month
    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }
    month_name = month_names.get(int(month), "Unknown Month")

    sql = """
        SELECT
            b.name AS budgetname,
            b.fiscal_year,
            b.cost_center,
            ba.account AS expense_account,
            ba.budget_amount,
            ba.custom_monthly_distribution AS MonthlyDistributionname,
            mdp.month,
            mdp.percentage_allocation,
            (mdp.percentage_allocation * ba.budget_amount/100) AS amountFormonth
        FROM
            `tabBudget` b
        LEFT JOIN
            `tabBudget Account` ba ON b.name = ba.parent
        LEFT JOIN
            `tabMonthly Distribution` md ON md.name = ba.custom_monthly_distribution
        LEFT JOIN
            `tabMonthly Distribution Percentage` mdp ON mdp.parent = md.name
        WHERE
            b.docstatus = '1'
            AND b.applicable_on_purchase_order = '1'
            AND b.fiscal_year = %(fiscal_year)s
            AND b.cost_center = %(cost_center)s
            AND ba.account = %(expense_account)s
            AND mdp.month = %(month_name)s;
    """
    data = frappe.db.sql(
        sql,
        {
            "fiscal_year": fiscal_year,
            "cost_center": cost_center,
            "expense_account": expense_account,
            "month_name": month_name,
        },
        as_dict=True,
    )

    return data or [
        {"message": "No distribution data found for the selected parameters."}
    ]


# @frappe.whitelist()
# def get_po_totals(filters):
#     results = {}
#     # get all PO name which are
#     filters = frappe.parse_json(filters)
#     purchase_orders = frappe.get_all(
#         "Purchase Order", limit_page_length=500000, fields=["name"], filters=filters
#     )

#     if purchase_orders:
#         for po in purchase_orders:
#             po_items = frappe.get_all(
#                 "Purchase Order Item",
#                 fields=["amount", "expense_account"],
#                 filters={"parent": po.name},
#             )

#             for item in po_items:
#                 expense_account = item.expense_account or ""
#                 amount = item.amount or 0

#                 if expense_account:
#                     if expense_account not in results:
#                         results[expense_account] = {"total_amount": 0}
#                     results[expense_account]["total_amount"] += amount

#     return results

# def get_monthly_distribution(transaction_date, po_totals):
#     allocated_amounts = []

#     fiscal_year = getdate(transaction_date).year
#     budget_details = get_budget_details(fiscal_year)

#     month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#     po_month = getdate(transaction_date)
#     current_month_index = po_month.month - 1  # Zero-based index

#     for budget in budget_details:
#         monthly_dist = frappe.get_doc('Monthly Distribution', budget['monthly_distribution'])
#         for row in monthly_dist.percentages:
#             if row.month == month_list[current_month_index]:
#                 allocated_amount = (row.percentage_allocation * budget['budget_amount']) / 100
#                 total_amount = po_totals.get(budget['account'], {}).get('total_amount', 0)
#                 allocated_amounts.append({
#                     'account': budget['account'],
#                     'cost_center': budget['cost_center'],
#                     'budget_monthly': allocated_amount,
#                     'total_amount': total_amount,
#                     'parent': budget['parent']
#                 })

#     return allocated_amounts
# def handle_workflow_action(filters):
#     po_totals = get_po_totals(filters)
#     allocated_amounts = get_monthly_distribution(filters.get('transaction_date'), po_totals)

#     for row in allocated_amounts:
#         budget = frappe.get_doc('Budget', row['parent'])
#         applicable = budget.applicable_on_purchase_order
#         action = budget.custom_action_if__monthly_budget_exceeded_on_po

#         for item in frappe.get_all('Purchase Order Item', fields=['amount', 'expense_account', 'cost_center'], filters={
#             'parenttype': 'Purchase Order',
#             'parent': row['parent']
#         }):
#             if applicable == 1:
#                 if action == "Warn" and row['account'] == item.expense_account and row['cost_center'] == item.cost_center and item['amount'] + row['total_amount'] > row['budget_monthly']:
#                     return {
#                         'message': f"Are you sure you want to Save?\n\nMonthly Budget: {row['budget_monthly']} Total Amount: {row['total_amount']} For Account: {row['account']} It will exceed by {item['amount']}",
#                         'action': 'warn'
#                     }
#                 elif action == "Stop" and row['total_amount'] > row['budget_monthly']:
#                     raise frappe.ValidationError(f"Budget exceeded:\n\nMonthly Budget: {row['budget_monthly']} Total Amount: {row['total_amount']} For Account: {row['account']} Action is set to Stop.")
#                 elif action == "Ignore":
#                     return {
#                         'message': f"Monthly Budget: {row['budget_monthly']} Total Amount: {row['total_amount']} For Account: {row['account']}",
#                         'action': 'ignore'
#                     }

#     return {'action': 'continue'}
# def get_monthly_distribution(transaction_date, po_totals):
#     if not transaction_date:
#         frappe.log_error("Transaction date is None")
#         return []  # Return an empty list or handle it appropriately

#     allocated_amounts = []
#     fiscal_year = 2024
#     budget_details = get_budget_details(fiscal_year)

#     month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#     po_month = getdate(transaction_date)
#     current_month_index = po_month.month - 1  # Zero-based index

#     for budget in budget_details:
#         monthly_dist = frappe.get_doc('Monthly Distribution', budget['monthly_distribution'])
#         for row in monthly_dist.percentages:
#             if row.month == month_list[current_month_index]:
#                 allocated_amount = (row.percentage_allocation * budget['budget_amount']) / 100
#                 total_amount = po_totals.get(budget['account'], {}).get('total_amount', 0)
#                 allocated_amounts.append({
#                     'account': budget['account'],
#                     'cost_center': budget['cost_center'],
#                     'budget_monthly': allocated_amount,
#                     'total_amount': total_amount,
#                     'parent': budget['parent']
#                 })

#     return allocated_amounts

# @frappe.whitelist()
# def after_workflow_action(docname, transaction_date, filters):
#     filters = frappe.parse_json(filters)  # Parse filters from JSON
#     if not transaction_date:
#         frappe.throw(_("Transaction date is required"))
    
#     doc = frappe.get_doc('Purchase Order', docname)
#     result = handle_workflow_action(filters)
    

#     doc = frappe.get_doc('Purchase Order', docname)
#     result = handle_workflow_action(filters)

#     if result['action'] == 'warn':
#         return result['message']
#     elif result['action'] == 'ignore':
#         frappe.msgprint(result['message'])
#     elif result['action'] == 'continue':
#         pass
