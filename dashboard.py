import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ------------------
# Loading csv's
# ------------------

BASE_DIR = os.path.dirname(__file__)

flights = pd.read_csv(os.path.join(BASE_DIR, "assets", "flights.csv"))
fuel_consumption = pd.read_csv(os.path.join(BASE_DIR, "assets", "fuel_consumption.csv"))
passenger_stats = pd.read_csv(os.path.join(BASE_DIR, "assets", "passenger_stats.csv"))
weather_conditions = pd.read_csv(os.path.join(BASE_DIR, "assets", "weather_conditions.csv"))
employee_stats = pd.read_csv(os.path.join(BASE_DIR, "assets", "employee_stats.csv"))
baggage_handling = pd.read_csv(os.path.join(BASE_DIR, "assets", "baggage_handling.csv"))

# ------------------
# Dashboard
# ------------------
st.title("✈️ Airplane Operations Dashboard")
st.markdown('<style>div.block-container{padding-top:50px;}</style>',unsafe_allow_html=True)
datasets = ["Flight","Fuel Consumption","Passenger Stats","Weather Conditions","Employee Stats","Baggage Handling"]
st.divider()
# ____SideBar____

with st.sidebar:
    title = st.title("📃 Select Dataset")
    selected_dataset = st.selectbox(
        "Choose a dataset",
        datasets,
        label_visibility="collapsed"
    )
    st.success(f"{selected_dataset} dataset is selected")

#---------------
# Flights
#---------------
if selected_dataset == "Flight":
    st.header("✈️ Flights Dataset")
    st.divider()
    total_flights = len(flights)
    on_time = (flights["status"] == "On Time").sum() / total_flights * 100
    delayed = (flights["status"] == "Delayed").sum() / total_flights * 100
    cancelled = (flights["status"] == "Cancelled").sum() / total_flights * 100
    st.header("📊 Visualizations",divider=True,width='content')
    #------------------------------------------------------
    # Bar plot showing ontime,delayed and cancelled filghts
    #------------------------------------------------------
    status_counts = flights.groupby('status').size().reset_index(name="counts")
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(10,9.5))
        sns.barplot(data=status_counts,x='status',y='counts',ax=ax,palette='coolwarm')
        ax.set_title("Flight Status Distribution",size=20)
        ax.set_xlabel("Status",size = 20)
        ax.set_ylabel("Counts",size = 20)
        st.pyplot(fig)
    #------------------------------------------------------
    # Bar plot showing number of flights per airline
    #------------------------------------------------------
    with col2:
        fig, ax = plt.subplots()
        sns.countplot(data=flights, x="airline", hue="airline", palette="coolwarm", legend=False)
        ax.set_title("Number of Flights per Airline",size = 20,color = 'purple')
        ax.set_xlabel("Airline",size = 15)
        ax.set_ylabel("Number of Flights",size = 15)
        for label in ax.get_xticklabels():
            label.set_rotation(90)
            label.set_color("blue")
        ax.set_yticklabels(ax.get_yticklabels(),color = 'blue')
        st.pyplot(fig)
    st.divider()
    st.header("🔢 Metrics",divider=True,width='content')
    total_flights = flights["status"].count()
    st.subheader(f"Total Flights : {total_flights}")
    st.subheader(f"Flights on time : {on_time}%")
    st.subheader(f"Flights delayed : {delayed}%")
    st.subheader(f"Flights cancelled : {cancelled}%")

