#===================
#Libraries
#===================

import pandas as pd
import inflection
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from PIL import Image
import folium
from streamlit_folium import folium_static

#===================
#Functions
#===================

#Changing country names
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]

#Creating types for each food price

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

#Color names
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]

#Renaming df columns
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

#=================================================== Logic Structure =======================================================

#========================
#Data Import and Cleaning
#========================

df = pd.read_csv( 'zomato.csv' )
pd.set_option('display.max_columns', None)
df1 = df.copy()

#Source:https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv

#Renaming colums
df1 = rename_columns(df1)

#Removing null values
df1 = df1.dropna()

#Removing duplicate rows
df1 = df1.drop_duplicates()

#Separating elements in 'Cuisines'
df1['cuisines'] = df1.loc[:, 'cuisines'].astype(str).apply(lambda x: x.split(",")[0])

#Creating 'Country' column
df1['country'] = df1.loc[:, 'country_code'].apply(lambda x: country_name(x))

#Creating 'Price Type' column
df1['price_type'] = df1.loc[:, 'price_range'].apply(lambda x: create_price_type(x))

#Swapping color codes with color names
df1["color_name"] = df1.loc[:, "rating_color"].apply(lambda x: color_name(x))


#=============================
#Page Config
#=============================

#has to be the first st code
st.set_page_config(page_title='World Map', page_icon='🗺️', layout='wide')


#============================
#Sidebar
#============================
st.sidebar.header('Filters')
st.sidebar.markdown("""---""")

#Rating Filters
rating_slider = st.sidebar.slider('Sort by Rating:', min_value=None, max_value=5.0, value=5.0, step=0.25, label_visibility="visible")

selected_ratings = df1['aggregate_rating'] < rating_slider
df1 = df1.loc[selected_ratings, :]
st.sidebar.markdown("""---""")

#Country Filters
country_options = st.sidebar.multiselect( 'Select Countries:', ['Australia', 'Brazil', 'Canada', 'England', 'India', 'Indonesia',
                                                               'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa',
                                                               'Sri Lanka', 'Turkey', 'United Arab Emirates',
                                                               'United States of America'],                    
                    default=['Brazil', 'Canada', 'England', 'Turkey', 'Indonesia', 'South Africa', 'Australia'] )

selected_countries = df1['country'].isin( country_options )
df1 = df1.loc[selected_countries, :]
st.sidebar.markdown("""---""")

#Cuisine Filter
cuisine_options = st.sidebar.multiselect( 'Select Cuisines:', ['Afghan', 'African', 'American', 'Andhra', 'Arabian', 'Argentine',
                                                               'Armenian', 'Asian', 'Asian Fusion', 'Assamese', 'Australian',
                                                               'Author', 'Awadhi', 'BBQ', 'Bakery', 'Balti', 'Bar Food',
                                                               'Belgian', 'Bengali', 'Beverages', 'Biryani', 'Brazilian',
                                                               'Breakfast', 'British', 'Burger', 'Burmese', 'Cafe', 'Cafe Food',
                                                               'Cajun', 'California', 'Canadian', 'Cantonese', 'Caribbean',
                                                               'Charcoal Chicken', 'Chettinad', 'Chinese', 'Coffee',
                                                               'Coffee and Tea', 'Contemporary', 'Continental', 'Creole',
                                                               'Crepes', 'Cuban', 'Deli', 'Desserts', 'Dim Sum', 'Dimsum',
                                                               'Diner', 'Donuts', 'Drinks Only', 'Durban', 'Döner',
                                                               'Eastern European', 'Egyptian', 'European', 'Fast Food',
                                                               'Filipino', 'Finger Food', 'Fish and Chips', 'French',
                                                               'Fresh Fish', 'Fusion', 'German', 'Giblets', 'Goan',
                                                               'Gourmet Fast Food', 'Greek', 'Grill', 'Gujarati', 'Hawaiian',
                                                               'Healthy Food', 'Home-made', 'Hyderabadi', 'Ice Cream', 'Indian',
                                                               'Indonesian', 'International', 'Iranian', 'Irish', 'Italian',
                                                               'Izgara', 'Japanese', 'Juices', 'Kebab', 'Kerala', 'Khaleeji',
                                                               'Kiwi', 'Kokoreç', 'Korean', 'Korean BBQ', 'Kumpir',
                                                               'Latin American', 'Lebanese', 'Lucknowi', 'Maharashtrian',
                                                               'Malaysian', 'Malwani', 'Mandi', 'Mangalorean', 'Mediterranean',
                                                               'Mexican', 'Middle Eastern', 'Mineira', 'Mithai',
                                                               'Modern Australian', 'Modern Indian', 'Momos', 'Mongolian',
                                                               'Moroccan', 'Mughlai', 'Naga', 'Nepalese', 'New American',
                                                               'New Mexican', 'North Eastern', 'North Indian', 'Old Turkish Bars',
                                                               'Others', 'Ottoman', 'Pacific Northwest', 'Pakistani', 'Pan Asian',
                                                               'Parsi', 'Patisserie', 'Peruvian', 'Pizza', 'Polish', 'Portuguese',
                                                               'Pub Food', 'Rajasthani', 'Ramen', 'Restaurant Cafe',
                                                               'Roast Chicken', 'Rolls', 'Russian', 'Salad', 'Sandwich',
                                                               'Scottish', 'Seafood', 'Singaporean', 'South African',
                                                               'South Indian', 'Southern', 'Southwestern', 'Spanish',
                                                               'Sri Lankan', 'Steak', 'Street Food', 'Sunda', 'Sushi', 'Taco',
                                                               'Taiwanese', 'Tapas', 'Tea', 'Tex-Mex', 'Thai', 'Tibetan',
                                                               'Turkish', 'Turkish Pizza', 'Ukrainian', 'Vegetarian',
                                                               'Vietnamese', 'Western', 'World Cuisine', 'Yum Cha'],
                    default=['Italian', 'Japanese', 'Brazilian', 'American', 'Fast Food', 'North Indian'])

selected_cuisines = df1['cuisines'].isin( cuisine_options )
df1 = df1.loc[selected_cuisines, :]
st.sidebar.markdown("""---""")

st.sidebar.markdown('###### For study, purposes by Helio Barbosa')
#===========================
#Main
#===========================
st.header('🗺️ World Map')
st.markdown('Disclaimer: The selection is limited by default to avoid performance issues in older systems')
st.markdown("""---""")

with st.container():
    map = folium.Map()
    for index, location_info in df1.iterrows():
     folium.Marker( [location_info['latitude'],
     location_info['longitude']],
     popup=location_info[['city', 'country', 'restaurant_name']] ).add_to( map )
    folium_static(map, width=960, height=720)