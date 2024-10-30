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
    
#     if result['action'] == 'warn':
#         return result['message']
#     elif result['action'] == 'ignore':
#         frappe.msgprint(result['message'])
#     elif result['action'] == 'continue':
#         pass
