import frappe
from frappe import _
from io import BytesIO
import base64
import barcode
from barcode.writer import ImageWriter
from datetime import datetime, timedelta
from redis import Redis
from redis.lock import Lock
from datetime import datetime
from frappe import enqueue


@frappe.whitelist()
def generate_barcode(first, sec, third):
    try:
        code128 = barcode.get_barcode_class('code128')
        result = f"{first}-{sec}-{third}"
        barcode_instance = code128(result, writer=ImageWriter())

        temp = BytesIO()
        barcode_instance.save(temp)
        temp.seek(0)

        b64 = base64.b64encode(temp.read())
        final =  "data:image/png;base64,{0}".format(b64.decode("utf-8"))
        return final
    except Exception as e:
        frappe.log_error("Error generating barcode: {}".format(str(e)))
        return None

@frappe.whitelist()
def get_material_request_data(cost_center,transaction_year):
    data = frappe.db.sql("""
       SELECT
            mr.material_request_type AS `Baio`,
            YEAR(mr.transaction_date) AS transaction_year,                     
            mri.expense_account,
            SUM(mri.amount) AS total_amount
        FROM
            `tabMaterial Request` AS mr
        LEFT JOIN
            `tabMaterial Request Item` AS mri ON mr.name = mri.parent
        WHERE
            mr.material_request_type = 'Budget' AND
            mr.docstatus = 1 AND
            mri.custom_status = 'تم الموافقة' AND
            mr.custom_cost_center = %s AND
            YEAR(mr.transaction_date) = %s
        GROUP BY
            mr.material_request_type,
            mri.expense_account
        """, (cost_center,transaction_year), as_dict=1)

    return data


@frappe.whitelist(allow_guest=True)
def create_journal_entry(treasury_bills):
    try:
        treasury_bills_doc = frappe.get_doc('Treasury bills', treasury_bills)
        purchase_date = treasury_bills_doc.purchase_date

        if not purchase_date:
            return _("Purchase date not found in Treasury Bills")
        purchase_date_dt = datetime.strptime(str(purchase_date), '%Y-%m-%d').date()
        current_date_dt = datetime.now().date()
#        if purchase_date_dt != current_date_dt:
#            return {"message": _("The purchase date is not today. Cannot create a Journal Entry.")}

        treasury_bills_setting = frappe.get_doc('Treasury bill setting', None)
        baio1_account = treasury_bills_setting.baio1 
        baio2_account = treasury_bills_setting.baio2 
        baio3_account = treasury_bills_setting.baio3 

        if not baio1_account or not baio2_account or not baio3_account:
            return _("Treasury Bills accounts not found in settings")

        nominal_value = treasury_bills_doc.nominal_value
        purchasing_value = treasury_bills_doc.purchasing_value
        grand_nominal_value = treasury_bills_doc.grand_nominal_value
        return_value = grand_nominal_value - purchasing_value

        new_journal_entry = frappe.get_doc({
            'doctype': 'Journal Entry',
            'posting_date': purchase_date,
            'accounts': [
                {
                    'account': baio1_account,
                    'debit_in_account_currency': grand_nominal_value,
                    'credit_in_account_currency': 0,
                },
                {
                    'account': baio2_account,
                    'debit_in_account_currency': 0,
                    'credit_in_account_currency': purchasing_value,
                },
                {
                    'account': baio3_account,
                    'debit_in_account_currency': 0,
                    'credit_in_account_currency': return_value,
                }
            ],
            'custom_reference_type': 'Treasury bills',
            'custom_reference_name': treasury_bills ,
            'voucher_type': 'Journal Entry'
        })

        new_journal_entry.insert()
        treasury_bills_doc.bidding_status = 'قيد التنفيذ'
        treasury_bills_doc.save()
        frappe.db.commit()
        return {
            'message': _('Journal Entry created successfully'),
            'journal_entry_name': new_journal_entry.name
        }

    except Exception as e:
        frappe.local.response['http_status_code'] = 500
        return _("An error occurred"), e



