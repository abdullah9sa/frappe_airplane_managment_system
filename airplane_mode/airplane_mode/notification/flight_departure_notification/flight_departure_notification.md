

<table class="panel-body" border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr height="12"></tr>
    <tr>
        <td width="15"></td>
        <td>
            <div>
                <p>Flight Departure Details :</p>
                <ul class="list-unstyled" style="line-height: 1.7">
                    <li><b>{{_("Flight")}}: </b>{{ doc.flight }}</li>
                    <li><b>{{_("Departure Date")}}: </b>{{ frappe.utils.formatdate(doc.date_of_departure) }}</li>
                    <li><b>{{_("Time of Departure")}}: {{doc.time_of_departure}}</b> </li>
                    <li><b>{{doc.source_airport}}->{{doc.destination_airport_code}}</b> </li>
                    
                </ul>
            </div>
        </td>
    </tr>
</table>