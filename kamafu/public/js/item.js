/*
 * 
 * Script extensions for item
 * 
 */
 
frappe.ui.form.on('Item', {
    refresh(frm) {
        if (frm.doc.__islocal) {
            get_item_code();
        }
    }
});

function get_item_code() {
    frappe.call({
        'method': 'kamafu.kamafu.utils.get_next_item_code',
        'callback': function(response) {
            cur_frm.set_value("item_code", response.message);
        }
    });
}
