from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Load data
DATA_PATH = Path(__file__).parent / "worldometer_coronavirus_daily_data.csv"
df = pd.read_csv(DATA_PATH)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Fill missing values with zeros
df = df.fillna(0)

# Create array of unique countries
countries = sorted(df['country'].unique().tolist())
print(f"Total countries in dataset: {len(countries)}")
print(f"Data period: {df['date'].min()} - {df['date'].max()}")

# Comprehensive country coordinates mapping (all major countries from the dataset)
country_coords = {
    'Afghanistan': {'lat': 33.9391, 'lon': 67.7100},
    'Albania': {'lat': 41.1533, 'lon': 20.1683},
    'Algeria': {'lat': 28.0339, 'lon': 1.6596},
    'Andorra': {'lat': 42.5063, 'lon': 1.5218},
    'Angola': {'lat': -11.2027, 'lon': 17.8739},
    'Antigua and Barbuda': {'lat': 17.0608, 'lon': -61.7964},
    'Argentina': {'lat': -38.4161, 'lon': -63.6167},
    'Armenia': {'lat': 40.0691, 'lon': 45.0382},
    'Australia': {'lat': -25.2744, 'lon': 133.7751},
    'Austria': {'lat': 47.5162, 'lon': 14.5501},
    'Azerbaijan': {'lat': 40.1431, 'lon': 47.5769},
    'Bahamas': {'lat': 25.0343, 'lon': -77.3963},
    'Bahrain': {'lat': 26.0667, 'lon': 50.5577},
    'Bangladesh': {'lat': 23.6850, 'lon': 90.3563},
    'Barbados': {'lat': 13.1939, 'lon': -59.5432},
    'Belarus': {'lat': 53.7098, 'lon': 27.9534},
    'Belgium': {'lat': 50.5039, 'lon': 4.4699},
    'Belize': {'lat': 17.1899, 'lon': -88.4976},
    'Benin': {'lat': 9.3077, 'lon': 2.3158},
    'Bhutan': {'lat': 27.5142, 'lon': 90.4336},
    'Bolivia': {'lat': -16.2902, 'lon': -63.5887},
    'Bosnia and Herzegovina': {'lat': 43.9159, 'lon': 17.6791},
    'Botswana': {'lat': -22.3285, 'lon': 24.6849},
    'Brazil': {'lat': -14.2350, 'lon': -51.9253},
    'Brunei': {'lat': 4.5353, 'lon': 114.7277},
    'Bulgaria': {'lat': 42.7339, 'lon': 25.4858},
    'Burkina Faso': {'lat': 12.2383, 'lon': -1.5616},
    'Burundi': {'lat': -3.3731, 'lon': 29.9189},
    'Cambodia': {'lat': 12.5657, 'lon': 104.9910},
    'Cameroon': {'lat': 7.3697, 'lon': 12.3547},
    'Canada': {'lat': 56.1304, 'lon': -106.3468},
    'Cape Verde': {'lat': 16.5388, 'lon': -23.0418},
    'Central African Republic': {'lat': 6.6111, 'lon': 20.9394},
    'Chad': {'lat': 15.4542, 'lon': 18.7322},
    'Chile': {'lat': -35.6751, 'lon': -71.5430},
    'China': {'lat': 35.8617, 'lon': 104.1954},
    'Colombia': {'lat': 4.5709, 'lon': -74.2973},
    'Comoros': {'lat': -11.6455, 'lon': 43.3333},
    'Congo': {'lat': -0.2280, 'lon': 15.8277},
    'Costa Rica': {'lat': 9.7489, 'lon': -83.7534},
    'Croatia': {'lat': 45.1000, 'lon': 15.2000},
    'Cuba': {'lat': 21.5218, 'lon': -77.7812},
    'Cyprus': {'lat': 35.1264, 'lon': 33.4299},
    'Czechia': {'lat': 49.8175, 'lon': 15.4730},
    'Denmark': {'lat': 56.2639, 'lon': 9.5018},
    'Djibouti': {'lat': 11.8251, 'lon': 42.5903},
    'Dominica': {'lat': 15.4150, 'lon': -61.3710},
    'Dominican Republic': {'lat': 18.7357, 'lon': -70.1627},
    'Ecuador': {'lat': -1.8312, 'lon': -78.1834},
    'Egypt': {'lat': 26.8206, 'lon': 30.8025},
    'El Salvador': {'lat': 13.7942, 'lon': -88.8965},
    'Equatorial Guinea': {'lat': 1.6508, 'lon': 10.2679},
    'Eritrea': {'lat': 15.1794, 'lon': 39.7823},
    'Estonia': {'lat': 58.5953, 'lon': 25.0136},
    'Eswatini': {'lat': -26.5225, 'lon': 31.4659},
    'Ethiopia': {'lat': 9.1450, 'lon': 40.4897},
    'Fiji': {'lat': -17.7134, 'lon': 178.0650},
    'Finland': {'lat': 61.9241, 'lon': 25.7482},
    'France': {'lat': 46.2276, 'lon': 2.2137},
    'Gabon': {'lat': -0.8037, 'lon': 11.6094},
    'Gambia': {'lat': 13.4432, 'lon': -15.3101},
    'Georgia': {'lat': 42.3154, 'lon': 43.3569},
    'Germany': {'lat': 51.1657, 'lon': 10.4515},
    'Ghana': {'lat': 7.9465, 'lon': -1.0232},
    'Greece': {'lat': 39.0742, 'lon': 21.8243},
    'Grenada': {'lat': 12.1165, 'lon': -61.6790},
    'Guatemala': {'lat': 15.7835, 'lon': -90.2308},
    'Guinea': {'lat': 9.9456, 'lon': -9.6966},
    'Guinea-Bissau': {'lat': 11.8037, 'lon': -15.1804},
    'Guyana': {'lat': 4.8604, 'lon': -58.9302},
    'Haiti': {'lat': 18.9712, 'lon': -72.2852},
    'Honduras': {'lat': 15.2000, 'lon': -86.2419},
    'Hungary': {'lat': 47.1625, 'lon': 19.5033},
    'Iceland': {'lat': 64.9631, 'lon': -19.0208},
    'India': {'lat': 20.5937, 'lon': 78.9629},
    'Indonesia': {'lat': -0.7893, 'lon': 113.9213},
    'Iran': {'lat': 32.4279, 'lon': 53.6880},
    'Iraq': {'lat': 33.2232, 'lon': 43.6793},
    'Ireland': {'lat': 53.4129, 'lon': -8.2439},
    'Israel': {'lat': 31.0461, 'lon': 34.8516},
    'Italy': {'lat': 41.8719, 'lon': 12.5674},
    'Jamaica': {'lat': 18.1096, 'lon': -77.2975},
    'Japan': {'lat': 36.2048, 'lon': 138.2529},
    'Jordan': {'lat': 30.5852, 'lon': 36.2384},
    'Kazakhstan': {'lat': 48.0196, 'lon': 66.9237},
    'Kenya': {'lat': -0.0236, 'lon': 37.9062},
    'Kuwait': {'lat': 29.3117, 'lon': 47.4818},
    'Kyrgyzstan': {'lat': 41.2044, 'lon': 74.7661},
    'Laos': {'lat': 19.8563, 'lon': 102.4955},
    'Latvia': {'lat': 56.8796, 'lon': 24.6032},
    'Lebanon': {'lat': 33.8547, 'lon': 35.8623},
    'Lesotho': {'lat': -29.6100, 'lon': 28.2336},
    'Liberia': {'lat': 6.4281, 'lon': -9.4295},
    'Libya': {'lat': 26.3351, 'lon': 17.2283},
    'Liechtenstein': {'lat': 47.1660, 'lon': 9.5554},
    'Lithuania': {'lat': 55.1694, 'lon': 23.8813},
    'Luxembourg': {'lat': 49.8153, 'lon': 6.1296},
    'Madagascar': {'lat': -18.7669, 'lon': 46.8691},
    'Malawi': {'lat': -13.2543, 'lon': 34.3015},
    'Malaysia': {'lat': 4.2105, 'lon': 101.9758},
    'Maldives': {'lat': 3.2028, 'lon': 73.2207},
    'Mali': {'lat': 17.5707, 'lon': -3.9962},
    'Malta': {'lat': 35.9375, 'lon': 14.3754},
    'Mauritania': {'lat': 21.0079, 'lon': -10.9408},
    'Mauritius': {'lat': -20.3484, 'lon': 57.5522},
    'Mexico': {'lat': 23.6345, 'lon': -102.5528},
    'Moldova': {'lat': 47.4116, 'lon': 28.3699},
    'Monaco': {'lat': 43.7384, 'lon': 7.4246},
    'Mongolia': {'lat': 46.8625, 'lon': 103.8467},
    'Montenegro': {'lat': 42.7087, 'lon': 19.3744},
    'Morocco': {'lat': 31.7917, 'lon': -7.0926},
    'Mozambique': {'lat': -18.6657, 'lon': 35.5296},
    'Myanmar': {'lat': 21.9162, 'lon': 95.9560},
    'Namibia': {'lat': -22.9576, 'lon': 18.4904},
    'Nepal': {'lat': 28.3949, 'lon': 84.1240},
    'Netherlands': {'lat': 52.1326, 'lon': 5.2913},
    'New Zealand': {'lat': -40.9006, 'lon': 174.8860},
    'Nicaragua': {'lat': 12.8654, 'lon': -85.2072},
    'Niger': {'lat': 17.6078, 'lon': 8.0817},
    'Nigeria': {'lat': 9.0820, 'lon': 8.6753},
    'North Macedonia': {'lat': 41.6086, 'lon': 21.7453},
    'Norway': {'lat': 60.4720, 'lon': 8.4689},
    'Oman': {'lat': 21.4735, 'lon': 55.9754},
    'Pakistan': {'lat': 30.3753, 'lon': 69.3451},
    'Panama': {'lat': 8.5380, 'lon': -80.7821},
    'Papua New Guinea': {'lat': -6.3150, 'lon': 143.9555},
    'Paraguay': {'lat': -23.4425, 'lon': -58.4438},
    'Peru': {'lat': -9.1900, 'lon': -75.0152},
    'Philippines': {'lat': 12.8797, 'lon': 121.7740},
    'Poland': {'lat': 51.9194, 'lon': 19.1451},
    'Portugal': {'lat': 39.3999, 'lon': -8.2245},
    'Qatar': {'lat': 25.3548, 'lon': 51.1839},
    'Romania': {'lat': 45.9432, 'lon': 24.9668},
    'Russia': {'lat': 61.5240, 'lon': 105.3188},
    'Rwanda': {'lat': -1.9403, 'lon': 29.8739},
    'Saint Kitts and Nevis': {'lat': 17.3578, 'lon': -62.7830},
    'Saint Lucia': {'lat': 13.9094, 'lon': -60.9789},
    'Saint Vincent and the Grenadines': {'lat': 12.9843, 'lon': -61.2872},
    'Samoa': {'lat': -13.7590, 'lon': -172.1046},
    'San Marino': {'lat': 43.9424, 'lon': 12.4578},
    'Sao Tome and Principe': {'lat': 0.1864, 'lon': 6.6131},
    'Saudi Arabia': {'lat': 23.8859, 'lon': 45.0792},
    'Senegal': {'lat': 14.4974, 'lon': -14.4524},
    'Serbia': {'lat': 44.0165, 'lon': 21.0059},
    'Seychelles': {'lat': -4.6796, 'lon': 55.4920},
    'Sierra Leone': {'lat': 8.4606, 'lon': -11.7799},
    'Singapore': {'lat': 1.3521, 'lon': 103.8198},
    'Slovakia': {'lat': 48.6690, 'lon': 19.6990},
    'Slovenia': {'lat': 46.1512, 'lon': 14.9955},
    'Solomon Islands': {'lat': -9.6457, 'lon': 160.1562},
    'Somalia': {'lat': 5.1521, 'lon': 46.1996},
    'South Africa': {'lat': -30.5595, 'lon': 22.9375},
    'South Korea': {'lat': 35.9078, 'lon': 127.7669},
    'South Sudan': {'lat': 6.8770, 'lon': 31.3070},
    'Spain': {'lat': 40.4637, 'lon': -3.7492},
    'Sri Lanka': {'lat': 7.8731, 'lon': 80.7718},
    'Sudan': {'lat': 12.8628, 'lon': 30.2176},
    'Suriname': {'lat': 3.9193, 'lon': -56.0278},
    'Sweden': {'lat': 60.1282, 'lon': 18.6435},
    'Switzerland': {'lat': 46.8182, 'lon': 8.2275},
    'Syria': {'lat': 34.8021, 'lon': 38.9968},
    'Taiwan': {'lat': 23.6978, 'lon': 120.9605},
    'Tajikistan': {'lat': 38.8610, 'lon': 71.2761},
    'Tanzania': {'lat': -6.3690, 'lon': 34.8888},
    'Thailand': {'lat': 15.8700, 'lon': 100.9925},
    'Timor-Leste': {'lat': -8.8742, 'lon': 125.7275},
    'Togo': {'lat': 8.6195, 'lon': 0.8248},
    'Trinidad and Tobago': {'lat': 10.6918, 'lon': -61.2225},
    'Tunisia': {'lat': 33.8869, 'lon': 9.5375},
    'Turkey': {'lat': 38.9637, 'lon': 35.2433},
    'Uganda': {'lat': 1.3733, 'lon': 32.2903},
    'Ukraine': {'lat': 48.3794, 'lon': 31.1656},
    'United Arab Emirates': {'lat': 23.4241, 'lon': 53.8478},
    'United Kingdom': {'lat': 55.3781, 'lon': -3.4360},
    'United States': {'lat': 37.0902, 'lon': -95.7129},
    'USA': {'lat': 37.0902, 'lon': -95.7129},  # Alias for United States
    'Uruguay': {'lat': -32.5228, 'lon': -55.7658},
    'Uzbekistan': {'lat': 41.3775, 'lon': 64.5853},
    'Vanuatu': {'lat': -15.3767, 'lon': 166.9592},
    'Venezuela': {'lat': 6.4238, 'lon': -66.5897},
    'Viet Nam': {'lat': 14.0583, 'lon': 108.2772},
    'Yemen': {'lat': 15.5527, 'lon': 48.5164},
    'Zambia': {'lat': -13.1339, 'lon': 27.8493},
    'Zimbabwe': {'lat': -19.0154, 'lon': 29.1549},
}

