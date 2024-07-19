frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
        frm.add_custom_button(__("Assign Seat"), function(){
            frappe.prompt(
                [
                    {
                        fieldname: 'seat_number',
                        label: 'Seat Number',
                        fieldtype: 'Data',
                        reqd: 1
                    }
                ],
                function(values){
                    const seat_number = values.seat_number;
                    const seat_format = /^[1-9][0-9]?[A-E]$/; // Format: 1-99 followed by A-E
                    if (!seat_format.test(seat_number)) {
                        frappe.msgprint(__('Invalid seat number format. Format should be 1-99 followed by A-E.'));
                        return;
                    }
                    frm.set_value('seat', values.seat_number);
                    frm.save();
                },
                __('Assign Seat'),
                __('Assign')
            );
        }, __("Actions"));
	},
});
