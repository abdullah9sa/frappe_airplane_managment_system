frappe.ui.form.on("Airport Shop", {
    refresh(frm) {
        // Add Rent Shop button
        if (!frm.doc.__islocal && !frm.doc.is_rented) {
            frm.add_custom_button(__('Rent Shop'), function() {
                rent_shop(frm);
            }, __('Actions'));
        }
        
        // Add Clear Rent button
        if (!frm.doc.__islocal && frm.doc.is_rented) {
            frm.add_custom_button(__('Clear Rent'), function() {
                clear_rent(frm);
            }, __('Actions'));
        }
    },
});

function rent_shop(frm) {
    let dialog = new frappe.ui.Dialog({
        title: __('Rent Shop'),
        fields: [
            {
                label: __('Shop Owner'),
                fieldname: 'shop_owner',
                fieldtype: 'Link',
                options: 'Shop Owner',
                reqd: 1
            },
            {
                label: __('Rent Amount'),
                fieldname: 'rent_amount',
                fieldtype: 'Currency',
                reqd: 1
            }
        ],
        primary_action_label: __('Rent'),
        primary_action(values) {
            frm.set_value('shop_owner', values.shop_owner);
            frm.set_value('rent_amount', values.rent_amount);
            frm.set_value('is_rented', 1);
            frm.save()
                .then(() => {
                    frappe.msgprint(__('Shop rented successfully.'));
                    dialog.hide();
                    frm.reload_doc();
                });
        }
    });

    dialog.show();
}

function clear_rent(frm) {
    frappe.confirm(
        __('Are you sure you want to clear the rent details for this shop?'),
        function() {
            frm.set_value('is_rented', 0);
            frm.set_value('shop_owner', null);
            frm.set_value('rent_amount', null);
            frm.set_value('valid_until', null);
            frm.save()
                .then(() => {
                    frappe.msgprint(__('Rent details cleared successfully.'));
                    frm.reload_doc();
                });
        }
    );
}
