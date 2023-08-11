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

#Cost for two per country
def country_cost_two(df1):
    df_aux = df1.loc[:,['country' , 'average_cost_for_two']].groupby('country').mean().sort_values(by='average_cost_for_two' , ascending = False).round(2).reset_index()
    fig = px.bar( df_aux , x='country' , y='average_cost_for_two' , color='average_cost_for_two' , labels={'country':'Country' , 'average_cost_for_two':'Mean avg cost for two'} , text='average_cost_for_two')
    return fig

#Cuisines per country
def country_cuisines(df1):
    df_aux = df1.loc[:,['country' , 'cuisines']].groupby('country').nunique().sort_values(by='cuisines' , ascending=False).reset_index()
    fig = px.bar( df_aux , x='country' , y='cuisines', color='cuisines' , labels={'country':'Country' , 'cuisines':'Number of Cuisines'} , text='cuisines')
    return fig

#Country mean rating
def country_mean_rate(df1):
    df_aux = df1.loc[:,['country' , 'aggregate_rating']].groupby('country').mean().sort_values(by='aggregate_rating' , ascending=False).round(2).reset_index()
    fig = px.bar( df_aux , x='country' , y='aggregate_rating' , color='aggregate_rating' ,labels={'country':'Country' , 'aggregate_rating':'Mean Average Rating'} , text='aggregate_rating')
    return fig

#Country mean number of ratings
def country_vote_mean(df1):
    df_aux = df1.loc[:,['country' , 'votes']].groupby('country').mean().sort_values(by='votes' , ascending=False).round(2).reset_index()
    fig = px.bar( df_aux , x='country' , y='votes' , color='votes' , labels={'country':'Country' , 'votes':'Mean Number of Ratings'} , text='votes')
    return fig
    
#Cities per country
def country_cities(df1):
    df_aux = df1.loc[:,['country' , 'city']].groupby('country').nunique().sort_values(by='city' , ascending=False).reset_index()
    fig = px.bar( df_aux , x='country' , y='city' , color='city' , labels={'country':'Country' , 'city':'Number of Cities'} , text='city' )
    return fig

#Restaurants per country
def country_rest(df1):
    df_aux = df1.loc[:,['country' , 'restaurant_id']].groupby('country').nunique().sort_values(by='restaurant_id' , ascending=False).reset_index()
    fig = px.bar( df_aux , x='country' , y='restaurant_id' , color='restaurant_id', labels={'country':'Country' , 'restaurant_id':'Number of Restaurants'} , text='restaurant_id')
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
st.set_page_config(page_title='Countries', page_icon='🌐', layout='wide')

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
                    default=['Australia', 'Brazil', 'Canada', 'England', 'India', 'Indonesia',
                             'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa',
                             'Sri Lanka', 'Turkey', 'United Arab Emirates',
                             'United States of America'] )
st.sidebar.markdown("""---""")

selected_countries = df1['country'].isin( country_options )
df1 = df1.loc[selected_countries, :]
st.sidebar.markdown("""---""")

st.sidebar.markdown('###### For study, purposes by Helio Barbosa')

#===========================
#Main
#===========================
st.header('🌐 Countries')
st.markdown("""---""")
    
with st.container():
    col1, col2 = st.columns( 2 )
    with col1:
        st.subheader('Number of registered restaurants per country')
        fig = country_rest(df1)
        st.plotly_chart ( fig , use_container_width=True )
    with col2:
        st.subheader('Number of registered cities per country')
        fig = country_cities(df1)
        st.plotly_chart ( fig , use_container_width=True )

st.markdown("""---""")

with st.container():
    col1, col2 = st.columns( 2 )
    with col1:
        st.subheader('The mean number of ratings per country')
        fig = country_vote_mean(df1)
        st.plotly_chart( fig , use_container_width=True)
        
    with col2:
        st.subheader('The mean aggregate rating per country')
        fig = country_mean_rate(df1)
        st.plotly_chart( fig , use_container_width=True)

st.markdown("""---""")

with st.container():
    col1, col2 = st.columns( 2 )
    with col1:
        st.subheader('Number of cuisines per country')
        fig = country_cuisines(df1)
        st.plotly_chart( fig , use_container_width=True)
        
    with col2:
        st.subheader('The mean average cost for two per country')        
        fig = country_cost_two(df1)
        st.plotly_chart( fig , use_container_width=True)

