// your_app_name/doctype/rent_payment/rent_payment.js

frappe.ui.form.on("Rent Payment", {
    refresh(frm) {
        if (frm.doc.docstatus == 0 && !frm.is_new()) {
            frm.add_custom_button(__('Pay'), function() {
                frm.events.show_payment_method_dialog(frm);
            });
        }
    },
    show_payment_method_dialog(frm) {
        let d = new frappe.ui.Dialog({
            title: 'Select Payment Method and Enter Paid Amount',
            fields: [
                {
                    label: 'Payment Method',
                    fieldname: 'payment_method',
                    fieldtype: 'Select',
                    options: ['Cash', 'Credit card', 'Bank Transfer'],
                    reqd: 1
                },
                {
                    label: 'Paid Amount',
                    fieldname: 'paid_amount',
                    fieldtype: 'Currency',
                    default:frm.doc.payment_amount,
                    reqd: 1
                }
            ],
            primary_action_label: 'Submit',
            primary_action(values) {
                frm.events.process_payment(frm, values.payment_method, values.paid_amount);
                d.hide();
            }
        });
        d.show();
    },
    process_payment(frm, payment_method, paid_amount) {
        frappe.call({
            method: 'airplane_mode.airport_shop.doctype.rent_payment.rent_payment.process_payment',
            args: {
                docname: frm.doc.name,
                payment_method: payment_method,
                paid_amount: paid_amount
            },
            callback: function(r) {
                if (r.message) {
                    frm.reload_doc();
                }
            }
        });
    }
});
