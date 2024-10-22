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
    setting7 = frappe.db.get_single_value('Treasury bill setting', 'baio5')
    # Fetch all 'Treasury bills' documents
    docs = frappe.get_all("Treasury bills")
    current_time = now_datetime().strftime('%H:%M:%S')
    # jl_names = []
    # row_name = []
    for doc in docs:
        treasury_bill = frappe.get_doc("Treasury bills", doc.name)
        table = treasury_bill.payment_schedule
        
        for row in table:
            #  if today() == str(row.entry_date):
                print(f"Processing row {row.name} from Treasury Bill {doc.name}")

                try:
                    # Create a journal entry for each row without validation
                    journal_entry = frappe.get_doc({
                        'doctype': 'Journal Entry',
                        'posting_date': row.entry_date,
                        'accounts': [
                            {
                                "account": setting5,
                                "debit": row.earned_return,
                                "against_account": setting3,
                                "debit_in_account_currency": row.earned_return,
                            },
                            {
                                "account": setting7,
                                "credit": row.earned_return,
                                "against_account": setting5,
                                "credit_in_account_currency": row.earned_return,
                            },
                            {
                                "account": setting4,
                                "debit": row.tax_on_return,
                                "against_account": setting4,
                                "debit_in_account_currency": row.tax_on_return,
                            },
                            {
                                "account": setting6,
                                "credit": row.tax_on_return,
                                "against_account": setting6,
                                "credit_in_account_currency": row.tax_on_return,
                            },
                        ]
                    })

                    # Insert and submit the journal entry
                    journal_entry.insert(ignore_permissions=True)
                    journal_entry.save()
                    frappe.db.commit()
                    # journal_entry.submit()
                    print(f"Journal Entry {journal_entry.name} created for {doc.name}")

                    # Update the payment schedule row with the journal entry reference
                    frappe.db.set_value('Payment', row.name, 'journal_entry', journal_entry.name)
                    # jl_names.append(journal_entry.name)
                    frappe.db.set_value('Treasury bills', doc.name, 'make_entry', 1)

                    frappe.db.sql("""
                        UPDATE `tabPayment`
                        SET journal_entry = %s
                        WHERE name = %s
                    """, (journal_entry.name, row.name))

                    frappe.db.commit()
                    # row_name.append(row.name)
                    print(f"Updated Payment {row.name} with Journal Entry {journal_entry.name}")

                except Exception as e:
                    print(f"Error while creating journal entry for {doc.name}: {e}")
        
        # for row in row_name:
        #     for jl in jl_names:
        #         print(row)
        #     print(jl)
        #     frappe.db.set_value("Payment", row, 'journal_entry', jl)


        print("Cron Job Completed")
