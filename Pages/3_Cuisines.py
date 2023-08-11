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

#Bottom 10 cuisines
def cuisines_bot(df1):
    df_aux = df1.loc[:,['cuisines','aggregate_rating']].groupby('cuisines').mean().sort_values(by='aggregate_rating').round(2).reset_index().head(10)
    fig = px.bar( df_aux , x='cuisines' , y='aggregate_rating' , color='aggregate_rating' , labels={'cuisines':'Cuisines' , 'aggregate_rating':'Mean Average Ratings'} , text='aggregate_rating')
    return fig
    

#Top 10 cuisines
def cuisines_top(df1):
    df_aux = df1.loc[:,['cuisines','aggregate_rating']].groupby('cuisines').mean().sort_values(by='aggregate_rating' , ascending=False).round(2).reset_index().head(10)
    fig = px.bar( df_aux , x='cuisines' , y='aggregate_rating' , color='aggregate_rating' , labels={'cuisines':'Cuisines' , 'aggregate_rating':'Mean Average Ratings'} , text='aggregate_rating')
    return fig

#Top restaurant from a cuisine type
def cuisine_top_rest(cuisine_type):
    df_aux = df1[df1['cuisines'] == cuisine_type][['restaurant_id' , 'restaurant_name', 'aggregate_rating']].sort_values(by=['aggregate_rating' , 'restaurant_id'] , ascending=[False , True] ).reset_index()
    return df_aux

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

#Remvoing cuisines with no reviews
df1 = df1.drop(df1[(df1["cuisines"] == "Drinks Only")].index)
df1 = df1.drop(df1[(df1["cuisines"] == "Mineira")].index)

#=============================
#Page Config
#=============================

#has to be the first st code run
st.set_page_config(page_title='Cuisines', page_icon='🥣', layout='wide')

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
                    default=['Italian', 'Japanese', 'Chinese', 'Seafood','Brazilian', 'Argentine', 'Arabian', 'French','German',
                             'Sushi', 'Mexican', 'Vegetarian', 'Thai', 'Indian', 'BBQ', 'Modern Australian', 'Australian',
                              'Mediterranean', 'Korean BBQ', 'Taco','Continental', 'South Indian', 'North Indian', 'Turkish',
                             'Modern Indian', 'American', 'Fast Food'])

selected_cuisines = df1['cuisines'].isin( cuisine_options )
df1 = df1.loc[selected_cuisines, :]
st.sidebar.markdown("""---""")

#Country Filter
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
st.header('🥣 Cuisines')
st.sidebar.markdown("""---""")

with st.container():
    st.header('Best restaurant from popular cuisines')
    col1, col2, col3, col4, col5 = st.columns( 5 )
    with col1:
        st.subheader('Italian')
        df_aux = cuisine_top_rest('Italian')
        st.write( df_aux.iloc[0]['restaurant_name'] )        
        st.write( df_aux.iloc[0]['aggregate_rating'] , '/5.0')
        
    with col2:
        st.subheader('Japanese')
        df_aux = cuisine_top_rest('Japanese')
        st.write( df_aux.iloc[0]['restaurant_name'] )        
        st.write( df_aux.iloc[0]['aggregate_rating'] , '/5.0')
        
    with col3:
        st.subheader('Arabian')
        df_aux = cuisine_top_rest('Arabian')
        st.write( df_aux.iloc[0]['restaurant_name'] )        
        st.write( df_aux.iloc[0]['aggregate_rating'] , '/5.0')
        
    with col4:
        st.subheader('American')
        df_aux = cuisine_top_rest('American')
        st.write( df_aux.iloc[0]['restaurant_name'] )        
        st.write( df_aux.iloc[0]['aggregate_rating'] , '/5.0')
       
    with col5:        
        st.subheader('Fast Food')
        df_aux = cuisine_top_rest('Fast Food')
        st.write( df_aux.iloc[0]['restaurant_name'] )        
        st.write( df_aux.iloc[0]['aggregate_rating'] , '/5.0')

st.markdown("""---""")
    
with st.container():
    col1, col2 = st.columns( 2 )
    with col1:
        st.subheader('Top 10 restaurants overall')
        df_aux = df1.loc[: , ['restaurant_id','restaurant_name','country','city','cuisines','aggregate_rating','votes']].sort_values(by=['aggregate_rating','votes','restaurant_id'] , ascending=[False,False,True]).reset_index().head(10)
        st.dataframe( df_aux , use_container_width=True )
    with col2:
        st.subheader('Top 10 cuisines with the highest mean average cost for two')
        df_aux = df1.loc[:,['cuisines','average_cost_for_two']].groupby('cuisines').mean().sort_values(by='average_cost_for_two' , ascending=False).round(2).reset_index().head(10)
        
        st.dataframe( df_aux, use_container_width=True)

st.markdown("""---""")
    
with st.container():
    col1, col2 = st.columns( 2 )
    with col1:
        st.subheader('Top 10 cuisines')
        fig = cuisines_top(df1)
        st.plotly_chart( fig , use_container_width=True)
        
    with col2:
        st.subheader('Bottom 10 cuisines')
        fig = cuisines_bot(df1)
        st.plotly_chart( fig , use_container_width=True)

