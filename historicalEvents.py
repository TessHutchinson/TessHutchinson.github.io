import pandas as pd
import plotly.express as px

# Load the CSV file
df = pd.read_csv("WorldImportantDates.csv", delimiter=',')

# Handle missing or 'Unknown' values
df['Year'] = df['Year'].replace('Unknown', pd.NA)

# Handle BC dates: Convert BC years to negative numbers
df['Year'] = df['Year'].apply(lambda x: -int(x.split()[0]) if 'BC' in str(x) else int(x))

# Drop rows with missing or invalid years
df = df.dropna(subset=['Year'])

# Sort by 'Year' in ascending order
df = df.sort_values(by='Year', ascending=True)

# Ensure BC dates like -2600 are correctly formatted
df['Formatted Year'] = df['Year'].apply(lambda x: f"{abs(x)} BC" if x < 0 else f"{x} AD")

# Create a mapping for country names
country_mapping = {
    "USA": "United States",
    "UK": "United Kingdom",
    "Russia": "Russia",
    "India": "India",
    "Basra": "Iraq",
}

# Replace country names in the DataFrame
df['Country'] = df['Country'].replace(country_mapping)

# Aggregate data by country and year
country_year_counts = df.groupby(['Country', 'Year']).size().reset_index(name='Incident Count')

# Merge the 'Incident Count' back into the main DataFrame
df = pd.merge(df, country_year_counts, on=['Country', 'Year'], how='left')

# Create the Tile Choropleth Map with hover data, including the formatted year
fig = px.choropleth(
    df,
    locations='Country',  # Ensure this column has the correct country names
    locationmode='country names',
    color='Incident Count',  # Represents the count of incidents
    hover_name='Country',
    hover_data={
        'Type of Event': True,
        'Affected Population': True,
        'Impact': True,
        'Important Person/Group Responsible': True,
        'Outcome': True,
        'Formatted Year': True  # Display the formatted year in the hover tooltip
    },
    title='Historical Events by Country Dates: 2600 BC - 2022',
    animation_frame='Formatted Year',  # Use the formatted year for animation
    color_continuous_scale=px.colors.sequential.Plasma,
)

# Update layout for better readability
fig.update_layout(
    geo=dict(showcoastlines=True, coastlinecolor="RebeccaPurple"),
    coloraxis_colorbar=dict(
        title='Incident Count',
        tickvals=[1, 2, 3, 4, 5],  # Set increments of 1 from 1 to 5
        ticktext=['1', '2', '3', '4', '5'],  # Display labels as numbers
    ),
    coloraxis=dict(cmin=1, cmax=5),  # Set fixed color range from 1 to 5
)

# Save the figure as an HTML file
fig.write_html(r"C:\Users\Figsa\Desktop\myWebsite\historical_events_map.html")
