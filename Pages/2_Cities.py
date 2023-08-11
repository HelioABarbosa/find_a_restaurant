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

#Top 10 cities x cuisines
def top_cuisines_city(df1):
    df_aux = df1.loc[: ,['cuisines' , 'city' , 'country']].groupby(['city','country']).nunique().sort_values(by='cuisines' , ascending=False).reset_index().head(10)
    fig = px.bar( df_aux , x='city' , y='cuisines' , color='country' , labels={'city':'Cities' , 'cuisines':'Cuisines'} , text='cuisines' )
    return fig

#Top 5 cities with rating below 2.5
def bot_rest_rate(df1):
    df_aux = df1[df1['aggregate_rating'] < 2.5][['restaurant_id', 'city', 'country']].groupby(['city','country']).nunique().sort_values(by='restaurant_id' , ascending=False).reset_index().head(5)
    fig = px.bar( df_aux , x='city' , y='restaurant_id' , color='country' , labels={'city':'Cities' , 'restaurant_id':'Number of Restaurants'} , text='restaurant_id' )
    return fig

#Top 5 cities with rating above 4
def top_rest_rate(df1):    
    df_aux = df1[df1['aggregate_rating'] > 4][['restaurant_id','city','country']].groupby(['city','country']).nunique().sort_values(by='restaurant_id' , ascending=False).reset_index().head(5)
    fig = px.bar( df_aux , x='city' , y='restaurant_id' , color='country' , labels={'city':'Cities' , 'restaurant_id':'Number of Restaurants'} , text='restaurant_id' )
    return fig

#Top 10 restaurants per city
def top_cities_rest(df1):    
    df_aux = df1[['restaurant_id','city','country']].groupby(['city','country']).nunique().sort_values(by='restaurant_id' , ascending=False).reset_index().head(10)
    fig = px.bar( df_aux, x='city' , y='restaurant_id' , color='country' , labels={'city':'Cities' , 'restaurant_id':'Number of Restaurants'} , text='restaurant_id' )
    return fig

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

#has to be the first st code run
st.set_page_config(page_title='Cities', page_icon='🌇', layout='wide')


#============================
#Sidebar
#============================
st.sidebar.header('Filters')
st.sidebar.markdown("""---""")

#Country Filters
country_options = st.sidebar.multiselect( 'Select Countries:', ['Australia', 'Brazil', 'Canada', 'England', 'India', 'Indonesia',
                                                               'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa',
                                                               'Sri Lanka', 'Turkey', 'United Arab Emirates',
                                                               'United States of America'],
                    default=['Australia', 'Brazil', 'Canada', 'England', 'India', 'Indonesia',
                             'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa',
                             'Sri Lanka', 'Turkey', 'United Arab Emirates',
                             'United States of America'] )

selected_countries = df1['country'].isin( country_options )
df1 = df1.loc[selected_countries, :]
st.sidebar.markdown("""---""")

st.sidebar.markdown('###### For study, purposes by Helio Barbosa')
#===========================
#Main
#===========================
st.header('🌇 Cities')
st.markdown("""---""")

with st.container():
    st.subheader('Top 10 cities with the most restaurants on the database')
    fig=top_cities_rest(df1)
    st.plotly_chart ( fig , use_container_width=True )

st.markdown("""---""")

with st.container():
    col1, col2 = st.columns( 2 )
    with col1:
        st.subheader('Top 5 cities with restaurants with an average rating > 4')
        fig = top_rest_rate(df1)
        st.plotly_chart( fig , use_container_width=True)        
    with col2:
        st.subheader('Top 5 cities with restaurants with an average rating < 2.5')
        fig = bot_rest_rate(df1)
        st.plotly_chart( fig , use_container_width=True)

st.markdown("""---""")

with st.container():
    st.subheader('Top 10 cities with unique cuisine types')
    fig = top_cuisines_city(df1)
    st.plotly_chart ( fig , use_container_width=True )