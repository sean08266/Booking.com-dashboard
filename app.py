import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urlencode, quote_plus

#爬蟲function
def booking_crawler(location, checkin_date, checkout_date):
    def generate_booking_url(location, checkin_date, checkout_date):
        base_url = "https://www.booking.com/searchresults.zh-tw.html"

        # 定義搜索參數
        params = {
            'ss': location,                  # 地點
            'checkin': checkin_date,         # 入住日期
            'checkout': checkout_date,       # 退房日期
            'group_adults': '2',              # 成人數
            'no_rooms': '1',                  # 房間數
            'group_children': '0',            # 兒童數
        }

        # 使用 urlencode 和 quote_plus 將參數編碼並構建 URL 字符串
        encoded_params = urlencode(params, quote_via=quote_plus)
        final_url = f"{base_url}?{encoded_params}"

        return final_url

    
    location_input = location
    checkin_date_input = checkin_date
    checkout_date_input = checkout_date

    url_book = generate_booking_url(location_input, checkin_date_input, checkout_date_input)
    def scrape_booking_data(url, num_pages=6):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        all_data = pd.DataFrame()  # 保存所有頁面的數據

        for page in range(1, num_pages + 1):
            # 構建每頁的 URL
            page_url = f"{url}&offset={(page - 1) * 25}"

            response = requests.get(page_url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            hotels = soup.findAll("div", {'data-testid': 'property-card'})

            name_list = []
            location_list = []
            price_list = []
            rating_list = []
            distance_list = []
            comments_list = []

            for hotel in hotels:
                name = hotel.find("div", {'data-testid': 'title'}).text.strip()
                name_list.append(name)

                location = hotel.find("span", {'data-testid': 'address'}).text.strip()
                location_list.append(location)

                price = hotel.find("span", {'data-testid': 'price-and-discounted-price'}).text.strip().replace('\xa0', ' ')
                price_list.append(price)

                rating = float(hotel.find("div", class_="a3b8729ab1 d86cee9b25").text.strip())
                rating_list.append(rating)

                distance = hotel.find("span", {'data-testid': 'distance'}).text.strip()
                distance_list.append(distance)

                comments = hotel.find("div", class_="a3b8729ab1 e6208ee469 cb2cbb3ccb").text.strip()
                comments_list.append(comments)

            # 將每頁的數據組織成 DataFrame
            data = {
                'name': name_list,
                'location': location_list,
                'price': price_list,
                'rating': rating_list,
                'distance': distance_list,
                'comments': comments_list
            }

            df = pd.DataFrame(data)
            all_data = pd.concat([all_data, df], ignore_index=True)

            # 休眠一下，避免對網站造成過多請求
            time.sleep(1)

        return all_data


    return scrape_booking_data(url_book,num_pages=5).drop_duplicates().reset_index(drop=True)



#資料處理function
def preprocess_data(df):
    # 將 'name' 欄位轉為字串
    df['name'] = df['name'].astype(str)

    # 將 'price' 欄位去除 'TWD '，並移除逗號，轉為整數型態
    df['price'] = df['price'].str.replace('TWD ', '').str.replace(',', '').astype(int)

    # 將 'comments' 欄位轉為字串
    df['comments'] = df['comments'].astype(str)
    # 將 'distance' 欄位轉為浮點數
    df["distance"]=df["distance"].str.replace('距中心 ', '')
    
    # 將 'distance' 欄位去除 '距中心 '，並根據單位轉為浮點數
    for i in range(len(df["distance"])):
        if '公尺' in df["distance"][i].split(" ")[1]:
            df["distance"][i] = float(df["distance"][i].split(" ")[0]) * 0.001
        else:
            df["distance"][i] = float(df["distance"][i].split(" ")[0])
    df["distance"] = df["distance"].astype(float)
   

    return df
from datetime import datetime as dt
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1("Booking.com Hotel Data "),
            width={'size': 6, 'offset': 3},
        ),
        className="mb-4",
    ),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label("Location:"),
                dbc.Input(id='location-input', value='', type='text'),
            ], className="mb-3"),
            html.Div([
                dbc.Label("Check-in Date:"),
                dcc.DatePickerSingle(
                    id='checkin-date-picker',
                    min_date_allowed=dt.today(),
                    initial_visible_month=dt.today(),
                    date=str(dt.today().date())
                ),
            ], className="mb-3"),
            html.Div([
                dbc.Label("Check-out Date:"),
                dcc.DatePickerSingle(
                    id='checkout-date-picker',
                    min_date_allowed=dt.today(),
                    initial_visible_month=dt.today(),
                    date=str(dt.today().date())
                ),
            ], className="mb-3"),
            dbc.Button("Submit", id='submit-button', color="primary", className="me-2"),
        ], width=4),
    ]),
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='scatter-plot'),
            width=12,
        )
    ),
    dbc.Row([
        dbc.Col([
            dcc.Loading(
                id="loading-1",
                children=html.Div(id="loading-output-1"),
                type="default",
                fullscreen=True,  # or False if you want it inline
                style={'position': 'absolute', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)'}
            )

        ], width=12),
    ])
], fluid=True)

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('submit-button', 'n_clicks'),
    [State('location-input', 'value'),
     State('checkin-date-picker', 'date'),
     State('checkout-date-picker', 'date')],
    prevent_initial_call=True
)
def update_output(n_clicks, location, check_in, check_out):

    if n_clicks:
    
        df = booking_crawler(location, check_in, check_out)
        
        df = preprocess_data(df)

        fig = px.scatter(
            df,
            x='price',
            y='distance',
            color='rating',
            hover_name='name',
            hover_data={'price': ':,', 'distance': ':.2f', 'rating': ':.1f'},
            title='Hotel Price and Distance Scatter Plot',
            labels={'price': 'Price (TWD)', 'distance': 'Distance from Center (km)'},
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig.update_layout(coloraxis_colorbar=dict(title='Rating'))
        return fig
    else:
        return px.scatter()

if __name__ == '__main__':
    app.run_server(debug=True)