##################################################################################
@frappe.whitelist(allow_guest=True)
def journal_entry_due_date_1(treasury_bills):
    try:
        treasury_bills_doc = frappe.get_doc('Treasury bills', treasury_bills)
        due_date = treasury_bills_doc.due_date

        if not due_date:
            return _("Due date not found in Treasury Bills")
        due_date_dt = datetime.strptime(str(due_date), '%Y-%m-%d').date()
        current_date_dt = datetime.now().date()
#        if due_date_dt != current_date_dt:
#            return {"message": _("The due date is not today. Cannot create a Journal Entry.")}
        
        treasury_bills_setting = frappe.get_doc('Treasury bill setting', None)
        baio1_account = treasury_bills_setting.baio1 
        baio2_account = treasury_bills_setting.baio2 

        if not baio1_account or not baio2_account:
                return _("Treasury Bills accounts not found in settings")

        nominal_value = treasury_bills_doc.nominal_value
        grand_nominal_value = treasury_bills_doc.grand_nominal_value

        new_journal_entry = frappe.get_doc({
                'doctype': 'Journal Entry',
                'posting_date': due_date,
                'accounts': [
                    {
                        'account': baio2_account,
                        'debit_in_account_currency': grand_nominal_value,
                        'credit_in_account_currency': 0,
                    },
                    {
                        'account': baio1_account,
                        'debit_in_account_currency': 0,
                        'credit_in_account_currency': grand_nominal_value,
                    },
                ],
                'custom_reference_type': 'Treasury bills',
                'custom_reference_name': treasury_bills ,
                'voucher_type': 'Journal Entry'
            })

        new_journal_entry.insert()
        new_journal_entry.save()
        frappe.db.commit()
        return {
                'message': _('Journal Entry created successfully'),
                'journal_entry_name': new_journal_entry.name
            }

    except Exception as e:
        frappe.local.response['http_status_code'] = 500
        return _("An error occurred"), e

    
# ##################################################################################
@frappe.whitelist(allow_guest=True)
def journal_entry_due_date_2(treasury_bills):
    try:
        treasury_bills_doc = frappe.get_doc('Treasury bills', treasury_bills)
        due_date = treasury_bills_doc.due_date

        if not due_date:
            return _("Due date not found in Treasury Bills")
        due_date_dt = datetime.strptime(str(due_date), '%Y-%m-%d').date()
        current_date_dt = datetime.now().date()
#        if due_date_dt != current_date_dt:
#            return {"message": _("The due date is not today. Cannot create a Journal Entry.")}

        treasury_bills_setting = frappe.get_doc('Treasury bill setting', None)
        baio4_account = treasury_bills_setting.baio4 
        baio2_account = treasury_bills_setting.baio2 

        if not baio4_account or not baio2_account :
           return _("Treasury Bills accounts not found in settings")
        tax = treasury_bills_doc.tax
        new_journal_entry = frappe.get_doc({
            'doctype': 'Journal Entry',
            'posting_date': due_date,
            'accounts': [
                {
                    'account': baio4_account,
                    'debit_in_account_currency': tax,
                    'credit_in_account_currency': 0,
                },
                {
                    'account': baio2_account,
                    'debit_in_account_currency': 0,
                    'credit_in_account_currency': tax,
                },
            ],
            'custom_reference_type': 'Treasury bills',
            'custom_reference_name': treasury_bills,
            'voucher_type': 'Journal Entry'
        })

        new_journal_entry.insert()
        new_journal_entry.save()
        frappe.db.commit()

        return {
            'message': _('Journal Entry created successfully'),
            'journal_entry_name': new_journal_entry.name
        }

    except Exception as e:
        frappe.local.response['http_status_code'] = 500
        return _("An error occurred"), e
# #################################################################
@frappe.whitelist(allow_guest=True)
def journal_entry_due_date_3(treasury_bills):
    try:
        treasury_bills_doc = frappe.get_doc('Treasury bills', treasury_bills)
        due_date = treasury_bills_doc.due_date

        if not due_date:
            return _("Due date not found in Treasury Bills")
        due_date_dt = datetime.strptime(str(due_date), '%Y-%m-%d').date()
        current_date_dt = datetime.now().date()