# Function to format Y-axis values (1000 -> 1K, 200000 -> 200K)
def format_y_axis(value, pos):
    if value >= 1000:
        return f'{int(value/1000)}K'
    return f'{int(value)}'

# Function to create COVID-19 charts for a specific country or world using Plotly
def create_covid_charts(country_name, data_type='New'):
    """
    Creates two interactive time series charts for a given country or world using Plotly:
    1. New/Cumulative Positive Cases over time
    2. New/Cumulative Deaths over time
    
    Parameters:
    country_name (str): Name of the country to analyze or 'World' for global statistics
    data_type (str): 'New' or 'Cumulative' - type of data to display
    
    Returns:
    plotly figure object
    """
    # Filter data for the specific country or aggregate for world
    if country_name == 'World':
        # Aggregate data for all countries by date
        country_data = df.groupby('date').agg({
            'daily_new_cases': 'sum',
            'daily_new_deaths': 'sum',
            'cumulative_total_cases': 'sum',
            'cumulative_total_deaths': 'sum'
        }).reset_index()
        country_data = country_data.sort_values('date')
    else:
        # Filter data for the specific country
        country_data = df[df['country'] == country_name].copy()
        country_data = country_data.sort_values('date')
    
    # Select columns based on data_type
    if data_type == 'New':
        cases_column = 'daily_new_cases'
        deaths_column = 'daily_new_deaths'
        title_cases = 'New Positive Cases'
        title_deaths = 'New Deaths'
    else:  # Cumulative
        cases_column = 'cumulative_total_cases'
        deaths_column = 'cumulative_total_deaths'
        title_cases = 'Cumulative Positive Cases'
        title_deaths = 'Cumulative Deaths'
    
    # Get last day values and calculate percentage change
    last_cases = country_data[cases_column].iloc[-1] if len(country_data) > 0 else 0
    prev_cases = country_data[cases_column].iloc[-2] if len(country_data) > 1 else 0
    cases_change = ((last_cases - prev_cases) / prev_cases * 100) if prev_cases != 0 else 0
    
    last_deaths = country_data[deaths_column].iloc[-1] if len(country_data) > 0 else 0
    prev_deaths = country_data[deaths_column].iloc[-2] if len(country_data) > 1 else 0
    deaths_change = ((last_deaths - prev_deaths) / prev_deaths * 100) if prev_deaths != 0 else 0
    
    # Create subplots
    from plotly.subplots import make_subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(title_cases, title_deaths),
        vertical_spacing=0.15
    )
    
    # Plot 1: Cases (New or Cumulative)
    fig.add_trace(
        go.Scatter(
            x=country_data['date'],
            y=country_data[cases_column],
            fill='tozeroy',
            fillcolor='rgba(0, 180, 216, 0.7)',
            line=dict(color='#0077b6', width=1),
            mode='lines',
            name=title_cases,
            customdata=country_data[cases_column],
            hovertemplate=(
                '<b>%{x|%b %d, %Y}</b><br>'
                f'{title_cases}: ' + '%{customdata:,.0f}'
                '<extra></extra>'
            ),
            hoveron='points+fills'
        ),
        row=1, col=1
    )
    
    # Plot 2: Deaths (New or Cumulative)
    fig.add_trace(
        go.Scatter(
            x=country_data['date'],
            y=country_data[deaths_column],
            fill='tozeroy',
            fillcolor='rgba(0, 180, 216, 0.7)',
            line=dict(color='#0077b6', width=1),
            mode='lines',
            name=title_deaths,
            customdata=country_data[deaths_column],
            hovertemplate=(
                '<b>%{x|%b %d, %Y}</b><br>'
                f'{title_deaths}: ' + '%{customdata:,.0f}'
                '<extra></extra>'
            ),
            hoveron='points+fills'
        ),
        row=2, col=1
    )
    
    # Update layout for both subplots
    fig.update_xaxes(
        tickformat='%b',  # Month abbreviation (Jan, Feb, Mar...)
        showgrid=False,
        zeroline=False,
        showline=False,
        row=1, col=1
    )
    fig.update_xaxes(
        tickformat='%b',
        showgrid=False,
        zeroline=False,
        showline=False,
        row=2, col=1
    )
    
    # Format Y-axis to show K for thousands
    fig.update_yaxes(
        tickformat=',.0f',
        showgrid=False,
        zeroline=False,
        showline=False,
        row=1, col=1
    )
    fig.update_yaxes(
        tickformat=',.0f',
        showgrid=False,
        zeroline=False,
        showline=False,
        row=2, col=1
    )
    
    # Add annotations for current values and percentage change
    arrow_cases = '▲' if cases_change > 0 else '▼'
    color_cases = 'red' if cases_change > 0 else 'green'
    
    arrow_deaths = '▲' if deaths_change > 0 else '▼'
    color_deaths = 'red' if deaths_change > 0 else 'green'
    
    fig.add_annotation(
        text=f'<b>{int(last_cases):,}</b>',
        xref="x domain", yref="y domain",
        x=0.02, y=0.98,
        showarrow=False,
        font=dict(size=20, color='black'),
        align='left',
        xanchor='left',
        yanchor='top',
        row=1, col=1
    )
    
    fig.add_annotation(
        text=f'{arrow_cases} {abs(cases_change):.1f}% vs previous day',
        xref="x domain", yref="y domain",
        x=0.02, y=0.88,
        showarrow=False,
        font=dict(size=10, color=color_cases),
        align='left',
        xanchor='left',
        yanchor='top',
        row=1, col=1
    )
    
    fig.add_annotation(
        text=f'<b>{int(last_deaths):,}</b>',
        xref="x2 domain", yref="y2 domain",
        x=0.02, y=0.98,
        showarrow=False,
        font=dict(size=20, color='black'),
        align='left',
        xanchor='left',
        yanchor='top',
        row=2, col=1
    )
    
    fig.add_annotation(
        text=f'{arrow_deaths} {abs(deaths_change):.1f}% vs previous day',
        xref="x2 domain", yref="y2 domain",
        x=0.02, y=0.88,
        showarrow=False,
        font=dict(size=10, color=color_deaths),
        align='left',
        xanchor='left',
        yanchor='top',
        row=2, col=1
    )
    
    # Update overall layout
    fig.update_layout(
        title_text=f'COVID-19 Statistics for {country_name}',
        title_font_size=16,
        title_font_family='Arial',
        title_font_color='black',
        showlegend=False,
        height=600,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=80, b=50),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    
    return fig

