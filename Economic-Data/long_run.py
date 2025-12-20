import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from collections import namedtuple

data_url = "mpd2020.xlsx"
data = pd.read_excel(data_url,
                     sheet_name="Full data")
# print(data.head())
countries = data.country.unique()  # Access how many countries in the df
country_years = []
print(data.tail())
for country in countries:
    cy_data = data[data.country == country]['year']
    ymin, ymax = cy_data.min(), cy_data.max()
    country_years.append((country, ymin, ymax))
country_years = pd.DataFrame(country_years,
                             columns = ["country", 'min_year', "max_year"]).set_index('country')

# print(country_years.head())
code_to_name = data[
    ['countrycode', 'country']].drop_duplicates().reset_index(drop=True).set_index(['countrycode'])
# AFG - Afganistan, USA - United States
gdp_pc = data.set_index(["countrycode", "year"])["gdppc"]
gdp_pc = gdp_pc.unstack("countrycode")
print(gdp_pc.tail())
country_names = gdp_pc.columns
# Generate a colormap with the number of colors matching the number of countries
colors = cm.tab20(np.linspace(0, 0.95, len(country_names)))
# Generating a dictionary to map each country to its corresponding color
color_mapping = dict(zip(country_names, colors))

# Create Color-mapping
### GDP per Capita
## United Kingdom
fig, ax = plt.subplots(dpi=100)
country = "GBR"
# gdp_pc[country].plot(
#     ax=ax,
#     ylabel='international dollars',
#     xlabel='year',
#     color="red"
# )
ax.plot(gdp_pc[country].interpolate(), # interpolate means "--"
        linestyle="--",
        lw=2,
        color=color_mapping[country])
ax.plot(gdp_pc[country],
        lw=2,
        color=color_mapping[country])
ax.set_ylabel('international dollars')
ax.set_xlabel('year')
# International dollars are a hypothetical unit of currency that has the same purchasing
# power parity that the U.S. Dollar has in the United States at a given point in time.

### Comparing the US, UK, and China
def draw_interp_plots(series,
                      country,
                      ylabel,
                      xlabel,
                      color_mapping,
                      code_to_name,
                      lw,
                      logscale,
                      ax):
    for c in country:
        # Get the interpolated data
        df_interpolated = series[c].interpolate(limit_area='inside')
        interpolated_data = df_interpolated[series[c].isnull()]

        # Plot the interpolated data with dashed lines
        ax.plot(interpolated_data,
                linestyle='--',
                lw=lw,
                alpha=0.7,
                color=color_mapping[c])
        
        # Plot the non-interpolated data with solid lines
        ax.plot(series[c],
                lw=lw,
                color=color_mapping[c],
                alpha=0.8,
                label=code_to_name.loc[c]['country'])
        if logscale:
            ax.set_yscale('log')
        ax.legend(loc='upper left', frameon=False)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
# Define the namedtuple for the events.


Event = namedtuple('Event', ['year_range', 'y_text', 'text', 'color', 'ymax'])
fig2, ax2 = plt.subplots(dpi=100, figsize=(10, 6))
multicountries = ['CHN', "GBR", "USA"]
draw_interp_plots(gdp_pc.loc[1500:],
                  multicountries,
                  'international dollars',
                  'year',
                  color_mapping,
                  code_to_name,
                  2,
                  False,
                  ax2)
# Define the parameters for the events and the text
ylim = ax.get_ylim()[1]
b_params = {'color':'grey', 'alpha':0.2}
t_params = {'fontsize':9,
            'va':'center',
            'ha':'center'}
