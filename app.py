import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy_financial as npf

# External stylesheets for dark mode
external_stylesheets = [dbc.themes.DARKLY]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define CSS styles
styles = {
    'modal-body': {
        'maxHeight': '70vh',
        'overflowY': 'auto'
    },
    'input-group': {
        'marginBottom': '15px'
    },
    'table': {
        'backgroundColor': 'black',
        'color': 'white',
        'fontSize': '14px'
    },
    'table-header': {
        'backgroundColor': 'black',
        'color': 'white'
    },
    'table-container': {
        'maxHeight': '600px',
        'overflowY': 'auto'
    }
}

# Custom CSS to style table headers
custom_css = """
    .table thead th {
        background-color: black !important;
        color: white !important;
    }
"""

app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Home Ownership Costs Calculator</title>
        <link rel="stylesheet" href="{external_stylesheets[0]}">
        <style>{custom_css}</style>
    </head>
    <body>
        <div id="react-entry-point">
            <div class="_dash-loading">
                Loading...
            </div>
        </div>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

# Define the layout of the app
app.layout = dbc.Container(id='app-container', fluid=True, children=[
    dbc.Row(dbc.Col(html.H1('Home Ownership Costs Calculator'), width=12, className="mb-4 text-center")),

    dbc.Row(dbc.Col(dbc.Button('Enter Values', id='open-form', n_clicks=0, color="primary"), width={"size": 2, "offset": 5}, className="mb-4")),

    dbc.Modal(
        [
            dbc.ModalHeader("Input Values"),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Purchase Price"),
                        dbc.Input(id='purchase-price', type='number', placeholder='Enter Purchase Price', value=400000),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Down Payment (%)"),
                        dbc.Input(id='down-payment-percentage', type='number', placeholder='Enter Down Payment Percentage', value=0.10),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Annual Interest Rate (%)"),
                        dbc.Input(id='annual-interest-rate', type='number', placeholder='Enter Annual Interest Rate', value=0.065),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Property Tax Start"),
                        dbc.Input(id='property-tax-start', type='number', placeholder='Enter Property Tax Start', value=8000),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Tax Increase Interval"),
                        dbc.Input(id='property-tax-increase-interval', type='number', placeholder='Enter Tax Increase Interval', value=10),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Tax Increase Amount"),
                        dbc.Input(id='property-tax-increase-amount', type='number', placeholder='Enter Tax Increase Amount', value=2000),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Annual Insurance Cost"),
                        dbc.Input(id='annual-insurance-cost', type='number', placeholder='Enter Annual Insurance Cost', value=2000),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Real Estate Growth Rate (%)"),
                        dbc.Input(id='real-estate-annual-growth-rate', type='number', placeholder='Enter Real Estate Growth Rate', value=0.03),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Loan Term (Years)"),
                        dbc.Input(id='loan-term-years', type='number', placeholder='Enter Loan Term Years', value=30),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Monthly Rent"),
                        dbc.Input(id='monthly-rent', type='number', placeholder='Enter Monthly Rent', value=1350),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Monthly Rent Increase"),
                        dbc.Input(id='monthly-rent-increase', type='number', placeholder='Enter Monthly Rent Increase', value=30),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Monthly Investment"),
                        dbc.Input(id='monthly-investment', type='number', placeholder='Enter Monthly Investment', value=15000 / 12),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Investment Return Rate (%)"),
                        dbc.Input(id='investment-return-rate', type='number', placeholder='Enter Investment Return Rate', value=0.10),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Total Years"),
                        dbc.Input(id='total-years', type='number', placeholder='Enter Total Years', value=30),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Realtor Fee (%)"),
                        dbc.Input(id='realtor-fee', type='number', placeholder='Realtor Fee Percentage...', value=0.05),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Initial Rent Investment"),
                        dbc.Input(id='initial-rent-investment', type='number', placeholder='Enter Initial Rent Investment', value=1000),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Rent Increase Frequency (Years)"),
                        dbc.Input(id='rent-increase-frequency', type='number', placeholder='Enter Rent Increase Frequency', value=1),
                    ], style=styles['input-group']), width=12),
                ]),
                dbc.Row([
                    dbc.Col(dbc.InputGroup([
                        dbc.InputGroupText("Rent Increase Percentage (%)"),
                        dbc.Input(id='rent-increase-percentage', type='number', placeholder='Enter Rent Increase Percentage', value=0.05),
                    ], style=styles['input-group']), width=12),
                ]),
            ], style=styles['modal-body']),
            dbc.ModalFooter([
                dbc.Button('Submit', id='submit-form', color="primary"),
                dbc.Button('Close', id='close-form', className="ml-auto")
            ]),
        ],
        id="input-form",
        is_open=False,
    ),

    dbc.Tabs([
        dbc.Tab(label="Table View", tab_id="table", children=[html.Div(id='table-container')]),
        dbc.Tab(label="Graph View", tab_id="graph", children=[dcc.Graph(id='cost-graph', style={'height': '75vh'})])
    ], id='view-tabs', active_tab='table'),

    dbc.Row(dbc.Col(dbc.Switch(id='dark-mode-switch', label="Dark Mode", value=True), width={"size": 2, "offset": 5}, className="mb-4"))
])

