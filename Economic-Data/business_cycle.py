import matplotlib.pyplot as plt
import pandas as pd
import datetime
import wbgapi as wb
import pandas_datareader.data as web

cycler = plt.cycler(linestyle=['-','-','-','-'],
                    color=['#377eb8', '#ff7f00', '#4daf4a', '#ff334f'])
plt.rc('axes', prop_cycle=cycler)

# We use World Bank API to retrive data
wb.series.info(q='GDP growth')
gdp_growth = wb.data.DataFrame('NY.GDP.MKTP.KD.ZG',
                               ['USA', 'ARG', 'GBR', 'GRC', 'JPN'],
                               labels=True)
gdp_growth = gdp_growth.set_index('Country')
gdp_growth.columns = gdp_growth.columns.str.replace('YR', '').astype(int)
print(gdp_growth)

def plot_series(data, country, ylabel,
                txt_pos, ax, g_params,
                b_params, t_params, ylim=15, baseline=0):
    ax.plot(data.loc[country], label=country, **g_params)
    # Highlight recessions
    ax.axvspan(1973, 1975, **b_params)
    ax.axvspan(1990, 1992, **b_params)
    ax.axvspan(2007, 2009, **b_params)
    ax.axvspan(2019, 2021, **b_params)
    if ylim != None:
        ax.set_ylim([-ylim, ylim])
    else:
        ylim = ax.get_ylim()[1]
    ax.text(1974, ylim+ylim*txt_pos,
            'Oil Crisis\n(1974)', **t_params)
    ax.text(1990, ylim+ylim*txt_pos,
            '1990s recession\n(1991)', **t_params)
    ax.text(2007, ylim+ylim*txt_pos,
            'GFC\n(2008)', **t_params)
    ax.text(2019, ylim+ylim*txt_pos,
            'COVID-19\n(2020)', **t_params)
    
    # Add a baseline for reference
    if baseline != None:
        ax.axhline(y=baseline,
                   color='black',
                   linestyle='--')
    ax.set_ylabel(ylabel)
    ax.legend()
    return ax
# Define graphical parameters
g_params = {'alpha':0.7}
b_params = {'color':'grey', 'alpha':0.2}
t_params = {'color':'grey', 'fontsize':9,
            'va':'center', 'ha':'center'}
# United States
fig, ax = plt.subplots()
country = 'United States'
ylabel = 'GDP growth rate (%)'
plot_series(gdp_growth, country,
            ylabel, 0.1, ax,
            g_params, b_params, t_params)
# United Kingdom
fig2, ax2 = plt.subplots()
country2 = 'United Kingdom'
plot_series(gdp_growth, country2,
            ylabel, 0.1, ax2,
            g_params, b_params, t_params)


# Unemployment Rate
start_date = datetime.datetime(1929, 1, 1)
end_date = datetime.datetime(1942, 6, 1)
unrate_hist = web.DataReader('M0892AUSM156SNBR',
                             'fred', start_date, end_date)
unrate_hist.rename(columns={'M0892AUSM156SNBR': 'UNRATE'},
                   inplace=True)
start_date = datetime.datetime(1948, 1, 1)
end_date = datetime.datetime(2022, 12, 31)
unrate = web.DataReader('UNRATE', 'fred',
                        start_date, end_date)
# Plot the Unemployment rate of the US from 1929 to 2022
years = [datetime.datetime(year, 6, 1) for year in range(1942, 1948)]
unrate_census = [4.7, 1.9, 1.2, 1.9, 3.9, 3.9]
unrate_census = pd.DataFrame({'DATE':years, 'UNRATE':unrate_census})
unrate_census.set_index('DATE', inplace=True)
start_date = datetime.datetime(1929, 1, 1)
end_date = datetime.datetime(2022, 12, 31)

nber = web.DataReader('USREC', 'fred', start_date, end_date)

fig3, ax3 = plt.subplots()
ax3.plot(unrate_hist, **g_params,
         color='#377eb8',
         linestyle='-', linewidth=2)
ax3.plot(unrate_census, **g_params,
         color='black',
         linestyle='--',
         label = 'Census estimates', linewidth=2)
ax3.plot(unrate, **g_params,
         color='#377eb8',
         linestyle='-', linewidth=2)
# Draw Recession blackbox
ax3.fill_between(nber.index, 0, 1,
                 where=nber['USREC']==1,
                 color='grey', edgecolor='none',
                 alpha=0.3,
                 transform=ax3.get_xaxis_transform(),
                 label='NBER recession indicators')
ax3.set_ylim([0, ax3.get_ylim()[1]])
ax.legend(loc='upper center',
          bbox_to_anchor=(0.5, 1.1),
          ncol=3, fancybox=True, shadow=True)
ax3.set_ylabel('unemployment rate(%)')


# Plot comparisons between countries in receisson
def plot_comparison(data, countries,
                    ylabel, txt_pos, y_lim, ax,
                    g_params, b_params, t_params,
                    baseline=0):
    for country in countries:
        ax.plot(data.loc[country], label=country, **g_params)
    ax.axvspan(1973, 1975, **b_params)
    ax.axvspan(1990, 1992, **b_params)
    ax.axvspan(2007, 2009, **b_params)
    ax.axvspan(2019, 2021, **b_params)
    if y_lim != None:
        ax.set_ylim([-y_lim, y_lim])
    ylim = ax.get_ylim()[1]
    ax.text(1974, ylim+ylim*txt_pos,
            'Oil Crisis\n(1974)', **t_params)
    ax.text(1991, ylim+ylim*txt_pos,
            '1990s recession\n(1991)', **t_params)
    ax.text(2008, ylim+ylim*txt_pos,
            'GFC\n(2008)', **t_params)
    ax.text(2019, ylim+ylim*txt_pos,
            'COVID-19\n(2020)', **t_params)
    if baseline != None:
        ax.hlines(y=baseline, xmin=ax.get_xlim()[0],
                  xmax=ax.get_xlim()[1], color='black',
                  linestyle='--')
    ax.set_ylabel(ylabel)
    ax.legend()
    return ax
gdp_growth2 = wb.data.DataFrame('NY.GDP.MKTP.KD.ZG',
                                ['CHN', 'USA', 'DEU', 'BRA', 'ARG', 'GBR', 'JPN', 'MEX'],
                                labels=True)
gdp_growth2 = gdp_growth2.set_index('Country')
gdp_growth2.columns = gdp_growth2.columns.str.replace('YR', '').astype(int)
fig4, ax4 = plt.subplots()
countries = ['United Kingdom', 'United States', 'Germany', 'Japan']
ylabel = 'GDP growth rate(%)'
plot_comparison(gdp_growth2.loc[countries, 1962:],
                countries, ylabel,
                0.1, 20, ax4, g_params, b_params, t_params)

fig5, ax5 = plt.subplots()
countries2 = ['Brazil', 'China', 'Argentina', 'Mexico']
plot_comparison(gdp_growth2.loc[countries2, 1962:],
                countries2, ylabel,
                0.1, 20, ax5,
                g_params, b_params, t_params)
plt.show()