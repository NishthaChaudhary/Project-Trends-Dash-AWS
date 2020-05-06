import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import datetime
from dash.dependencies import Input, Output

global dff
df=pd.read_csv('data-trending-nishtha-2020.csv', index_col=False, sep='|')
dff=df.copy()
dff['transaction_date']=pd.to_datetime(dff['transaction_date'],format= '%m/%d/%Y')

global family
global day
family=dff['prod_family'].unique()
day=[8,31,90]


external_stylesheets = ['https://github.com/STATWORX/blog/blob/master/DashApp/assets/style.css']

application = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


application.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('PRODUCT TRENDS'),
                                 html.P('Select the Product Family:'),
                    html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='product-family',options=[{'label': i, 'value': i} for i in family],
                                                      value='ACCESSORIES',
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='stockselector'
                                                      )],style={'color': '#1E1E1E'}),
                    html.Div(       children=[
                                    html.P('Time Duration:'),
                                    dcc.RadioItems(id='duration-time',
                                                   options=[{'label': i, 'value': i} for i in day],
                                                   value=8
                                        )],style={'display': 'inline-block'}),
                    html.Div(children=[
                                html.Div(id='html',style={'align':'centre'})]
                             )]),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='trend-graph', style={'color': '#1E1E1E'})
                             ])
        ])])


@application.callback(
        Output('trend-graph','figure'),
        [Input('product-family','value'),
         Input('duration-time','value')])
        
def week_data(family,days):
    dff_family=dff.loc[dff.prod_family==family]
    last=dff_family['transaction_date'].max()
    d=days
    start_delta = datetime.timedelta(d)
    start_of_week = last - start_delta
    mask=(dff_family['transaction_date']>start_of_week) & (dff_family['transaction_date']<=last)
    dff_family_lastweek=dff_family.loc[mask]
    week_data=dff_family_lastweek.groupby('prod_name').agg({'transaction_id':lambda x:len(x)}).reset_index()
    #rename the columns
    week_data.rename(columns={'transaction_id':'# transactions'},inplace=True)
    week_data.sort_values(by=['# transactions'],ascending=False,inplace= True)
    week_data.reset_index(drop=True, inplace= True)
    week_data_top5=week_data.head(5).reset_index(drop=True)
    
    return ({
            'data': [{'x': week_data_top5['prod_name'], 'y': week_data_top5['# transactions'], 'type': 'line', 
                      'name': 'Transactions'} , ],'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                            'color': colors['text']
        }
        }
    }
    )
    
    
@application.callback(
        Output('html','children'),
        [Input('product-family','value'),
         Input('duration-time','value')])
    
def generate_table(family,days):
    dff_family=dff.loc[dff.prod_family==family]
    last=dff_family['transaction_date'].max()
    d=days
    start_delta = datetime.timedelta(d)
    start_of_week = last - start_delta
    mask=(dff_family['transaction_date']>start_of_week) & (dff_family['transaction_date']<=last)
    dff_family_lastweek=dff_family.loc[mask]
    week_data=dff_family_lastweek.groupby('prod_name').agg({'transaction_id':lambda x:len(x)}).reset_index()
    #rename the columns
    week_data.rename(columns={'transaction_id':'# transactions'},inplace=True)
    week_data.sort_values(by=['# transactions'],ascending=False,inplace= True)
    week_data.reset_index(drop=True, inplace= True)
    week_data_top5=week_data.head(5).reset_index(drop=True)
    return html.Table([
       html.Thead(
            html.Tr([html.Th(col) for col in week_data_top5.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(week_data_top5.iloc[i][col]) for col in week_data_top5.columns
            ]) for i in range(min(len(week_data_top5), 5))
        ])
   ])





# Run the app
if __name__ == '__main__':
    application.run_server(debug=True)