#-----------------
# Fuel Consumption
#-----------------
elif selected_dataset == "Fuel Consumption":
    st.header("⛽ Fuel Consumption Dataset")
    st.divider()
    st.header("📊 Visualization",divider=True,width='content')
    #--------------
    # Visualization
    #--------------
    merged_df = fuel_consumption.merge(flights[['airline','flight_id']],on='flight_id')
    grouped_df = merged_df.groupby(['airline'])['fuel_liters'].sum().reset_index()
    grouped_df['fuel_liters'] = grouped_df["fuel_liters"]/100000
    COl1,COl2 = st.columns(2)
    with COl1:
        fig,ax = plt.subplots()
        sns.barplot(data=grouped_df,x='airline',y='fuel_liters',palette='Set2')
        ax.set_title("Fuel used by an Airline",size = 20)
        ax.set_xlabel("Airline",size = 18)
        ax.set_ylabel("Fuel (liters in Million)",size = 15)
        ax.set_xticklabels(ax.get_xticklabels(),rotation = 45)
        st.pyplot(fig)
    #--------
    # Metrics
    # -------
    st.divider()
    st.subheader("🔢Metrics",width='content',divider=True)
    total_cost_of_fuel = fuel_consumption['fuel_cost_usd'].sum()
    total_fuel = fuel_consumption['fuel_liters'].sum()
    st.subheader(f"Total Fuel Cost : {total_cost_of_fuel} $")
    st.subheader(f"Total Fuel : {total_fuel} liters")
    min_fuel_used = grouped_df["fuel_liters"].min()
    min_fuel_usage_airline = grouped_df.loc[grouped_df["fuel_liters"] == min_fuel_used,'airline'].iloc[0]
    st.subheader(f"{min_fuel_usage_airline} has used the minimum fuel : {min_fuel_used} million liters")

#-----------------
# Passenger Stats
#-----------------
elif selected_dataset == "Passenger Stats":
    st.header("💺 Passenger Stats Dataset")
    st.divider()
    st.header("📊 Visualization",divider=True,width='content')
    #--------------
    # Visualization
    #--------------
    passenger_stats['date'] = pd.to_datetime(passenger_stats["date"])
    passenger_stats['Date'] = passenger_stats["date"].dt.date
    Col1,Col2 = st.columns(2)
    with Col1:
        st.subheader("Domestic vs International Passengers per Day",divider=True,width='content')
        st.line_chart(data=passenger_stats,
                      x='Date',
                      y=["domestic", "international"],
                      x_label='Date',
                      y_label="Passengers",
                      color=["#ffaa0088","#a6ff008c"])
    #-------------------------
    # Monthly Passenger Counts
    #-------------------------
    passenger_stats["total_passengers"] = passenger_stats['domestic'] + passenger_stats['international']
    passenger_stats["month"] = passenger_stats["date"].dt.month_name()
    passenger_per_months = passenger_stats.groupby('month')['total_passengers'].sum().reset_index()
    with Col2:
        st.subheader("Total Passengers Per Month",divider=True,width='content')
        st.bar_chart(data=passenger_per_months,
                     x='month',
                     y='total_passengers',
                     x_label='Months',
                     y_label='Total Passenger',
                     color="#1effd6be")
    #--------
    # Metrics
    # -------
    st.divider()
    st.subheader("🔢Metrics",width='content',divider=True)
    st.subheader(f"Total Passengers in 2024 : {passenger_stats['total_passengers'].sum()} Passengers")
    st.subheader(f"Total Domestic Passengers in 2024 : {passenger_stats['domestic'].sum()} Passengers")
    st.subheader(f"Total International Passengers in 2024 : {passenger_stats['international'].sum()} Passengers")

#-----------------
# Weather Condtions
#-----------------
elif selected_dataset == "Weather Conditions":
    st.header("🌦️ Weather Conditions Dataset")
    st.divider()
    st.snow()

    # grouping data: 
    grouped_visibility_condition = weather_conditions.groupby('condition')['visibility_km'].mean().round(2)
    grouped_windspeed_condition = weather_conditions.groupby('condition')['wind_speed_kmh'].mean().round(2)
    grouped_temperature_c_condition = weather_conditions.groupby('condition')['temperature_c'].mean().round(2)
    #--------------
    # Visualization
    #--------------
    st.header("📊 Visualization",divider=True,width='content')
    coL1,coL2 = st.columns(2)
    with coL1:
        st.subheader("👁️ Visibility in Different Weather Conditions")
        st.bar_chart(data=grouped_visibility_condition,
                     color="#9B76F2B2",
                     x_label="Weather Condition",
                     y_label="Visibility (km)")
    with coL2:
        st.subheader("💨 Average Wind Speed in Different Weather Conditions")
        st.bar_chart(data=grouped_windspeed_condition,
                     x_label="Weather Condition",
                     y_label="Wind Speed (kmh)",
                     color="#4a9edeb1")
    st.subheader("💨 Average Temprature (°C) in Different Weather Conditions")
    st.bar_chart(data=grouped_temperature_c_condition,
                 x_label="Weather Condition",
                 y_label="Temprature (°C)",
                 color="#6b2748dc")
    #--------
    # Metrics
    # -------
    st.divider()
    st.subheader("🔢Metrics",width='content',divider=True)
    highest_visibility = weather_conditions['visibility_km'].max()
    highest_visibility_day = weather_conditions.loc[weather_conditions['visibility_km'] == highest_visibility,'date'].values[0]
    highest_windspeed = weather_conditions['wind_speed_kmh'].max()
    highest_windspeed_day = weather_conditions.loc[weather_conditions['wind_speed_kmh'] == highest_windspeed,'date'].values[0]
    highest_temprature = weather_conditions['temperature_c'].max()
    highest_temprature_day = weather_conditions.loc[weather_conditions['temperature_c'] == highest_temprature,'date'].values[0] 
    st.subheader(f"Highest Visibility Day : {highest_visibility_day}")
    st.subheader(f"Highest Wind Speed Day : {highest_windspeed_day}")
    st.subheader(f"Highest Temprature Day : {highest_temprature_day}")

    #-----------------
    # Fuel Consumption
    #-----------------
