import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy_financial as npf

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define CSS styles
styles = {
    'container': {
        'maxWidth': '800px',
        'margin': '0 auto',
        'padding': '20px',
        'border': '1px solid #ddd',
        'borderRadius': '5px',
        'boxShadow': '2px 2px 10px #aaa'
    },
    'input': {
        'margin': '10px 0'
    },
    'button': {
        'margin': '20px 0'
    }
}

# Define the layout of the app
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row(dbc.Col(html.H1('Home Ownership Costs Calculator'), width=12, className="mb-4 text-center")),

    dbc.Row([
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Purchase Price"),
            dbc.Input(id='purchase-price', type='number', placeholder='Enter Purchase Price', value=400000),
        ]), width=4),
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Down Payment (%)"),
            dbc.Input(id='down-payment-percentage', type='number', placeholder='Enter Down Payment Percentage', value=0.10),
        ]), width=4),
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Annual Interest Rate (%)"),
            dbc.Input(id='annual-interest-rate', type='number', placeholder='Enter Annual Interest Rate', value=0.065),
        ]), width=4),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Property Tax Start"),
            dbc.Input(id='property-tax-start', type='number', placeholder='Enter Property Tax Start', value=8000),
        ]), width=4),
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Tax Increase Interval"),
            dbc.Input(id='property-tax-increase-interval', type='number', placeholder='Enter Tax Increase Interval', value=10),
        ]), width=4),
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Tax Increase Amount"),
            dbc.Input(id='property-tax-increase-amount', type='number', placeholder='Enter Tax Increase Amount', value=2000),
        ]), width=4),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Annual Insurance Cost"),
            dbc.Input(id='annual-insurance-cost', type='number', placeholder='Enter Annual Insurance Cost', value=2000),
        ]), width=4),
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Real Estate Growth Rate (%)"),
            dbc.Input(id='real-estate-annual-growth-rate', type='number', placeholder='Enter Real Estate Growth Rate', value=0.03),
        ]), width=4),
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Loan Term (Years)"),
            dbc.Input(id='loan-term-years', type='number', placeholder='Enter Loan Term Years', value=30),
        ]), width=4),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Monthly Rent"),
            dbc.Input(id='monthly-rent', type='number', placeholder='Enter Monthly Rent', value=1350),
        ]), width=4),
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Monthly Rent Increase"),
            dbc.Input(id='monthly-rent-increase', type='number', placeholder='Enter Monthly Rent Increase', value=30),
        ]), width=4),
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Monthly Investment"),
            dbc.Input(id='monthly-investment', type='number', placeholder='Enter Monthly Investment', value=15000 / 12),
        ]), width=4),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Investment Return Rate (%)"),
            dbc.Input(id='investment-return-rate', type='number', placeholder='Enter Investment Return Rate', value=0.10),
        ]), width=4),
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Total Years"),
            dbc.Input(id='total-years', type='number', placeholder='Enter Total Years', value=30),
        ]), width=4),
        dbc.Col(dbc.InputGroup([
            dbc.InputGroupText("Realtor Fee (%)"),
            dbc.Input(id='realtor-fee', type='number', placeholder='Realtor Fee Percentage...', value=0.05),
        ]), width=4),
    ], className="mb-3"),

    dbc.Row(dbc.Col(
        dbc.Button('Calculate', id='calculate', n_clicks=0, color="primary", className="me-md-2"),
        width={"size": 2, "offset": 5}, className="mb-4"
    )),

    dbc.Row(dbc.Col(html.Div(id='table-container'), width=12))
])

@app.callback(
    Output('table-container', 'children'),
    [Input('calculate', 'n_clicks')],
    [Input('purchase-price', 'value'),
     Input('down-payment-percentage', 'value'),
     Input('annual-interest-rate', 'value'),
     Input('property-tax-start', 'value'),
     Input('property-tax-increase-interval', 'value'),
     Input('property-tax-increase-amount', 'value'),
     Input('annual-insurance-cost', 'value'),
     Input('real-estate-annual-growth-rate', 'value'),
     Input('loan-term-years', 'value'),
     Input('monthly-rent', 'value'),
     Input('monthly-rent-increase', 'value'),
     Input('monthly-investment', 'value'),
     Input('investment-return-rate', 'value'),
     Input('realtor-fee', 'value'),
     Input('total-years', 'value'),
     ])

def update_table(n_clicks, purchase_price, down_payment_percentage, annual_interest_rate, property_tax_start,
                 property_tax_increase_interval, property_tax_increase_amount, annual_insurance_cost,
                 real_estate_annual_growth_rate, loan_term_years, monthly_rent, monthly_rent_increase,
                 monthly_investment, investment_return_rate, realtor_fee, total_years):
    if n_clicks > 0:
        formatted_annual_df = calculate_home_ownership_costs(
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
            total_years
        )
        # Use dbc.Table.from_dataframe to create a Bootstrap-styled table
        table = dbc.Table.from_dataframe(formatted_annual_df, striped=True, bordered=True, hover=True, className="sticky-header-table")
        # Wrap your table in a container and set a max height
        return html.Div(table, style={'overflowY': 'auto', 'maxHeight': '600px'}, className="table-container")
    return html.Div('Enter values and click calculate.', className="mt-4")

# The calculate_home_ownership_costs function (implementation)
import numpy_financial as npf
import pandas as pd

def calculate_home_ownership_costs(purchase_price, down_payment_percentage, annual_interest_rate, property_tax_start,
                                   property_tax_increase_interval, property_tax_increase_amount, annual_insurance_cost,
                                   real_estate_annual_growth_rate, loan_term_years, monthly_rent, monthly_rent_increase,
                                   monthly_investment, investment_return_rate, realtor_fee_percentage, total_years=30):
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
    years_to_display = list(range(1, total_years + 1))
    annual_data = []

    for year in years_to_display:
        year_data = df[df['Month'] <= year * 12]

        total_interest_paid = year_data['Interest for Month'].sum()
        total_insurance_paid = year_data['Insurance for Month'].sum()
        total_property_tax_paid = year_data['Property Tax for Month'].sum()
        data = year_data.iloc[-1]  # Get the last month of the year
        total_house_value = data['Home Value']  # Get the home value at the end of the year
        realtor_fee = total_house_value * realtor_fee_percentage  # Calculate realtor fee
        net_equity = data['Total Equity'] - total_interest_paid - total_insurance_paid - total_property_tax_paid - realtor_fee  # Subtract realtor fee from net equity
        cumulative_rent_paid = sum([(monthly_rent + (y - 1) * monthly_rent_increase) * 12 for y in range(1, int(year) + 1)])

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
            'Investment Value': data['Investment Value']
        })

    # Convert annual_data to DataFrame and format
    annual_df = pd.DataFrame(annual_data)
    for column in annual_df.columns[1:]:  # Include all columns
        annual_df[column] = annual_df[column].apply(lambda x: f"({'{:,}'.format(round(abs(x), 2))})" if x < 0 else '{:,}'.format(round(x, 2)))

    return annual_df



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')