# Function to create country ranking bar chart
def create_country_ranking(data_type, metric_type, top_n=20):
    # Define the target date for 'New' data (May 14, 2022)
    target_date = pd.to_datetime('2022-05-14')
    
    # Select appropriate column based on parameters
    if data_type == 'Cumulative' and metric_type == 'Cases':
        column = 'cumulative_total_cases'
        title = 'Cumulative Positive Cases'
    elif data_type == 'Cumulative' and metric_type == 'Deaths':
        column = 'cumulative_total_deaths'
        title = 'Cumulative Deaths'
    elif data_type == 'New' and metric_type == 'Cases':
        column = 'daily_new_cases'
        title = 'New Positive Cases'
    else:  # New Deaths
        column = 'daily_new_deaths'
        title = 'New Deaths'
    
    # Filter data based on data_type
    if data_type == 'New':
        # Get data for the specific date (May 14, 2022)
        filtered_data = df[df['date'] == target_date].copy()
    else:
        # For cumulative, get the latest data for each country
        filtered_data = df.sort_values('date').groupby('country').last().reset_index()
    
    # Get top N countries
    top_countries = filtered_data.nlargest(top_n, column)[['country', column]]
    top_countries = top_countries.sort_values(column, ascending=True)  # Ascending for horizontal bar
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top_countries['country'],
        x=top_countries[column],
        orientation='h',
        marker=dict(
            color='#00b4d8',
            line=dict(color='rgba(0, 119, 182, 0)', width=3)  # Transparent border by default
        ),
        text=top_countries[column].apply(lambda x: f'{int(x):,}'),
        textposition='outside',
        textfont=dict(size=10),
        hovertemplate='<b>%{y}</b><br>%{x:,.0f}<extra></extra>',
        customdata=top_countries['country']  # Add country name to customdata
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=14, family='Arial', color='black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            showgrid=False,
            showticklabels=True,
            zeroline=False,
            showline=False
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            tickfont=dict(size=10)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600,
        margin=dict(l=80, r=30, t=50, b=30),  # Increased right margin for text labels
        showlegend=False,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    
    return fig