#        if due_date_dt != current_date_dt:
#            return {"message": _("The due date is not today. Cannot create a Journal Entry.")}

        treasury_bills_setting = frappe.get_doc('Treasury bill setting', None)
        baio3_account = treasury_bills_setting.baio3 
        baio5_account = treasury_bills_setting.baio5 

        if not baio3_account or not baio5_account :
            return _("Treasury Bills accounts not found in settings")
        nominal_value = treasury_bills_doc.nominal_value
        purchasing_value = treasury_bills_doc.purchasing_value
        return_value = grand_nominal_value - purchasing_value


        new_journal_entry = frappe.get_doc({
            'doctype': 'Journal Entry',
            'posting_date': due_date,
            'accounts': [
                {
                    'account': baio3_account,
                    'debit_in_account_currency': return_value,
                    'credit_in_account_currency': 0,
                },
                {
                    'account': baio5_account,
                    'debit_in_account_currency': 0,
                    'credit_in_account_currency': return_value,
                },
            ],
            'custom_reference_type': 'Treasury bills',
            'custom_reference_name': treasury_bills,
            'voucher_type': 'Journal Entry'
        })

        new_journal_entry.insert()
        new_journal_entry.save()
        frappe.db.commit()

        return {
            'message': _('Journal Entry created successfully'),
            'journal_entry_name': new_journal_entry.name
        }

    except Exception as e:
        frappe.local.response['http_status_code'] = 500
        return _("An error occurred"), e


##########################
def on_submit(doc, method):
    if doc.doctype == 'Treasury bills':
        enqueue_create_journal_entry(doc.name)
        enqueue_journal_entry_due_date_1(doc.name)
        enqueue_journal_entry_due_date_2(doc.name)
        enqueue_journal_entry_due_date_3(doc.name)





# #########################
@frappe.whitelist()
def enqueue_create_journal_entry(treasury_bills):
    frappe.enqueue('barcode_aec.barcode.create_journal_entry', treasury_bills=treasury_bills)

@frappe.whitelist()
def enqueue_journal_entry_due_date_1(treasury_bills):
    frappe.enqueue('barcode_aec.barcode.journal_entry_due_date_1', treasury_bills=treasury_bills)


@frappe.whitelist()
def enqueue_journal_entry_due_date_2(treasury_bills):
    frappe.enqueue('barcode_aec.barcode.journal_entry_due_date_2', treasury_bills=treasury_bills)

@frappe.whitelist()
def enqueue_journal_entry_due_date_3(treasury_bills):
    frappe.enqueue('barcode_aec.barcode.journal_entry_due_date_3', treasury_bills=treasury_bills)






def format_date(date):
    year = date.year
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)
    return f"{year}-{month}-{day}"

@frappe.whitelist()
def getValidation(customer, due_date, name):
    today = datetime.strptime(due_date, "%Y-%m-%d")
    first_date = datetime(today.year, 1, 1)
    last_date = datetime(today.year + 1, 1, 1) - timedelta(days=1)
    formatted_first_date = format_date(first_date)
    formatted_last_date = format_date(last_date)
    
    invoice_list = frappe.get_list(
        doctype="Sales Invoice",
        filters={
            "customer": customer,
            "due_date": ["between", [formatted_first_date, formatted_last_date]],
            "custom_annual_fees": ["is", "set"],
        },
    )

    table = []
    

    for invoice in invoice_list:
        temp = frappe.db.get_value("Sales Invoice", invoice.name, ['status'])
        table.append(temp)

    print(table)

    if not table:
        test = 0
        frappe.db.set_value("Sales Invoice", name, "custom_membership_status", "Unpaid yet")
    else:
        for i in table:
            if i == 'Paid':
                test = 1
                frappe.db.set_value("Sales Invoice", name, "custom_membership_status", "Paid")
            else:
                test = 0
                frappe.db.set_value("Sales Invoice", name, "custom_membership_status", "Unpaid yet")

    return test








