# Import Library
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
# Import File Quarter
df_clean = pd.read_csv('sale_analyst.csv',parse_dates=['Date'])
print(df_clean)
def between(start_date,end_date):
  df_between_date = df_clean[(df_clean['Date'] > start_date) & (df_clean['Date'] <= end_date)]
  df_between_date['quarter'] = df_between_date['Date'].dt.quarter
  df_between_date
  return df_between_date
df_between_date = between('2018-01-12','2020-12-18')
# year

def choose_category(category_date,category_stock):
    list_price = []
    list_quantity = []

    if 'year' == category_date:
        df_sum = df_between_date.groupby(['year']).sum().reset_index()[['year','Price','Quantity']]
        list_name = df_sum['year'].tolist()
        list_price_category = df_sum['Price'].tolist() 
        list_quantity_category = df_sum['Quantity'].tolist()
        for i in range(len(list_name)):
            list_price.append({'x': [list_name[i]], 'y': [list_price_category[i]], 'type': 'bar', 'name': '{}'.format(list_name[i])})
            list_quantity.append({'x': [list_name[i]], 'y': [list_quantity_category[i]], 'type': 'bar', 'name': '{}'.format(list_name[i])})

    if 'quarter' == category_date or 'month' == category_date or 'date' == category_date:
        df_sum = df_between_date.groupby(['year',f'{category_date}']).sum().reset_index()[['year',f'{category_date}','Price','Quantity']].sort_values(by=[f'{category_date}']).reset_index()
        list_name_year = df_sum['year'].tolist()
        list_name = df_sum[f'{category_date}'].tolist()
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
            list_price.append({'x': df_list_quarter[df_list_quarter['year'] == list_unique_year[i]]['name'].tolist(), 'y': df_list_quarter[df_list_quarter['year'] == list_unique_year[i]]['list_price_category'].tolist(), 'type': 'bar', 'name': f'{list_name_year[i]}'})
            list_quantity.append({'x': df_list_quarter[df_list_quarter['year'] == list_unique_year[i]]['name'].tolist(), 'y': df_list_quarter[df_list_quarter['year'] == list_unique_year[i]]['list_quantity_category'].tolist(), 'type': 'bar', 'name': f'{list_name_year[i]}'})
    elif 'week' == category_date:
        df_sum_week = df_between_date.groupby(['year','week']).sum().reset_index()[['year','week','Price','Quantity']].sort_values(by=['week']).reset_index()
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
choose_category('quarter','price')
# Import Css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# # Port and Css
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# # Layout
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Graph(
        id='year_price',
        figure={
            'data': choose_category('year','price'),
            'layout': {
                'title': 'year_price'
            }
        }
    ),
    dcc.Graph(
        id='year_quantity',
        figure={
            'data': choose_category('year','quantity'),
            'layout': {
                'title': 'year_quantity'
            }
        }
    ),
    dcc.Graph(
        id='quarter_price',
        figure={
            'data': choose_category('quarter','price'),
            'layout': {
                'title': 'quarter_price'
            }
        }
    ),
    dcc.Graph(
        id='quarter_quantity',
        figure={
            'data': choose_category('quarter','quantity'),
            'layout': {
                'title': 'quarter_quantity'
            }
        }
    ),
    dcc.Graph(
        id='month_price',
        figure={
            'data': choose_category('month','price'),
            'layout': {
                'title': 'month_price'
            }                          
        }
    ),
    dcc.Graph(
        id='month_quantity',
        figure={
            'data': choose_category('month','quantity'),
            'layout': {
                'title': 'month_quantity'
            }                          
        }
    ),
    dcc.Graph(
        id='day_price',
        figure={
            'data': choose_category('date','price'),
            'layout': {
                'title': 'day_price'
            }                          
        }
    ),
    dcc.Graph(
        id='day_quantity',
        figure={
            'data': choose_category('date','quantity'),
            'layout': {
                'title': 'day_quantity'
            }                          
        }
    ),
        dcc.Graph(
        id='week_price',
        figure={
            'data': choose_category('week','price'),
            'layout': {
                'title': 'week_price'
            }                          
        }
    ),
    dcc.Graph(
        id='week_quantity',
        figure={
            'data': choose_category('week','quantity'),
            'layout': {
                'title': 'week_quantity'
            }                          
        }
    ),
])
if __name__ == '__main__':
    app.run_server(debug=True)