# Function to create interactive world map with COVID-19 data using Mapbox
def create_world_map(data_type, metric_type):
    """
    Creates an interactive world map showing COVID-19 data by country using Mapbox
    
    Parameters:
    data_type (str): 'New' or 'Cumulative'
    metric_type (str): 'Cases' or 'Deaths'
    
    Returns:
    plotly figure object
    """
    # Define the target date for 'New' data (May 14, 2022)
    target_date = pd.to_datetime('2022-05-14')
    
    # Select appropriate column based on parameters
    if data_type == 'Cumulative' and metric_type == 'Cases':
        column = 'cumulative_total_cases'
        title = 'Cumulative Cases'
    elif data_type == 'Cumulative' and metric_type == 'Deaths':
        column = 'cumulative_total_deaths'
        title = 'Cumulative Deaths'
    elif data_type == 'New' and metric_type == 'Cases':
        column = 'daily_new_cases'
        title = 'New Cases'
    else:  # New Deaths
        column = 'daily_new_deaths'
        title = 'New Deaths'
    
    # Filter data based on data_type
    if data_type == 'New':
        map_data = df[df['date'] == target_date].copy()
    else:
        map_data = df.sort_values('date').groupby('country').last().reset_index()
    
    # Add coordinates to data
    map_data['lat'] = map_data['country'].map(lambda x: country_coords.get(x, {}).get('lat', None))
    map_data['lon'] = map_data['country'].map(lambda x: country_coords.get(x, {}).get('lon', None))
    
    # Remove countries without coordinates
    map_data = map_data.dropna(subset=['lat', 'lon'])
    
    # Normalize bubble sizes (between 10 and 50)
    max_val = map_data[column].max()
    min_val = map_data[column].min()
    if max_val > min_val:
        map_data['bubble_size'] = 10 + (map_data[column] - min_val) / (max_val - min_val) * 40
    else:
        map_data['bubble_size'] = 25
    
    # Create Scattermapbox trace
    fig = go.Figure()
    
    fig.add_trace(go.Scattermapbox(
        lon=map_data['lon'],
        lat=map_data['lat'],
        text=map_data['country'],
        customdata=map_data[[column, 'country']],
        mode='markers',
        marker=dict(
            size=map_data['bubble_size'],
            color='#00b4d8',
            opacity=0.7,
            sizemode='diameter'
        ),
        hovertemplate=(
            '<b>%{customdata[1]}</b><br>'
            f'{title}: ' + '%{customdata[0]:,.0f}'
            '<extra></extra>'
        ),
        name=''
    ))
    
    fig.update_layout(
        title=dict(
            text=f'COVID-19: {title}',
            font=dict(size=14, family='Arial', color='black'),
            x=0.5,
            xanchor='center'
        ),
        mapbox=dict(
            style='open-street-map',  # Используем OpenStreetMap (не требует токена)
            center=dict(lat=20, lon=0),  # Центр мира
            zoom=1.0
        ),
        height=600,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        # Enable zoom and pan controls
        dragmode='zoom',
        modebar=dict(
            orientation='v',
            bgcolor='rgba(255, 255, 255, 0.7)'
        )
    )
    
    # Enable zoom and pan interactions
    fig.update_mapboxes(
        style='open-street-map',
        # Enable standard mapbox controls
    )
    
    return fig

