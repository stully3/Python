"""
Name:      Sean Tully
CS230:      Section 002
Data:       Uber fares dataset
URL:        Link to your web application online

Description:

This program produces 3 queries. One to create a pie chart to show the percentages of rides under each passenger count,
Another that displays a map of all drop off locations in New york city, and one final one that creates a box plot to
show average price based on the different passenger counts.

"""

import pandas as pd
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt


def getPieData(df):
    dfPie = df[['passenger_count']]
    dfValues = dfPie.value_counts()
    dfPie = dfValues.to_frame()
    dfPie.reset_index(inplace=True)
    dfPie.columns = ['numPass', 'count']
    labels = []
    amounts = []
    for index, row in dfPie.iterrows():
        label = row['numPass']
        labels.append(label)
        amount = row['count']
        amounts.append(amount)
    return labels, amounts


def plotPie(l, a):
    fig, ax = plt.subplots()
    ax.pie(a, autopct='%1.1f%%')
    ax.legend(l, loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title('Percentage of Rides by Passenger Count')
    st.header('Pie Chart')
    st.pyplot(fig)


def getBoxData(df, passCount):
    bar = df[['passenger_count', 'fare_amount']]
    bar.index = df['passenger_count']
    bar = bar.loc[[passCount]]
    data = bar['fare_amount']
    data = data.to_frame()
    data2 = data[data['fare_amount'] < 30]
    data2 = data2[data2['fare_amount'] >0]
    return data2


def plotBox(data, passCount):
    fig, ax = plt.subplots()
    ax.boxplot(data)
    ax.set_xlabel(passCount)
    st.pyplot(fig, sys='')




df =pd.read_csv("C:/Users/Tully_Sean/Desktop/pythonProject/uber_8000_sample.csv")

selected_map = st.sidebar.radio("Please select a section you would like to see", ["Background", "Pie Chart", "Map of Ubers", "Box Plot"])
if selected_map == "Background":
    st.title("About this Project")
    st.write("This project aims to provide a variety of data in reference to the Uber Fares Dataset that was provided. The first section produces a pie chart that percentage of the total number of rides for each separate passenger count between 1 and 5. The next section shows a map of the Uber drop-off locations in New York to see the spread. Finally the last section produces a box plot where you can see the average price and range of a ride based on the passenger count selected")
elif selected_map == "Pie Chart":
    st.title('Uber Pie Chart')
    st.write("This pie chart breaks down the percentage of rides by each number of passengers")
    l, a = getPieData(df)
    plotPie(l, a)
elif selected_map == "Map of Ubers":
    st.title("New York Uber Dropoffs")
    st.write("This is a map that shows all of the uber drop-off locations in New York City.")
    # Create custom icons
    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Uber_App_Icon.svg/640px-Uber_App_Icon.svg.png" # Get the custom icon online
    # Format your icon
    icon_data = {
        "url": ICON_URL,
        "width": 100,
        "height": 100,
        "anchorY": 100
        }
    # Add icons to your dataframe
    df["icon_data"]= None
    for i in df.index:
        df["icon_data"][i] = icon_data
    # Create a layer with your custom icon
    icon_layer = pdk.Layer(type="IconLayer",
                           data = df,
                           get_icon='icon_data',
                           get_position='[dropoff_longitude,dropoff_latitude]',
                           get_size=4,
                           size_scale=10,
                           pickable=True)
    # view map
    view_state = pdk.ViewState(
        latitude=df["dropoff_latitude"].mean(),
        longitude=df["dropoff_longitude"].mean(),
        zoom=6,
        pitch=0
        )
    icon_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/navigation-day-v1',
        layers=[icon_layer],
        initial_view_state= view_state)
    st.pydeck_chart(icon_map)
elif selected_map == "Box Plot":
    st.title("Uber Box Plot")
    st.write("This is a Box Plot that shows the average price of an Uber based on how many passengers you expect to have")
    passCount = st.selectbox('Choose Number of Passengers', [1, 2, 3, 4, 5, 6])
    data = getBoxData(df, passCount)
    plotBox(data, passCount)