@frappe.whitelist()
def getCustomers(com):
    customers = frappe.db.sql("""

        SELECT
    `tabCustomer`.customer_name AS customer_name,
    `tabCustomer`.custom_customer_status AS customer_status,
    `tabCustomer`.custom_email AS custom_email,
    `tabCustomer`.custom_name_of_the_cioowner_of_the_company AS ceo_name,
    `tabCommittees you would like to join`.committees
FROM
    `tabCustomer`
JOIN
    `tabCommittees you would like to join` ON `tabCustomer`.name = `tabCommittees you would like to join`.parent
WHERE
    `tabCommittees you would like to join`.committees = %s
   AND `tabCustomer`.custom_customer_status = 'Active';

""",(com,), as_dict=1)
    
    return customers






@frappe.whitelist()
def getActiveMembers(com):
     active = frappe.db.sql("""

    SELECT
    COUNT(*) AS total_count
FROM
    tabCustomer c
JOIN
    `tabCommittees you would like to join` cc ON c.name = cc.parent
WHERE
    c.custom_customer_status = 'Active'
    AND cc.committees = %s;



""",(com,), as_dict=1)
     return active





@frappe.whitelist()
def getTotalMembers(com):
     total = frappe.db.sql("""

    SELECT
    COUNT(*) AS total_count
FROM
    tabCustomer c
JOIN
    `tabCommittees you would like to join` cc ON c.name = cc.parent
WHERE
    cc.committees = %s;



""",(com,), as_dict=1)
     return total






@frappe.whitelist()
def getInactiveMembers(com):
     inactive = frappe.db.sql("""

    SELECT
    COUNT(*) AS total_count
FROM
    tabCustomer c
JOIN
    `tabCommittees you would like to join` cc ON c.name = cc.parent
WHERE
   c.custom_customer_status IN ('Suspended', 'Inactive')             
  AND  cc.committees = %s;



""",(com,), as_dict=1)
     return inactive









@frappe.whitelist(allow_guest=True)
def create_fetch(doc_name):
    try:
        meeting_doc = frappe.get_doc('Meeting', doc_name)
        committee = meeting_doc.committee
        location = meeting_doc.location
        subject = meeting_doc.subject.encode('utf-8')[:140].decode('utf-8')
        date = meeting_doc.date
        from_time = meeting_doc.from_time
        to_time = meeting_doc.to_time

        quality_meeting_agenda = frappe.get_all(
            "Quality Meeting Agenda",
            filters={"parent": doc_name},
            fields=["agenda"]
        )
        
        committee_members = frappe.get_all(
            "Committee Members",
            filters={"parent": doc_name},
            fields=["member", "status","name1"]
        )
        
        external_authorities = frappe.get_all(
            "External Authority",
            filters={"parent": doc_name},
            fields=["name1", "email", "phone_number"]
        )

        council_entities = frappe.get_all("council entities",
                                          filters={"parent":doc_name},
                                          fields=["entity","designation","email","phone","status"])

        new_minutes = frappe.get_doc({
            'doctype': 'Minutes Of Meeting',
            'committee': committee,
            'location': location,
            'subject': subject,
            'date': date,
            'from_time': from_time,
            'to_time': to_time,
	    'custom_meeting_reference': doc_name,
        })

        for agenda_item in quality_meeting_agenda:
            new_minutes.append('meeting_agenda', {'agenda': agenda_item['agenda']})

        for member in committee_members:
            new_minutes.append('committee_member', {'member': member['member'], 'status': member['status'],'custom_ceo_name':member['name1']})

        for authority in external_authorities:
            new_minutes.append('external_authority', {'name1': authority['name1'], 'email': authority['email'], 'phone_number': authority['phone_number']})

        for council in council_entities:
            new_minutes.append('custom_council_entities',{'entity':council['entity'],'designation':council['designation'],'email':council['email'],'phone':council['phone'],'status':council['status']})    

        new_minutes.insert()

        return new_minutes.name
    except Exception as e:
        frappe.log_error(f"Error creating Minutes Of Meeting: {e}")
        frappe.throw("Error creating Minutes Of Meeting")








