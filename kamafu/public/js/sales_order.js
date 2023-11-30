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
    },
    before_save: function(frm) {
        if (frm.doc.items) {
            for (var i = 0; i < frm.doc.items.length; i++) {
                update_tax(frm, frm.doc.items[i].doctype, frm.doc.items[i].name);
            }
            compile_sales_taxes(frm);
        }
    }
});

frappe.ui.form.on('Sales Order Item', {
    item_code: function(frm, cdt, cdn) {
        if (locals[cdt][cdn].item_code) {
            set_sales_tax_rate(frm, cdt, cdn);
        }
    },
    base_net_amount: function(frm, cdt, cdn) {
        update_tax(frm, cdt, cdn);
    },
    tax_rate: function(frm, cdt, cdn) {
        update_tax(frm, cdt, cdn);
    }
});

function create_akonto(frm) {
    frappe.model.open_mapped_doc({
        'method': 'kamafu.kamafu.utils.create_akonto',
        'frm': frm
    });
}
