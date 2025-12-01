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

# Get country coordinates for map (simplified mapping - you may need a better source)
country_coords = {
    'United States': {'lat': 37.0902, 'lon': -95.7129},
    'Brazil': {'lat': -14.2350, 'lon': -51.9253},
    'India': {'lat': 20.5937, 'lon': 78.9629},
    'Russia': {'lat': 61.5240, 'lon': 105.3188},
    'United Kingdom': {'lat': 55.3781, 'lon': -3.4360},
    'France': {'lat': 46.2276, 'lon': 2.2137},
    'Turkey': {'lat': 38.9637, 'lon': 35.2433},
    'Germany': {'lat': 51.1657, 'lon': 10.4515},
    'Italy': {'lat': 41.8719, 'lon': 12.5674},
    'Spain': {'lat': 40.4637, 'lon': -3.7492},
    'Argentina': {'lat': -38.4161, 'lon': -63.6167},
    'Colombia': {'lat': 4.5709, 'lon': -74.2973},
    'Poland': {'lat': 51.9194, 'lon': 19.1451},
    'Iran': {'lat': 32.4279, 'lon': 53.6880},
    'Mexico': {'lat': 23.6345, 'lon': -102.5528},
    'Ukraine': {'lat': 48.3794, 'lon': 31.1656},
    'Peru': {'lat': -9.1900, 'lon': -75.0152},
    'Indonesia': {'lat': -0.7893, 'lon': 113.9213},
    'South Africa': {'lat': -30.5595, 'lon': 22.9375},
    'Netherlands': {'lat': 52.1326, 'lon': 5.2913},
    'Czechia': {'lat': 49.8175, 'lon': 15.4730},
    'Chile': {'lat': -35.6751, 'lon': -71.5430},
    'Iraq': {'lat': 33.2232, 'lon': 43.6793},
    'Belgium': {'lat': 50.5039, 'lon': 4.4699},
    'Romania': {'lat': 45.9432, 'lon': 24.9668},
    'Canada': {'lat': 56.1304, 'lon': -106.3468},
    'Philippines': {'lat': 12.8797, 'lon': 121.7740},
    'Vietnam': {'lat': 14.0583, 'lon': 108.2772},
    'Malaysia': {'lat': 4.2105, 'lon': 101.9758},
    'Portugal': {'lat': 39.3999, 'lon': -8.2245},
    'Japan': {'lat': 36.2048, 'lon': 138.2529},
    'Israel': {'lat': 31.0461, 'lon': 34.8516},
    'Switzerland': {'lat': 46.8182, 'lon': 8.2275},
    'Austria': {'lat': 47.5162, 'lon': 14.5501},
    'Greece': {'lat': 39.0742, 'lon': 21.8243},
    'Hungary': {'lat': 47.1625, 'lon': 19.5033},
    'Serbia': {'lat': 44.0165, 'lon': 21.0059},
    'Jordan': {'lat': 30.5852, 'lon': 36.2384},
    'Thailand': {'lat': 15.8700, 'lon': 100.9925},
    'South Korea': {'lat': 35.9078, 'lon': 127.7669},
    'Cuba': {'lat': 21.5218, 'lon': -77.7812},
    'Denmark': {'lat': 56.2639, 'lon': 9.5018},
    'Bulgaria': {'lat': 42.7339, 'lon': 25.4858},
    'Slovakia': {'lat': 48.6690, 'lon': 19.6990},
    'Croatia': {'lat': 45.1, 'lon': 15.2},
    'Tunisia': {'lat': 33.8869, 'lon': 9.5375},
    'China': {'lat': 35.8617, 'lon': 104.1954},
    'Australia': {'lat': -25.2744, 'lon': 133.7751},
}

# Function to format Y-axis values (1000 -> 1K, 200000 -> 200K)
def format_y_axis(value, pos):
    if value >= 1000:
        return f'{int(value/1000)}K'
    return f'{int(value)}'

# Function to create COVID-19 charts for a specific country using Plotly
def create_covid_charts(country_name, data_type='New'):
    """
    Creates two interactive time series charts for a given country using Plotly:
    1. New/Cumulative Positive Cases over time
    2. New/Cumulative Deaths over time
    
    Parameters:
    country_name (str): Name of the country to analyze
    data_type (str): 'New' or 'Cumulative' - type of data to display
    
    Returns:
    plotly figure object
    """
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
        marker=dict(color='#00b4d8'),
        text=top_countries[column].apply(lambda x: f'{int(x):,}'),
        textposition='outside',
        textfont=dict(size=10),
        hovertemplate='<b>%{y}</b><br>%{x:,.0f}<extra></extra>'
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
        margin=dict(l=120, r=80, t=50, b=30),
        showlegend=False
    )
    
    return fig

# Function to create interactive world map with COVID-19 data
def create_world_map(data_type, metric_type):
    """
    Creates an interactive world map showing COVID-19 data by country
    
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
    
    # Create the scatter geo map
    fig = go.Figure()
    
    fig.add_trace(go.Scattergeo(
        lon=map_data['lon'],
        lat=map_data['lat'],
        text=map_data['country'],
        customdata=map_data[[column, 'country']],
        mode='markers',
        marker=dict(
            size=map_data[column] / map_data[column].max() * 50 + 5,  # Scale bubble size
            color='#00b4d8',
            line=dict(width=0.5, color='white'),
            sizemode='diameter',
            opacity=0.7
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
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            showcountries=True,
            countrycolor='rgb(204, 204, 204)',
            showlakes=False,
            showocean=True,
            oceancolor='rgb(230, 245, 255)',
        ),
        height=600,
        margin=dict(l=0, r=0, t=50, b=0),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

# Shiny UI
app_ui = ui.page_fluid(
    ui.h2("COVID-19 Dashboard"),
    ui.row(
        ui.column(6,
            ui.input_select(
                "data_type",
                "Data Type:",
                choices=["New", "Cumulative"],
                selected="New"
            ),
        ),
        ui.column(6,
            ui.input_select(
                "metric_type",
                "Metric:",
                choices=["Cases", "Deaths"],
                selected="Cases"
            ),
        )
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
    )
)

def server(input, output, session):
    # Reactive value to store selected country
    selected_country = reactive.Value("Russia")
    
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
            map_html = fig.to_html(include_plotlyjs="cdn", div_id="plotly-map", config={'displayModeBar': False})
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
            return ui.HTML(fig.to_html(include_plotlyjs="cdn", div_id="plotly-ranking", config={'displayModeBar': False}))
        except Exception as e:
            return ui.p(f"Error: {str(e)}")
    
    # Update selected country when map is clicked
    @reactive.effect
    @reactive.event(input.selected_country)
    def update_country():
        if input.selected_country():
            selected_country.set(input.selected_country())

app = App(app_ui, server)
