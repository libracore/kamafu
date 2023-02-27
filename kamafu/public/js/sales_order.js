// Copyright (c) 2021-2023, libracore AG and contributors
// For license information, please see license.txt
        
frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {

        if (frm.doc.docstatus === 1) {
            // add create akonto function
            frm.add_custom_button(__("Anzahlungsrechnung"),  function() { 
                create_akonto(frm);
            }, __("Create"));
            // remove obsolete menu items
            setTimeout(function() {
                $("a[data-label='" + encodeURI(__("Pick List")) + "']").parent().remove();
                $("a[data-label='" + encodeURI(__("Work Order")) + "']").parent().remove();
                $("a[data-label='" + encodeURI(__("Material Request")) + "']").parent().remove();
                $("a[data-label='" + encodeURI(__("Request for Raw Materials")) + "']").parent().remove();
                $("a[data-label='" + encodeURI(__("Purchase Order")) + "']").parent().remove();
                $("a[data-label='" + encodeURI(__("Project")) + "']").parent().remove();
                $("a[data-label='" + encodeURI(__("Subscription")) + "']").parent().remove();
                $("a[data-label='" + encodeURI(__("Payment Request")) + "']").parent().remove();
            }, 1000);
        }
    }
});

function create_akonto(frm) {
    frappe.model.open_mapped_doc({
        'method': 'kamafu.kamafu.utils.create_akonto',
        'frm': frm
    });
}
