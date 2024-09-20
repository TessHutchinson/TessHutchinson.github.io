import pandas as pd
import plotly.express as px

# Load the CSV file, ensure the delimiter is correct
df = pd.read_csv("WorldImportantDates.csv", delimiter=',')


# Handle missing values for 'Date', 'Month', and 'Year'
# Replace 'Unknown' values with NaN for easier handling
df['Date'] = df['Date'].replace('Unknown', pd.NA)
df['Month'] = df['Month'].replace('Unknown', pd.NA)
df['Year'] = df['Year'].replace('Unknown', pd.NA)

# Handle BC dates by converting 'Year' to numeric, where 'BC' should become negative numbers
df['Year'] = df['Year'].apply(lambda x: -int(x.split()[0]) if 'BC' in str(x) else x)

# Create a 'Full Date' column by combining 'Date', 'Month', and 'Year'
df['Full Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].fillna(1).astype(str) + '-' + df['Date'].fillna(1).astype(str), format='%Y-%m-%d', errors='coerce')

# Drop any rows where 'Full Date' could not be parsed
df = df.dropna(subset=['Full Date'])

# Create a scatter plot for the timeline
fig = px.scatter(
    df,
    x='Full Date',
    y='Impact', 
    hover_name='Name of Incident',  
    color='Type of Event',  
    title='Historical Events Timeline',
)

# Update layout for better readability
fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Historical Events',
    showlegend=True,
)

# Save the figure as an HTML file
fig.write_html(r"C:\Users\Figsa\Desktop\myWebsite\historical_events_graph.html")



