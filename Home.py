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
st.set_page_config(page_title='Main', page_icon='📈', layout='wide')


#============================
#Sidebar
#============================
image = Image.open( 'logo.png' )
#Base image: https://commons.wikimedia.org/wiki/File:Search-icon-plain.png , by Kurt Kaiser

st.sidebar.image( image , width=80 )

st.sidebar.markdown('# Find-A-Restaurant')
st.sidebar.markdown('## Analyzing restaurants worldwide')
st.sidebar.markdown("""---""")

#Rating Filters
rating_slider = st.sidebar.slider('Sort by Rating:', min_value=None, max_value=5.0, value=5.0, step=0.25, label_visibility="visible")

selected_ratings = df1['aggregate_rating'] < rating_slider
df1 = df1.loc[selected_ratings, :]
st.sidebar.markdown("""---""")

#Country Filters
country_options = st.sidebar.multiselect( 'Select Countries:', ['Philippines', 'Brazil', 'Australia', 'United States of America', 
                                                               'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia',
                                                               'New Zeland', 'England', 'Qatar', 'South Africa','Sri Lanka', 'Turkey'],
                    default=['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates',
                             'India', 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa','Sri Lanka', 'Turkey'] )

selected_countries = df1['country'].isin( country_options )
df1 = df1.loc[selected_countries, :]
st.sidebar.markdown("""---""")

st.sidebar.markdown('###### For study, purposes by Helio Barbosa')
#===========================
#Main
#===========================
st.image( image , width=80 )


st.header('Find-A-Restaurant')
st.subheader('Find the right restaurant for you, anywhere in the world!')

st.markdown("""---""")

st.markdown('We have in our database:')

st.markdown("""---""")

with st.container():
    col1, col2, col3, col4, col5 = st.columns( 5 )
    with col1:
        df_aux=df1['restaurant_id'].nunique()
        st.metric('Restaurants' , df_aux )
    with col2:
        df_aux=df1['country_code'].nunique()
        st.metric('Countries' , df_aux )
    with col3:
        df_aux=df1['city'].nunique()
        st.metric('Cities' , df_aux )
    with col4:
        df_aux=df1['cuisines'].nunique()
        st.metric('Cuisines' , df_aux )
    with col5:
        df_aux=df1['votes'].sum()
        st.metric('Number of Ratings' , df_aux )
st.markdown("""---""")

st.markdown(
    """
    To facilitate data-driven decisions, the Find-a-Restaurant project started. The project used the Zomato Restaurants database, which helps clients to find restaurants worldwide, informing the cuisines, addresses, booking information, and delivery information of restaurants; alongside a rating system.
    
    ### How to use this Dashboard?
    
    - Home:
        - Overview of contents and this set of instructions;
        - For quick insights, there is a country selector and a rating slider on the sidebar.
           
    - Countries:
        - Number of registered restaurants and cities on the database;
        - Total of ratings and mean average ratings;
        - Number of cuisines and average prices per country;

    - Cities:
        - Top lists of cities according to the number of restaurants, ratings, and cuisines.
    
    - Cuisines:
        - Lists of top and bottom restaurants using the sidebar selection;
        - In the top section, there is a list of the top restaurants from popular cuisines;
        - The cuisine selection can be used to remove less popular cuisines for better analysis;
        - IMPORTANT: Do not remove the popular cuisines from the sidebar to avoid errors.
    
    - World Map:
        - An interactive World Map with location pins containing descriptions;
        - The selection is limited by default to avoid performance issues in older systems.
    
    ### Ask for Help
    - @heliobtech - Author
""")