# Shiny UI
app_ui = ui.page_fluid(
    # Custom CSS for header
    ui.tags.style("""
        .header-container {
            background-color: #003d82;
            padding: 30px 20px;
            margin: -15px -15px 20px -15px;
            color: white;
            text-align: center;
        }
        .header-title {
            font-size: 32px;
            font-weight: bold;
            margin: 0;
            padding: 0;
        }
        .header-subtitle {
            font-size: 14px;
            margin-top: 8px;
            color: #b3d4fc;
        }
        body {
            background-color: #f5f5f5;
        }
    """),
    
    # Header
    ui.div(
        {"class": "header-container"},
        ui.h1("Global COVID-19 Tracker", {"class": "header-title"}),
        ui.p("Data Period: February 15, 2020 - May 14, 2022", {"class": "header-subtitle"})
    ),
    
    ui.row(
        ui.column(3),  # Empty column for centering
        ui.column(3,
            ui.input_select(
                "data_type",
                "New or Cumulative:",
                choices=["New", "Cumulative"],
                selected="New"
            ),
        ),
        ui.column(3,
            ui.input_select(
                "metric_type",
                "Positive Cases or Deaths:",
                choices=["Cases", "Deaths"],
                selected="Cases"
            ),
        ),
        ui.column(3)  # Empty column for centering
    ),
    ui.row(
        ui.column(4,
            ui.h4("Country Statistics"),
            ui.output_ui("covid_charts")
        ),
        ui.column(4,
            ui.h4("World Map"),
            ui.output_ui("world_map")
        ),
        ui.column(4,
            ui.h4("Country Ranking"),
            ui.output_ui("country_ranking")
        )
    ),
    ui.tags.script("""
        $(document).ready(function() {
            setTimeout(function() {
                // Simulate user interaction: change to Cumulative and back to New
                $('#data_type').val('Cumulative').trigger('change');
                setTimeout(function() {
                    $('#data_type').val('New').trigger('change');
                }, 100);
            }, 500);
        });
    """)
)