@frappe.whitelist()
def check_location_exists(location):
    exists = frappe.db.exists({
        'doctype': 'Meeting', 
        'location': location
    })

    return {
        'exists': exists
    }







@frappe.whitelist()
def check_date_exists(date, location, from_time=None, to_time=None):
    filters = {
        'date': date,
        'location': location,
    }

    if from_time is not None and to_time is not None:
        filters.update({
            'from_time': ['<=', to_time],
            'to_time': ['>=', from_time],
        })

    existing_meetings = frappe.get_all(
        'Meeting',
        filters=filters,
        fields=['name', 'from_time', 'to_time']
    )

    conflicting_meetings = []

    for meeting in existing_meetings:
        conflicting_meetings.append({
            'name': meeting['name'],
            'from_time': meeting['from_time'],
            'to_time': meeting['to_time']
        })

    if conflicting_meetings:
        return {
            'exists': True,
            'message': f"Conflicting meetings found for {date} at {location} between {from_time} and {to_time}.",
            'conflicting_meetings': conflicting_meetings
        }

    return {
        'exists': False
    }



############################################################
@frappe.whitelist(allow_guest=True)
def get_meeting_plan_count(committee):
    try:
        meeting_plans = frappe.get_all('Annual Meeting Plan', filters={'docstatus': 1,'custom_year':datetime.now().year},fields=['name'])

        count_by_committee = {}
        for meeting_plan in meeting_plans:
            committees = frappe.get_all('Annual Meeting Plane Table',
                                        filters={'parent': meeting_plan.name},
                                        fields=['committe'])
            for committee_data in committees:
                committee_name = committee_data.get('committe')
                if committee and committee_name == committee:
                    count_by_committee[committee_name] = count_by_committee.get(committee_name, 0) + 1
                elif not committee:
                    count_by_committee[committee_name] = count_by_committee.get(committee_name, 0) + 1


        return {
            'count_by_committee': count_by_committee
        }

    except Exception as e:
        frappe.log_error(f"Error in get_meeting_plan_count: {str(e)}")
        return {
            'error': _('An error occurred while processing the request.')
        }

###########################################################

@frappe.whitelist(allow_guest=True)
def get_meeting_count(committee1):
    try:
        count = frappe.db.count('Meeting', filters={'committee': committee1, 'docstatus': 1,'custom_year': datetime.now().year})

        return {'count_by_committee': {committee1: count}}  

    except Exception as e:
        frappe.log_error(f"Error in get_meeting_count: {str(e)}")
        return {'error': _('An error occurred while processing the request.')}
















@frappe.whitelist()
def getValidation2 (customer , due_date ):

    due_date_datetime = datetime.strptime(due_date, "%Y-%m-%d")
    first_day_of_year = datetime(due_date_datetime.year, 1, 1).strftime("%Y-%m-%d")
    last_day_of_year = datetime(due_date_datetime.year, 12, 31).strftime("%Y-%m-%d")

    invoices = frappe.db.sql("""
        SELECT
            si.name AS `name`,
            si.status AS `status`, 
            si.custom_product_bundle AS `custom_product_bundle`,
	        si.custom_annual_fees AS `custom_annual_fees`,
            si.custom_service_group AS `custom_service_group`,
            sii.item_code AS `item_code`
        FROM
            `tabSales Invoice` AS si
        LEFT JOIN
            `tabSales Invoice Item` AS sii 
        ON 
            si.name = sii.parent
        WHERE
            si.customer = %s
            AND si.due_date BETWEEN %s AND %s;
     """, (customer, first_day_of_year , last_day_of_year), as_dict=1)
    
    return invoices