elif selected_dataset == "Employee Stats":
    st.header("👨🏻‍💼 Employee Stats")
    st.divider()
    st.header("📊 Visualization",divider=True,width='content')
    # Grouping some data
    employees_of_each_role = employee_stats.groupby('role')['employee_id'].count().reset_index()
    employees_of_each_role.rename(columns = {'employee_id': 'Number of Employees','role': 'Role'}, inplace=True)
    avg_rating_of_each_role = employee_stats.groupby('role')['rating'].mean()
    cOl1,cOl2 = st.columns(2)
    #-----------------------------------------------
    # Bar graph sohwing total employees in each role
    #-----------------------------------------------
    with cOl1:
        st.subheader("Total Employees in Each Role",divider=True,width='content')
        st.bar_chart(data=employees_of_each_role,x='Role',y='Number of Employees',color="#92fcf08b")
    #--------------------------------------------------------
    # Bar graph sohwing employees average rating of each role
    #--------------------------------------------------------
    with cOl2:
        st.subheader("Average Rating of Each Role",divider=True,width='content')
        st.bar_chart(data=avg_rating_of_each_role,color="#5dfbac8c")

    #--------
    # Metrics
    #--------
    st.divider()
    st.subheader("🔢Metrics",width='content',divider=True)
    st.subheader("Total Employees in Each Role",divider=True,width='content')
    st.dataframe(employees_of_each_role,hide_index=True)
    st.subheader("Average Rating of Each Role",divider=True,width='content')
    st.dataframe(avg_rating_of_each_role,use_container_width=True)
elif selected_dataset == "Baggage Handling":
    st.header("🧳 Baggage Handling")
    st.divider()
    st.header("📊 Visualization",divider=True,width='content')
    #------------------------------
    # Baggages Checked-in vs Loaded
    #------------------------------
    st.subheader("🧳 Baggages Checked-in vs Loaded",divider=True,width='content')
    st.bar_chart(data=baggage_handling,x='checked_in',y='loaded',color="#7fff5cae")
    #------------------------------
    # Baggages Checked-in vs Lost
    #------------------------------
    st.subheader("🧳 Baggages Checked-in vs Lost",divider=True,width='content')
    st.bar_chart(data=baggage_handling,x='checked_in',y='lost',color="#c37584")
    #-------------------------------
    # Baggages Checked-in vs Delayed
    #-------------------------------
    st.subheader("🧳 Baggages Checked-in vs Delayed",divider=True,width='content')
    st.bar_chart(data=baggage_handling,x='checked_in',y='delayed',color="#29ffbba2")

    #--------
    # Metrics
    #--------
    st.divider()
    st.subheader("🔢Metrics",width='content',divider=True)
    st.subheader(f"Total Number of Lost Baggages : {baggage_handling['lost'].sum()}")
    st.subheader(f"Total Number of Delayed Baggages : {baggage_handling['delayed'].sum()}")
    st.subheader(f"Total Number of Loaded Baggages : {baggage_handling['loaded'].sum()}")
    st.subheader(f"Total Number of Checked-In Baggages : {baggage_handling['checked_in'].sum()}")