@app.callback(
    Output('input-form', 'is_open'),
    [Input('open-form', 'n_clicks'), Input('close-form', 'n_clicks')],
    [State('input-form', 'is_open')]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    [Output('table-container', 'children'),
     Output('cost-graph', 'figure')],
    [Input('submit-form', 'n_clicks'),
     Input('dark-mode-switch', 'value')],
    [State('purchase-price', 'value'),
     State('down-payment-percentage', 'value'),
     State('annual-interest-rate', 'value'),
     State('property-tax-start', 'value'),
     State('property-tax-increase-interval', 'value'),
     State('property-tax-increase-amount', 'value'),
     State('annual-insurance-cost', 'value'),
     State('real-estate-annual-growth-rate', 'value'),
     State('loan-term-years', 'value'),
     State('monthly-rent', 'value'),
     State('monthly-rent-increase', 'value'),
     State('monthly-investment', 'value'),
     State('investment-return-rate', 'value'),
     State('realtor-fee', 'value'),
     State('total-years', 'value'),
     State('initial-rent-investment', 'value'),
     State('rent-increase-frequency', 'value'),
     State('rent-increase-percentage', 'value')
     ])

def update_output(n_clicks, dark_mode, purchase_price, down_payment_percentage, annual_interest_rate, property_tax_start,
                  property_tax_increase_interval, property_tax_increase_amount, annual_insurance_cost,
                  real_estate_annual_growth_rate, loan_term_years, monthly_rent, monthly_rent_increase,
                  monthly_investment, investment_return_rate, realtor_fee, total_years,
                  initial_rent_investment, rent_increase_frequency, rent_increase_percentage):
    if n_clicks > 0:
        formatted_annual_df, graph_df = calculate_home_ownership_costs(
            purchase_price,
            down_payment_percentage,
            annual_interest_rate,
            property_tax_start,
            property_tax_increase_interval,
            property_tax_increase_amount,
            annual_insurance_cost,
            real_estate_annual_growth_rate,
            loan_term_years,
            monthly_rent,
            monthly_rent_increase,
            monthly_investment,
            investment_return_rate,
            realtor_fee,
            total_years,
            initial_rent_investment,
            rent_increase_frequency,
            rent_increase_percentage
        )

        table = dbc.Table.from_dataframe(formatted_annual_df, striped=True, bordered=True, hover=True, className="sticky-header-table", style=styles['table'])
        table_container = html.Div(table, style=styles['table-container'])

        graph_layout = {
            'title': 'Financial Overview',
            'xaxis': {'title': 'Year', 'color': 'white'},
            'yaxis': {'title': 'Value', 'color': 'white'},
            'plot_bgcolor': 'black',
            'paper_bgcolor': 'black',
            'font': {'color': 'white'}
        }

        figure = {
            'data': [
                {'x': graph_df['Year'], 'y': graph_df['Cumulative Rent Paid'], 'type': 'line', 'name': 'Cumulative Rent Paid'},
                {'x': graph_df['Year'], 'y': graph_df['Net Equity'], 'type': 'line', 'name': 'Net Equity'},
                {'x': graph_df['Year'], 'y': graph_df['Investment Value'], 'type': 'line', 'name': 'Investment Value'},
                {'x': graph_df['Year'], 'y': graph_df['Total House Value'], 'type': 'line', 'name': 'Total House Value'},
                {'x': graph_df['Year'], 'y': graph_df['Cumulative Investment Rent'], 'type': 'line', 'name': 'Cumulative Investment Rent'},
            ],
            'layout': graph_layout
        }

        return table_container, figure
    return html.Div('Enter values and click calculate.', className="mt-4"), {}

# The calculate_home_ownership_costs function (implementation)
import numpy_financial as npf
import pandas as pd