@frappe.whitelist()
def files (name):
    doc_data = frappe.get_doc("Sales Invoice" , name)

    custom_registration_number_in_commercial_register_attachment = doc_data.custom_registration_number_in_commercial_register_attachment 
    custom_start_date = doc_data.custom_start_date
    end_date = doc_data.custom_end_date

    custom_registration_number_in_exporter_register_attachment = doc_data.custom_registration_number_in_exporter_register_attachment
    custom_starte_datee = doc_data.custom_starte_datee
    custom_end_datee = doc_data.custom_end_datee

    custom_tax_id = doc_data.custom_tax_id
    custom_start_date_of_tax = doc_data.custom_start_date_of_tax
    custom_end_date_of_tax = doc_data.custom_end_date_of_tax

    createAttachFile(name ,custom_registration_number_in_commercial_register_attachment ,  'custom_registration_number_in_commercial_register_attachment')
    frappe.db.set_value("Customer" , doc_data.customer , 'custom_registration_number_in_commercial_register_attachment' , custom_registration_number_in_commercial_register_attachment)
    frappe.db.set_value("Customer" , doc_data.customer , 'custom_date_of_registration' , custom_start_date)
    frappe.db.set_value("Customer" , doc_data.customer , 'custom_even_valid' , end_date)

    createAttachFile(name ,custom_registration_number_in_exporter_register_attachment ,  'custom_registration_number_in_exporter_register_attachment')
    frappe.db.set_value("Customer" , doc_data.customer , 'custom_registration_number_in_exporter_register_attachment' , custom_registration_number_in_exporter_register_attachment)
    frappe.db.set_value("Customer" , doc_data.customer , 'custom_date_of_registration2' , custom_starte_datee)
    frappe.db.set_value("Customer" , doc_data.customer , 'custom_even_valid2' , custom_end_datee)

    createAttachFile(name ,custom_tax_id ,  'custom_tax_card_number_attachment')
    frappe.db.set_value("Customer" , doc_data.customer , 'custom_even_valid4' , custom_end_date_of_tax)
    frappe.db.set_value("Customer" , doc_data.customer , 'custom_tax_card_number_attachment' , custom_tax_id)
    frappe.db.set_value("Customer" , doc_data.customer , 'custom_date_registration4' , custom_start_date_of_tax)

    doc_data.save()



def createAttachFile(name, field, attached_to_field):
    doc_data = frappe.get_doc("Sales Invoice", name)
    file_name = frappe.db.get_list("File", filters={
        "attached_to_docType": "Sales Invoice",
        "attached_to_field": field,
        "attached_to_name": name,
    })

    if file_name:
        file_data = frappe.get_doc("File", file_name[0].name)

        log = frappe.new_doc("File")
        log.file_name = file_data.file_name
        log.is_private = 0
        log.file_size = file_data.file_size
        log.file_url = file_data.file_url
        log.attached_to_docType = "Customer"
        log.attached_to_name = doc_data.customer
        log.attached_to_field = attached_to_field
        log.insert(ignore_permissions=True)
        frappe.db.commit()
    else:
        print("No file found for the given filters.")










@frappe.whitelist()
def get_volume_last_year(tax_id):
    data = frappe.db.sql("""
        SELECT
        	`season__name` AS `season_name`,
            `season` AS `season`,
            SUM(`total_amount_in_egp`) AS `total`,
	    SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
	    SUM(`quantity_in_tons`) AS `quantity_in_tons`

        FROM
            `tabVolume Of Member Exports`
        WHERE 
            `tax__number` = %s
            AND YEAR(`posring_date`) = YEAR(CURDATE()) - 1
        GROUP BY
            `season`;
        """, (tax_id,), as_dict=1)

    return data

@frappe.whitelist()
def get_volume_last_two_year(tax_id):
    data = frappe.db.sql("""
        SELECT
        `season__name` AS `season_name`,
            `season` AS `season`,
            SUM(`total_amount_in_egp`) AS `total`,
	    SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
	    SUM(`quantity_in_tons`) AS `quantity_in_tons`

        FROM
            `tabVolume Of Member Exports`
        WHERE 
            `tax__number` = %s
            AND YEAR(`posring_date`) = YEAR(CURDATE()) - 2
        GROUP BY
            `season`;
        """, (tax_id,), as_dict=1)

    return data

