// Copyright (c) 2024, ds and contributors
// For license information, please see license.txt

frappe.ui.form.on('Export Opportunities', {
	refresh: function(frm) {
    frm.add_custom_button(__('Get Selected'),function(){
      frappe.call({
        doc: frm.doc,
				method: "get_volume_exports",
				freeze: true,
				freeze_message: __("Fetching Volume Exports Data"),
      }).then((response) => {
        cur_frm.clear_table('targeted_members');
        console.log("Message",response.message )
        if (response.message) { 

          
          let msg = response.message
          
          for (let cri of msg){
            let ch = frm.add_child('targeted_members')
            ch.member_code = cri.member; 
            ch.tax_id = cri.tax_id; 
            ch.email = cri.email; 
            ch.committees = cri.committees_name; 
            ch.governorate = cri.countries; 
            ch.shipping_port = cri.shipping_port; 
            ch.customer_status = cri.custom_customer_status; 
            ch.cluster = cri.cluster; 
            ch.season = cri.season__name; 
            ch.export_value_in_egp = cri.total_amount_in_egp; 
            ch.export_value_in_usd = cri.total_amount_in_usd; 
            ch.quantity_in_tons  = cri.quantity_in_tons; 
            ch.products = cri.products;
            ch.member_name = cri.custom_name_of_the_cioowner_of_the_company;
            ch.company_name = cri.customer_name;
            ch.category_name = cri.category_name;
      
          }
          frm.refresh_field("targeted_members");
        }
      });
    })
	},
  on_submit :function(frm){
    frm.add_custom_button(__('Send to newsletter'),function(){
      let allEmails = cur_frm.doc.targeted_members
      .filter(member => member.email !== undefined) 
      .map(member => member.email);
  
      // console.log(allEmails);
      frappe.new_doc("Customer Newsletter",{
             "source":cur_frm.doctype,
             "generealiztion_id":cur_frm.doc.name
         }).then(() => {
             for (let email of allEmails) {
                 let child = cur_frm.add_child("customer_email");
                 child.email = email;
                 // frappe.db.set_value("Customer Newsletter",doc.name,"sender_email","Account")
                 cur_frm.refresh_fields("customer_email");
             }
         });
    })
  }
});
