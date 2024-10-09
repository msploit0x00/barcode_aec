import frappe
from frappe.utils import now_datetime, today

def cron():
    print("HIiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    setting1 = frappe.db.get_single_value('Treasury bill setting', 'baio1')
    setting2 = frappe.db.get_single_value('Treasury bill setting', 'baio2')
    setting3 = frappe.db.get_single_value('Treasury bill setting', 'baio3')
    setting4 = frappe.db.get_single_value('Treasury bill setting', 'baio4')
    setting5 = frappe.db.get_single_value('Treasury bill setting', 'due_returns')
    setting6 = frappe.db.get_single_value('Treasury bill setting', 'taxes_owed')
    # Fetch the single Treasury bill setting document
    docs = frappe.get_all("Treasury bills")
    # # # Get the current time in 'HH:MM' format
    current_time = now_datetime().strftime('%H:%M:%S')
    print("HIiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    # # # Extract the time in 'HH:MM' format from doc.time, assuming doc.time is stored as 'HH:MM:SS'
    for doc in docs:
        Treasury_bill = frappe.get_doc("Treasury bills", doc.name)
        table = Treasury_bill.payment_schedule
        print("Treasury_bill",table)
        for row in table:
            print("Row",row)  # Print entry date and current date
            # if today() == str(row.entry_date):
            print("Dayessss",row.dayes) 
            print(today()) # Print entry date and current date
            journal_entry = frappe.get_doc({
                'doctype': 'Journal Entry',
                'posting_date': today(),
                'accounts': [
                    {
                        "account": setting5,
                        "credit": row.earned_return,
                        "against_account": setting3,
                        "credit_in_account_currency": row.earned_return,
                    },
                    {
                        "account": setting3,
                        "debit": row.earned_return,
                        "against_account": setting5,
                        "debit_in_account_currency": row.earned_return,
                    },
                    {
                        "account": setting6,
                        "credit": row.tax_on_return,
                        "against_account": setting4,
                        "credit_in_account_currency": row.tax_on_return,
                    },
                    {
                        "account": setting4,
                        "debit": row.tax_on_return,
                        "against_account": setting6,
                        "debit_in_account_currency": row.tax_on_return,
                    },
                ] })
            journal_entry.insert(ignore_permissions=True)
            journal_entry.submit()

                # Update the payment schedule row with the journal entry reference
        frappe.db.set_value('Payment', row.name, 'journal_entry', journal_entry.name)
        print(doc.name)
        frappe.db.set_value('Treasury bills', doc.name,'make_entry', 1)
        print("Ok.....")

            # else:
            #     print("Not Ok.....")