def calculate_home_ownership_costs(purchase_price, down_payment_percentage, annual_interest_rate, property_tax_start,
                                   property_tax_increase_interval, property_tax_increase_amount, annual_insurance_cost,
                                   real_estate_annual_growth_rate, loan_term_years, monthly_rent, monthly_rent_increase,
                                   monthly_investment, investment_return_rate, realtor_fee_percentage, total_years=30,
                                   initial_rent_investment=1000, rent_increase_frequency=1, rent_increase_percentage=0.05):
    # Calculations
    down_payment = purchase_price * down_payment_percentage
    loan_amount = purchase_price - down_payment
    monthly_interest_rate = annual_interest_rate / 12
    number_of_payments = loan_term_years * 12
    monthly_mortgage_payment = npf.pmt(monthly_interest_rate, number_of_payments, -loan_amount)

    # Initialize variables
    remaining_balance = loan_amount
    equity = down_payment
    property_tax = property_tax_start
    home_value = purchase_price
    investment_value = 0
    monthly_investment_return_rate = (1 + investment_return_rate) ** (1/12) - 1  # Convert annual return rate to monthly

    # Create DataFrame
    monthly_data = []

    for month in range(1, total_years * 12 + 1):
        # Interest for the month
        interest_for_month = remaining_balance * monthly_interest_rate if month <= number_of_payments else 0

        # Principal payment for the month
        principal_payment = monthly_mortgage_payment - interest_for_month if month <= number_of_payments else 0

        # Update remaining balance
        remaining_balance = max(remaining_balance - principal_payment, 0)

        # Update home value annually
        if month % 12 == 0:
            home_value *= (1 + real_estate_annual_growth_rate)

        # Calculate equity
        equity = home_value - remaining_balance

        # Update investment monthly
        investment_value = investment_value * (1 + monthly_investment_return_rate) + monthly_investment

        # Update property tax at the specified interval
        if month % (property_tax_increase_interval * 12) == 0:
            property_tax += property_tax_increase_amount

        # Append to monthly_data
        monthly_data.append({
            'Month': month,
            'Interest for Month': interest_for_month,
            'Insurance for Month': annual_insurance_cost / 12 if month <= number_of_payments else 0,
            'Property Tax for Month': property_tax / 12,  # Updated to include monthly property tax
            'Total Equity': equity,
            'Investment Value': investment_value,
            'Home Value': home_value  # Track home value monthly
        })

    # Convert monthly_data to DataFrame
    df = pd.DataFrame(monthly_data)

    # Generate dynamic annual breakdown based on total_years
    years_to_display = list(range(1, loan_term_years + 1))
    annual_data = []
    graph_data = []

    for year in years_to_display:
        year_data = df[df['Month'] <= year * 12]

        total_interest_paid = year_data['Interest for Month'].sum()
        total_insurance_paid = year_data['Insurance for Month'].sum()
        total_property_tax_paid = year_data['Property Tax for Month'].sum()
        data = year_data.iloc[-1]  # Get the last month of the year
        total_house_value = data['Home Value']  # Get the home value at the end of the year
        realtor_fee = total_house_value * realtor_fee_percentage  # Calculate realtor fee
        net_equity = data['Total Equity'] - total_interest_paid - total_insurance_paid - total_property_tax_paid - realtor_fee  # Subtract realtor fee from net equity
        cumulative_rent_paid = -sum([(monthly_rent + (y - 1) * monthly_rent_increase) * 12 for y in range(1, int(year) + 1)])
        
        # Calculate cumulative investment rent
        cumulative_investment_rent = 0
        for y in range(1, int(year) + 1):
            rent_investment = initial_rent_investment * ((1 + rent_increase_percentage) ** ((y - 1) // rent_increase_frequency))
            cumulative_investment_rent += rent_investment * 12 * (1 + investment_return_rate) ** y

        annual_data.append({
            'Year': year,
            'Total House Value': total_house_value,  # Added Total House Value
            'Monthly Cost': monthly_mortgage_payment + (data['Property Tax for Month']) + (annual_insurance_cost / 12) if year <= loan_term_years else data['Property Tax for Month'],
            'Total Equity': data['Total Equity'],
            'Total Insurance Paid': total_insurance_paid,
            'Total Taxes Paid': total_property_tax_paid,
            'Realtor Fee': realtor_fee,  # Added Realtor Fee
            'Net Equity': net_equity,  # Updated Net Equity
            'Cumulative Rent Paid': cumulative_rent_paid,
            'Investment Value': data['Investment Value'],
            'Cumulative Investment Rent': cumulative_investment_rent  # Added Cumulative Investment Rent
        })

        graph_data.append({
            'Year': year,
            'Total House Value': total_house_value,
            'Net Equity': net_equity,
            'Cumulative Rent Paid': cumulative_rent_paid,
            'Investment Value': data['Investment Value'],
            'Cumulative Investment Rent': cumulative_investment_rent
        })

    # Convert annual_data to DataFrame and format
    annual_df = pd.DataFrame(annual_data)
    graph_df = pd.DataFrame(graph_data)

    for column in annual_df.columns[1:]:  # Include all columns
        annual_df[column] = annual_df[column].apply(lambda x: f"({'{:,}'.format(round(abs(x), 2))})" if x < 0 else '{:,}'.format(round(x, 2)))

    return annual_df, graph_df

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')

