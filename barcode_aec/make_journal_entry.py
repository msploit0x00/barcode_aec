import frappe
from frappe.utils import now_datetime, today

def cron():
    print("Cron Job Started")
    
    # Fetch settings from 'Treasury bill setting'
    setting1 = frappe.db.get_single_value('Treasury bill setting', 'baio1')
    setting2 = frappe.db.get_single_value('Treasury bill setting', 'baio2')
    setting3 = frappe.db.get_single_value('Treasury bill setting', 'baio3')
    setting4 = frappe.db.get_single_value('Treasury bill setting', 'baio4')
    setting5 = frappe.db.get_single_value('Treasury bill setting', 'due_returns')
    setting6 = frappe.db.get_single_value('Treasury bill setting', 'taxes_owed')
    
    # Fetch all 'Treasury bills' documents
    docs = frappe.get_all("Treasury bills")
    current_time = now_datetime().strftime('%H:%M:%S')

    for doc in docs:
        treasury_bill = frappe.get_doc("Treasury bills", doc.name)
        table = treasury_bill.payment_schedule
        
        for row in table:
            print(f"Processing row {row.name} from Treasury Bill {doc.name}")

            try:
                # Create a journal entry for each row without validation
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

                # Insert and submit the journal entry
                journal_entry.insert(ignore_permissions=True)
                journal_entry.submit()
                print(f"Journal Entry {journal_entry.name} created for {doc.name}")

                # Update the payment schedule row with the journal entry reference
                frappe.db.set_value('Payment', row.name, 'journal_entry', journal_entry.name)
                frappe.db.set_value('Treasury bills', doc.name, 'make_entry', 1)
                print(f"Updated Payment {row.name} with Journal Entry {journal_entry.name}")

            except Exception as e:
                print(f"Error while creating journal entry for {doc.name}: {e}")

    print("Cron Job Completed")
