import frappe
from frappe import _
from frappe.utils import now, today

@frappe.whitelist()
def make_journal_entry():
    docs = frappe.get_all("Treasury bills")
    setting1 = frappe.db.get_single_value('Treasury bill setting', 'baio1')
    setting2 = frappe.db.get_single_value('Treasury bill setting', 'baio2')
    setting3 = frappe.db.get_single_value('Treasury bill setting', 'baio3')
    setting4 = frappe.db.get_single_value('Treasury bill setting', 'baio4')
    setting5 = frappe.db.get_single_value('Treasury bill setting', 'due_returns')
    setting6 = frappe.db.get_single_value('Treasury bill setting', 'taxes_owed')
    for doc in docs:
        Treasury_bill = frappe.get_doc("Treasury bills", doc.name)
        table = Treasury_bill.payment_schedule
        for row in table:
            print(row.entry_date, today())  # Print entry date and current date
            if today() == str(row.entry_date):
                print("Ok.....")
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
                    ]
                })
                journal_entry.insert()
                journal_entry.submit()

                # Update the payment schedule row with the journal entry reference
                frappe.db.set_value('Payment', row.name, 'journal_entry', journal_entry.name)
                frappe.db.set_value('Treasury bills', doc.name,'make_entry', 1)

            else:
                print("Not Ok.....")