@frappe.whitelist()
def get_volume_last_three_year(tax_id):
    data = frappe.db.sql("""
        SELECT
        	`season__name` AS `season_name`,
            `season` AS `season`,
            SUM(`total_amount_in_egp`) AS `total`,
	    SUM(`total_amount_in_usd`) AS `total_amount_in_usd`,
	    SUM(`quantity_in_tons`) AS `quantity_in_tons`
        FROM
            `tabVolume Of Member Exports`
        WHERE 
            `tax__number` = %s
            AND YEAR(`posring_date`) = YEAR(CURDATE()) - 3
        GROUP BY
            `season`;
        """, (tax_id,), as_dict=1)

    return data
        
        
@frappe.whitelist()
def get_customer_group(value):
    data = frappe.db.sql("""
        SELECT
            `name`,
            `custom_from`,
            `custom_to`
        FROM
            `tabCustomer Group`
        WHERE 
            %s BETWEEN `custom_from` AND `custom_to`
        """, (value), as_dict=1)

    return data






@frappe.whitelist()
def get_log():
    data = frappe.db.sql("""
        SELECT
    v.season AS `season`,
    SUM(v.total_amount_in_egp) AS `total`,
    SUM(v.quantity_in_tons) AS `quantity_in_tons`,
    SUM(v.total_amount_in_usd) AS `total_amount_in_usd`,
    c.customer_name AS `customer_name`,
    c.name AS `name`,
    v.tax__number AS `tax__number`,
    c.customer_group AS `customer_group`,
    c.custom_volume_of__exports AS `volume_of_exports`
FROM
    `tabVolume Of Member Exports` AS v
JOIN
    `tabCustomer` AS c ON v.tax__number = c.tax_id
WHERE 
    YEAR(v.posring_date) = YEAR(CURDATE()) - 1
GROUP BY
    `tax__number`;
        """, (), as_dict=1)

    return data
   









@frappe.whitelist()
def update_vol (name):
    log = frappe.get_all(
        doctype="Log",
        filters={"parent": name},
        fields=["member_name", "tax_id", "member_category", "current_volume_of_exports" , "new_volume_of_member_exports" , "new_member_category" , "total_amount_in_usd" , "quantity_in_tons"]
    )
    for i in log:
        frappe.db.set_value('Customer', i.member_name , 'customer_group', i.new_member_category)
        frappe.db.set_value('Customer', i.member_name , 'custom_volume_of__exports', i.new_volume_of_member_exports)
        customer = frappe.get_doc("Customer" , i.member_name)
        customer.get("volume_of_member_exports_for_three_years").clear()
        temp1 = get_volume_last_year(i.tax_id)
        if temp1 is not None:
            customer.append("volume_of_member_exports_for_three_years",{
                "season" : temp1[0]['season'],
                "value" : temp1[0]['total'],
                "quantity_in_tons": temp1[0]['quantity_in_tons'],
                "total_amount_in_usd": temp1[0]['total_amount_in_usd']
            })
        temp2 = get_volume_last_two_year(i.tax_id)
        if temp2 is not None:
                customer.append("volume_of_member_exports_for_three_years",{
                "season" : temp2[0]['season'],
                "value" : temp2[0]['total'],
                "quantity_in_tons": temp2[0]['quantity_in_tons'],
                "total_amount_in_usd": temp2[0]['total_amount_in_usd']
            })
        temp3  = get_volume_last_three_year(i.tax_id)
        if temp3 is not None:
            customer.append("volume_of_member_exports_for_three_years",{
                "season" : temp3[0]['season'],
                "value" : temp3[0]['total'],
                "quantity_in_tons": temp3[0]['quantity_in_tons'],
                "total_amount_in_usd": temp3[0]['total_amount_in_usd']
            })
        customer.save()




@frappe.whitelist()
def get_all_customer():
    data = frappe.db.sql("""
        SELECT
    	   *
	FROM
    	   `tabCustomer`
        """, as_dict=1)

    return data