def server(input, output, session):
    # Reactive value to store selected country (default: World for global statistics)
    selected_country = reactive.Value("World")
    
    @output
    @render.ui
    def covid_charts():
        try:
            country = selected_country.get()
            data_type = input.data_type()
            fig = create_covid_charts(country, data_type)
            return ui.HTML(fig.to_html(include_plotlyjs="cdn", div_id="plotly-chart", config={'displayModeBar': False}))
        except Exception as e:
            return ui.p(f"Error: {str(e)}")
    
    @output
    @render.ui
    def world_map():
        try:
            data_type = input.data_type()
            metric_type = input.metric_type()
            fig = create_world_map(data_type, metric_type)
            
            # Add JavaScript to handle click events
            map_html = fig.to_html(include_plotlyjs="cdn", div_id="plotly-map", config={
                'displayModeBar': True,
                'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
                'displaylogo': False,
                'scrollZoom': True
            })
            js_code = """
            <script>
            setTimeout(function() {
                var mapDiv = document.getElementById('plotly-map');
                if (mapDiv && mapDiv.on) {
                    mapDiv.on('plotly_click', function(data) {
                        if (data.points && data.points[0] && data.points[0].customdata) {
                            var country = data.points[0].customdata[1];
                            Shiny.setInputValue('selected_country', country, {priority: 'event'});
                        }
                    });
                    
                    
                    var plotlyMap = document.querySelector('#plotly-map .plotly');
                    if (plotlyMap) {
                        plotlyMap.addEventListener('click', function(event) {
                            
                            var target = event.target;
                            var isMapBackground = target.classList.contains('mapboxgl-canvas') || 
                                                  target.classList.contains('bg') ||
                                                  target.tagName.toLowerCase() === 'canvas';
                            
                            if (isMapBackground) {
                                
                                setTimeout(function() {
                                    Shiny.setInputValue('selected_country', 'World', {priority: 'event'});
                                }, 50);
                            }
                        });
                    }
                }
            }, 1000);
            </script>
            """
            return ui.HTML(map_html + js_code)
        except Exception as e:
            return ui.p(f"Error: {str(e)}")
    
    @output
    @render.ui
    def country_ranking():
        try:
            data_type = input.data_type()
            metric_type = input.metric_type()
            fig = create_country_ranking(data_type, metric_type)
            
            # Add JavaScript to handle click events and hover effects
            ranking_html = fig.to_html(include_plotlyjs="cdn", div_id="plotly-ranking", config={'displayModeBar': False})
            js_code = """
            <script>
            setTimeout(function() {
                var rankingDiv = document.getElementById('plotly-ranking');
                if (rankingDiv && rankingDiv.on) {
                    // Handle click events
                    rankingDiv.on('plotly_click', function(data) {
                        if (data.points && data.points[0] && data.points[0].customdata) {
                            var country = data.points[0].customdata;
                            Shiny.setInputValue('selected_country', country, {priority: 'event'});
                        }
                    });
                    
                    // Handle hover events to add border effect
                    rankingDiv.on('plotly_hover', function(data) {
                        var update = {
                            'marker.line.color': [],
                            'marker.line.width': []
                        };
                        
                        for (var i = 0; i < data.points[0].data.y.length; i++) {
                            if (i === data.points[0].pointIndex) {
                                update['marker.line.color'].push('rgba(0, 119, 182, 1)');
                                update['marker.line.width'].push(3);
                            } else {
                                update['marker.line.color'].push('rgba(0, 119, 182, 0)');
                                update['marker.line.width'].push(3);
                            }
                        }
                        
                        Plotly.restyle('plotly-ranking', update, [0]);
                    });
                    
                    // Reset on unhover
                    rankingDiv.on('plotly_unhover', function() {
                        var update = {
                            'marker.line.color': 'rgba(0, 119, 182, 0)',
                            'marker.line.width': 3
                        };
                        Plotly.restyle('plotly-ranking', update, [0]);
                    });
                    
                    // Change cursor on hover
                    rankingDiv.addEventListener('mouseover', function() {
                        rankingDiv.style.cursor = 'pointer';
                    });
                }
            }, 1000);
            </script>
            """
            return ui.HTML(ranking_html + js_code)
        except Exception as e:
            return ui.p(f"Error: {str(e)}")
    
    # Update selected country when map is clicked
    @reactive.effect
    @reactive.event(input.selected_country)
    def update_country():
        if input.selected_country():
            selected_country.set(input.selected_country())

app = App(app_ui, server)
