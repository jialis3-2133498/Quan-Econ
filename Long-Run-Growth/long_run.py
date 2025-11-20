import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from collections import namedtuple

data_url = "mpd2020.xlsx"
data = pd.read_excel(data_url,
                     sheet_name="Full data")
# print(data.head())
countries = data.country.unique()
print(len(countries))  # Access how many countries in the df
country_years = []
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
        color="red")
ax.plot(gdp_pc[country],
        lw=2,
        color="red")
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
fig2, ax2 = plt.subplots(dpi=100, figsize=(10, 6))
draw_interp_plots(gdp_pc,
                  ['USA', 'GBR', "CHN"],
                  'international dollars',
                  'year',
                  {
                      'USA':'blue',
                      'GBR':'red',
                      'CHN':'green'
                  },
                  code_to_name,
                  2,
                  False,
                  ax2)
plt.show()
