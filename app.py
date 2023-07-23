import requests
import streamlit as st
import numpy as np
import pandas as pd
import datetime as dt
from constants import WEATHER_API_KEY

# 2022-2023 | Kazakhstan Population
cities_by_population = {'Almaty': '1534353', 'Astana': '844930', 
                        'Shymkent': '704983', 'Karaganda': '489355', 'Aqtobe': '385438', 'Taraz': '355682', 'Pavlodar': '332062', 'Ust-Kamenogorsk': '316093', 'Uralsk': '230354', 'Kostanay': '225464', 'Kyzylorda': '218300', 'Petropavlovsk': '208979', 'Atyrau': '202026', 'Aktau': '182033', 'Temirtau': '176865', 'Turkistan': '157399', 'Kokshetau': '141396', 'Taldykorgan': '137654', 'Ekibastuz': '132075', 'Zhezkazgan': '84977', 'Baikonur': '73464', 'Balkhash': '71339', 'Ridder': '49574', 'Talgar': '48107', 'Stepnogorsk': '47045', 'Shchuchinsk': '45963', 'Zharkent': '42809', 'Aksu': '42519', 'Arys': '42286', 'Saryagash': '39758', 'Shakhtinsk': '38468', 'Esik': '38440', 'Shu': '35929', 'Jitikara': '35132', 'Aksai': '33589', 'Kandyagash': '32102', 'Aralsk': '31768', 'Chardara': '30850', 'Tekeli': '30079', 'Zhetysai': '29688', 'Atbasar': '29673', 'Arkalyk': '28968', 'Abay': '27954', 'Shalkar': '27703', 'Karatau': '27667', 'Khromtau': '25198', 'Ushtobe': '24743', 'Lenger': '24302', 'Zhanatas': '21658', 'Alga': '19997', 'Shemonaikha': '18211', 'Ucharal': '17523', 'Makinsk': '17205', 'Zaisan': '15712', 'Sarkand': '13914', 'Akkol': '13708', 'Priozersk': '13367', 'Kurchatov': '11810', 'Emba': '11735', 'Tayinsha': '11437', 'Yesil': '10895', 'Ereimentau': '10349', 'Karazhal': '9569', 'Serebryansk': '9071', 'Karkaralinsk': '8633', 'Ball': '7710', 'Bulaevo': '7606', 'Sergeevka': '7374', 'Mamlutka': '7238', 'Kazalinsk': '7214', 'Derzhavinsk': '6307', 'Stepnyak': '3844', 'Temir': '2520'}

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather(city):
    open_weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    response = requests.get(open_weather_url)
    if response.status_code != 200:
        return None
    weather_data = response.json()
    return weather_data

def get_air_pollution(lat, lon):
    open_air_quality_url = f'http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}'
    response = requests.get(open_air_quality_url)
    if response.status_code != 200:
        return None
    air_quality_data = response.json()
    return air_quality_data

def main():
    st.set_page_config(
        page_title='Kazakhstan Weather App', 
        page_icon='🌤️'
    )

    st.title('Kazakhstan Smart Weather App', help='This app is built using Streamlit and OpenWeatherMap API')

    with st.form(key='weather_form'):
        city = st.selectbox('Choose a city', list(cities_by_population.keys()))
        submit_button = st.form_submit_button(label='Get Analytics')


    if submit_button:
        weather_data = get_weather(city)

        if weather_data is None:
            st.error(f'City not found, Population: {cities_by_population[city]}')
        else:
            st.subheader(f'🌤️ Weather Analytics in {city}: ')
            air_data = get_air_pollution(weather_data['coord']['lat'], weather_data['coord']['lon'])
            weather_data['main']['temp'] = kelvin_to_celsius(weather_data['main']['temp'])
            weather_data['main']['feels_like'] = kelvin_to_celsius(weather_data['main']['feels_like'])
            weather_data['main']['temp_min'] = kelvin_to_celsius(weather_data['main']['temp_min'])
            weather_data['main']['temp_max'] = kelvin_to_celsius(weather_data['main']['temp_max'])
            weather_data['population'] = cities_by_population[city]
            st.markdown(f'''
            Weather Analysis for Anomaly Detection:\n 
            - `Temperature`: {weather_data['main']['temp']} °C\n
            - `Pressure`: {weather_data['main']['pressure']} hPa\n
            - `Humidity`: {weather_data['main']['humidity']} %\n
            - `Wind Speed`: {weather_data['wind']['speed']} m/s\n
            - `Weather State`: {weather_data['weather'][0]['description']}\n
            - `Sunrise`: {dt.datetime.utcfromtimestamp(weather_data['sys']['sunrise'] + weather_data['timezone'])}\n
            - `Sunset`: {dt.datetime.utcfromtimestamp(weather_data['sys']['sunset'] + weather_data['timezone'])}\n
            - `Air Pollution Index`: {air_data['list'][0]['main']['aqi']}\n
            - `Air Pollution Components`:\n
                - `Carbon Monoxide`: {air_data['list'][0]['components']['co']} μg/m³\n
                - `Nitrogen Monoxide`: {air_data['list'][0]['components']['no']} μg/m³\n
                - `Nitrogen Dioxide`: {air_data['list'][0]['components']['no2']} μg/m³\n
                - `Ozone`: {air_data['list'][0]['components']['o3']} μg/m³\n
                - `Sulphur Dioxide`: {air_data['list'][0]['components']['so2']} μg/m³\n
                - `Ammonia`: {air_data['list'][0]['components']['nh3']} μg/m³\n''')
            df = pd.DataFrame({'lat': [weather_data['coord']['lat']], 'lon': [weather_data['coord']['lon']], 'name': [city], 'population': [weather_data['population']]})
            st.map(df, latitude='lat', longitude='lon', color='#00ff00')
            weather_json, air_pollution_json = st.columns(2)
            with weather_json:
                st.subheader('Weather JSON Data')
                weather_json.json(weather_data)
            with air_pollution_json:
                st.subheader('Air Pollution JSON Data')
                air_pollution_json.json(air_data)

    st.markdown('<footer style="margin-top: 300px; text-align: center;">Made with ❤️ by <a href="https://github.com/silvermete0r">Grembim</a></footer>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()