# Create a list of events to annotate
events = [
    Event((1650, 1652), ylim + ylim*0.04,
          'the Navigation Act\n(1651)',
          color_mapping['GBR'], 1),
          Event((1655, 1684), ylim + ylim*0.13, 
          'Closed-door Policy\n(1655-1684)', 
          color_mapping['CHN'], 1.1),
    Event((1848, 1850), ylim + ylim*0.22,
          'the Repeal of Navigation Act\n(1849)', 
          color_mapping['GBR'], 1.18),
    Event((1765, 1791), ylim + ylim*0.04, 
          'American Revolution\n(1765-1791)', 
          color_mapping['USA'], 1),
    Event((1760, 1840), ylim + ylim*0.13, 
          'Industrial Revolution\n(1760-1840)', 
          'grey', 1.1),
    Event((1929, 1939), ylim + ylim*0.04, 
          'the Great Depression\n(1929–1939)', 
          'grey', 1),
    Event((1978, 1979), ylim + ylim*0.13, 
          'Reform and Opening-up\n(1978-1979)', 
          color_mapping['CHN'], 1.1)
]
def draw_events(events, ax):
    # Iterate over events and add annotations and vertical lines
    for event in events:
        event_mid = sum(event.year_range)/2
        ax.text(event_mid,
                event.y_text, event.text,
                color=event.color, **t_params)
        ax.axvspan(*event.year_range, color=event.color, alpha=0.2)
        ax.axvline(event_mid, ymin=0, ymax=1, color=event.color,
                   alpha=0.15)
draw_events(events, ax2)

# China
fig3, ax3 = plt.subplots(dpi=100, figsize=(10, 6))
country = ['CHN']
draw_interp_plots(gdp_pc[country].loc[1500:2000],
                  country,
                  'international dollars', 'year',
                  color_mapping, code_to_name, 2, True, ax3)
ylim = ax3.get_ylim()[1]
events2 = [
    Event((1655, 1684), ylim*0.6,
          'Closed-door Policy\n(1655-1684)',
          'tab:orange', 1),
    Event((1760, 1840), ylim*0.4, 
        'Industrial Revolution\n(1760-1840)', 
        'grey', 1),
    Event((1839, 1842), ylim*0.5, 
        'First Opium War\n(1839–1842)', 
        'tab:red', 1.07),
    Event((1861, 1895), ylim*0.9, 
        'Self-Strengthening Movement\n(1861–1895)', 
        'tab:blue', 1.14),
    Event((1939, 1945), ylim*0.6, 
        'WW 2\n(1939-1945)', 
        'tab:red', 1),
    Event((1948, 1950), ylim*0.5, 
        'Founding of PRC\n(1949)', 
        color_mapping['CHN'], 1.08),
    Event((1958, 1962), ylim*0.4, 
        'Great Leap Forward\n(1958-1962)', 
        'tab:orange', 1.18),
    Event((1978, 1979), ylim*0.7, 
        'Reform and Opening-up\n(1978-1979)', 
        'tab:blue', 1.24)
]
draw_events(events2, ax3)

# US and UK
fig4, ax4 = plt.subplots(dpi=100, figsize=(10, 6))
country = ['GBR', "USA"]
ylim = ax4.get_ylim()[1]
draw_interp_plots(gdp_pc[country].loc[1500:2000],
                  country,
                  'international dollars', 'year',
                  color_mapping, code_to_name, 2, False, ax4)
events3 = [
    Event((1651, 1651), ylim* 0.5,
          'Navigation Ack(UK)\n(1651)',
          'tab:yellow', 1.1),
    Event((1760, 1840), ylim*0.6,
          'Industrial Revolution\n(1760-1840)',
          'tab:grey', 1.1),
    Event((1765, 1791), ylim*0.7,
          'American Revolution\n(1765-1791)',
          color_mapping['USA'], 1.2),
    Event((1849, 1849), ylim*0.8,
          'Repeal of Nagigation Act(UK)\n(1849)',
          color_mapping['GBR'], 1.2),
    Event((1861, 1865), ylim*0.7,
          'American Civil War\n(1861-1865)',
          color_mapping['USA'], 1.2),
    Event((1914, 1918), ylim*0.4,
          'WW1\n(1914-1918)',
          'tap:red', 1.2),
    Event((1939, 1945), ylim*0.6,
          'WW2'),
    Event()
]

plt.show()
