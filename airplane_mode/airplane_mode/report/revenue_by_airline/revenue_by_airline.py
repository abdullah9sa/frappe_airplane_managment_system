import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(), get_data()
    
    # Calculate total revenue (without adding a total row)
    total_revenue = sum([d['revenue'] for d in data])

    # Adding a summary section
    summary = [{'label': _('Total Revenue'), 'value': total_revenue}]

    # Add a chart for revenue distribution by airlines
    chart = {
        'data': {
            'labels': [d['airline'] for d in data],
            'datasets': [{
                'values': [d['revenue'] for d in data]
            }]
        },
        'type': 'donut',
    }

    return columns, data, None, chart, summary

def get_columns():
    return [
        {'fieldname': 'airline', 'label': _('Airline'), 'fieldtype': 'Link', 'options': 'Airline', 'width': 150},
        {'fieldname': 'revenue', 'label': _('Revenue'), 'fieldtype': 'Currency', 'width': 120}
    ]

def get_data():
    airlines = frappe.get_all('Airline', fields=['name'])
    data = []
    for airline in airlines:
        revenue = frappe.db.sql("""
            SELECT SUM(ticket.total_amount) AS revenue
            FROM `tabAirplane Ticket` AS ticket
            JOIN `tabAirplane Flight` AS flight ON ticket.flight = flight.name
            JOIN `tabAirplane` AS airplane ON flight.airplane = airplane.name
            WHERE airplane.airline = %s
        """, airline.name, as_dict=True)[0].revenue or 0
        data.append({'airline': airline.name, 'revenue': revenue})

    return data
