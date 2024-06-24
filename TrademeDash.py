import pandas as pd
import plotly.express as px
import streamlit as st
import openpyxl

# Set the page config
st.set_page_config(
    page_title='TradeMe Dashboard by TeamsByDesign',
    page_icon=":bar_chart:",
    layout="wide"
)

# Hide GitHub button
st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data from Excel
df = pd.read_excel(
    io='TradeMeNZ.xlsx',
    engine='openpyxl',
    sheet_name='Clean Data',
    usecols='A:J',
    nrows=63675,
)

# Ensure Property Listing Date is in datetime format
df["Property Listing Date"] = pd.to_datetime(df["Property Listing Date"])

# Sidebar filters
st.sidebar.header("Please Filter Here:")
region = st.sidebar.multiselect(
    "Select the Region:",
    options=df["Region"].unique(),
)

suburb = st.sidebar.multiselect(
    "Select the Suburb:",
    options=df["Suburb"].unique(),
)

num_bedrooms = st.sidebar.multiselect(
    "Select Number of Bedrooms:",
    options=df["Bedrooms"].unique(),
)

num_bathrooms = st.sidebar.multiselect(
    "Select Number of Bathrooms:",
    options=df["Number of Bathrooms"].unique(),
)

# Filter for Property Listing Date
listing_date = st.sidebar.date_input(
    "Select Listing Date Range:",
    value=(df["Property Listing Date"].min(), df["Property Listing Date"].max()),
    min_value=df["Property Listing Date"].min(),
    max_value=df["Property Listing Date"].max()
)

# Handle empty selections
if not region:
    region = df["Region"].unique()
if not suburb:
    suburb = df["Suburb"].unique()
if not num_bedrooms:
    num_bedrooms = df["Bedrooms"].unique()
if not num_bathrooms:
    num_bathrooms = df["Number of Bathrooms"].unique()

# Filter the DataFrame
df_selection = df[
    (df["Region"].isin(region)) &
    (df["Suburb"].isin(suburb)) &
    (df["Bedrooms"].isin(num_bedrooms)) &
    (df["Number of Bathrooms"].isin(num_bathrooms)) &
    (df["Property Listing Date"].between(pd.to_datetime(listing_date[0]), pd.to_datetime(listing_date[1])))
]

# Title and subtitle with style and icons
st.markdown(
    """
    <h1 style='text-align: center; color: white;'>
        TradeMe Dashboard <img src="https://img.icons8.com/color/48/000000/bar-chart.png" alt="bar chart icon"/>
    </h1>
    """,
    unsafe_allow_html=True
)

# Count the number of properties scraped (based on the number of rows)
property_count = len(df_selection)

# Calculate the average rent
average_rent = df_selection["Rent"].mean()

# Display the property count and average rent in cards
st.markdown(
    f"""
    <div style='display: flex; justify-content: space-around;'>
        <div style='background-color: #f0f2f6; padding: 10px; border-radius: 10px; text-align: center; flex: 1; margin: 10px;'>
            <h2 style='color: #333;'>Number of Properties Scraped</h2>
            <p style='font-size: 24px; color: #333;'><b>{property_count}</b></p>
        </div>
        <div style='background-color: #f0f2f6; padding: 10px; border-radius: 10px; text-align: center; flex: 1; margin: 10px;'>
            <h2 style='color: #333;'>Average Rent</h2>
            <p style='font-size: 24px; color: #333;'><b>${average_rent:.2f}</b></p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Style configuration for Plotly charts
plotly_template = "plotly_dark"
plot_bgcolor = 'rgba(0,0,0,0)'
axis_style = dict(showgrid=False)

# Creating a bar chart for Average Rent by Region
average_rent_by_region = (
    df_selection.groupby(by=["Region"]).mean(numeric_only=True)[["Rent"]].sort_values(by="Rent")
)

fig_average_rent = px.bar(
    average_rent_by_region.reset_index(),  # Reset index to use columns in px.bar
    x="Region",
    y="Rent",
    title="Average Rent by Region",
    color_discrete_sequence=["#1f77b4"],  # Set a single color for the bars
    template="presentation",
    text=average_rent_by_region["Rent"].round(0).astype(int).apply(lambda x: f"${x}")  # Add text to the bars with dollar sign
)

fig_average_rent.update_traces(
    texttemplate='%{text}', 
    textposition='inside'  # Position the text inside the bars
)

fig_average_rent.update_layout(
    plot_bgcolor=plot_bgcolor,
    xaxis=axis_style,
    yaxis=axis_style,
    title={
        'text': "<b>Average Rent by Region</b>",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'family': 'Arial, sans-serif', 'size': 16, 'color': 'white'}  # Adjust title font to white
    },
    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="black"  # Adjust font color
    )
)

# Create a bar chart for Average Days on Market by Region
average_days_on_market = (
    df_selection.groupby(by=["Region"]).mean(numeric_only=True)[["Days in the Market"]].sort_values(by="Days in the Market")
)

fig_days_on_market = px.bar(
    average_days_on_market.reset_index(),  # Reset index to use columns in px.bar
    x="Days in the Market",
    y="Region",
    orientation="h",
    title="Average Days on Market by Region",
    color="Days in the Market",  # Use Days in the Market for different colors
    template=plotly_template,
    text=average_days_on_market["Days in the Market"].round(0).astype(int)  # Add text to the bars with no decimal places
)

fig_days_on_market.update_traces(
    texttemplate='%{text}', 
    textposition='inside'  # Position the text inside the bars
)

fig_days_on_market.update_layout(
    plot_bgcolor=plot_bgcolor,
    xaxis=axis_style,
    yaxis=axis_style,
    title={
        'text': "Average Days on Market by Region",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'family': 'Arial, sans-serif', 'size': 16, 'color': 'white'}  # Adjust title font to white
    },
    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="white"  # Adjust font color to white
    ),
    width=1000,  # Set the width to 1000 pixels
    height=600   # Set the height to 600 pixels
)

# Create a line chart for Listing Volume
listing_volume = df_selection["Property Listing Date"].value_counts().sort_index()

fig_listing_volume = px.line(
    x=listing_volume.index,
    y=listing_volume.values,
    title="Listing Volume",
    template=plotly_template,
)

fig_listing_volume.update_traces(
    line=dict(color="white")
)

fig_listing_volume.update_layout(
    plot_bgcolor=plot_bgcolor,
    xaxis=axis_style,
    yaxis=axis_style,
    title={
        'text': "Listing Volume",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'family': 'Arial, sans-serif', 'size': 16, 'color': 'white'}  # Adjust title font to white
    },
    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="white"  # Adjust font color to white
    )
)

# Display the bar charts and line chart
st.plotly_chart(fig_average_rent)
st.plotly_chart(fig_days_on_market)
st.plotly_chart(fig_listing_volume)
