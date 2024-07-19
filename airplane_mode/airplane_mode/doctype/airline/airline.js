// Copyright (c) 2024, Abdullah Salih and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
    refresh(frm) {
        var link = frm.doc.website;
        if (link != null && link != "") {
            frm.add_web_link("www.google.com");
        }

    },
});
