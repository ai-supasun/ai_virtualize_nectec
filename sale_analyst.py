import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv('sale_analyst.csv',parse_dates=['Date'])
print(df)
app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),
    html.Div(id='datatable-interactivity-container')
])

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])
def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)


    def choose_category(category_date,category_stock):
        list_price = []
        list_quantity = []

        if 'year' == category_date:
            df_sum = dff.groupby(['year']).sum().reset_index()[['year','Price','Quantity']]
            list_name = df_sum['year'].tolist()
            list_price_category = df_sum['Price'].tolist() 
            list_quantity_category = df_sum['Quantity'].tolist()
            for i in range(len(list_name)):
                list_price.append({'x': [list_name[i]], 'y': [list_price_category[i]], 'type': 'bar', 'name': '{}'.format(list_name[i])})
                list_quantity.append({'x': [list_name[i]], 'y': [list_quantity_category[i]], 'type': 'bar', 'name': '{}'.format(list_name[i])})

        if 'quarter' == category_date or 'month' == category_date or 'date' == category_date:
            df_sum = dff.groupby(['year','{}'.format(category_date)]).sum().reset_index()[['year','{}'.format(category_date),'Price','Quantity']].sort_values(by=['{}'.format(category_date)]).reset_index()
            list_name_year = df_sum['year'].tolist()
            list_name = df_sum['{}'.format(category_date)].tolist()
            list_price_category = df_sum['Price'].tolist()
            list_quantity_category = df_sum['Quantity'].tolist()
            df_list_quarter = pd.DataFrame({
                'year':list_name_year,
                'name':list_name,
                'list_price_category':list_price_category,
                'list_quantity_category':list_quantity_category
            }).sort_values(by='year')
            # print(df_list_quarter)
            list_unique_year = df_list_quarter['year'].unique().tolist()
            for i in range(len(list_unique_year)):
                list_price.append({'x': df_list_quarter[df_list_quarter['year'] == list_unique_year[i]]['name'].tolist(), 'y': df_list_quarter[df_list_quarter['year'] == list_unique_year[i]]['list_price_category'].tolist(), 'type': 'bar', 'name': '{}'.format(list_name_year[i])})
                list_quantity.append({'x': df_list_quarter[df_list_quarter['year'] == list_unique_year[i]]['name'].tolist(), 'y': df_list_quarter[df_list_quarter['year'] == list_unique_year[i]]['list_quantity_category'].tolist(), 'type': 'bar', 'name': '{}'.format(list_name_year[i])})
        elif 'week' == category_date:
            df_sum_week = dff.groupby(['year','week']).sum().reset_index()[['year','week','Price','Quantity']].sort_values(by=['week']).reset_index()
            dict_week = {0:'monday',
                        1:'Tuesday',
                        2:'Wednesday',
                        3:'Thursday',
                        4:'Friday',
                        5:'Saturay',
                        6:'Sunday',}
            list_week_name = []
            for i in range(len(df_sum_week)):
                list_week_name.append(dict_week[df_sum_week['week'][i]])
            list_name_year_week = df_sum_week['year'].tolist()
            list_price_week = df_sum_week['Price'].tolist()
            list_quantity_week = df_sum_week['Quantity'].tolist()

            df_list_week = pd.DataFrame({
                'year':list_name_year_week,
                'name':list_week_name,
                'list_price_category':list_price_week,
                'list_quantity_category':list_quantity_week
            }).sort_values(by='year')
            list_unique_year = df_list_week['year'].unique().tolist()
            for i in range(len(list_unique_year)):
                list_price.append({'x': df_list_week[df_list_week['year'] == list_unique_year[i]]['name'].tolist(), 'y': df_list_week[df_list_week['year'] == list_unique_year[i]]['list_price_category'].tolist(), 'type': 'bar', 'name': '{}'.format(list_name_year_week[i])})
                list_quantity.append({'x': df_list_week[df_list_week['year'] == list_unique_year[i]]['name'].tolist(), 'y': df_list_week[df_list_week['year'] == list_unique_year[i]]['list_quantity_category'].tolist(), 'type': 'bar', 'name': '{}'.format(list_name_year_week[i])})
        if category_stock == 'price':
            solution = list_price
        elif category_stock == 'quantity':
            solution = list_quantity
        return solution
    temp_year = 'year'
    temp_category = 'price'

    return [
        dcc.Graph(
            id="Price",
            figure={"data": choose_category('{}'.format(temp_year),'{}'.format(temp_category))},
        )
    ]


if __name__ == '__main__':
    app.run_server(debug=True)