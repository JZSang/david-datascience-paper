# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
"Test portion"
from SIRModel import *
import matplotlib.pyplot as plt
import pandas as pd

# sir = SIRModel(10000, 140)
# sir.set_contact_rate(0.2)
# sir.integrate()

# S, I, R, t = sir.S, sir.I, sir.R, sir.t
# # Plot the data on three separate curves for S(t), I(t) and R(t)
# fig = plt.figure(facecolor='w')
# ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
# ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
# ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
# ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
# ax.plot(t, (I+R)/1000, 'm', alpha=0.5, lw=2, label="Confirmed cases")
# ax.set_xlabel('Time /days')
# ax.set_ylabel('Number (1000s)')
# ax.set_ylim(0, 10.2)
# ax.yaxis.set_tick_params(length=0)
# ax.xaxis.set_tick_params(length=0)
# ax.grid(b=True, which='major', c='w', lw=2, ls='-')
# legend = ax.legend()
# legend.get_frame().set_alpha(0.5)
# for spine in ('top', 'right', 'bottom', 'left'):
#     ax.spines[spine].set_visible(False)
# plt.show()


# %%
print("Processing data...")
us_records = pd.read_csv("./data/US_counties_COVID19_health_weather_data.csv")
population = pd.read_csv("./data/co-est2019-alldata.csv",
                         encoding="latin").set_index("CTYNAME")


# %%
print("Processing counties into dictionary...")
counties = us_records.county.unique()
county_specific = {elem: pd.DataFrame for elem in counties}
for county in county_specific.keys():
    county_specific[county] = us_records[:][us_records.county ==
                                            county].reset_index()


# %%
r2_score_by_name = []
for county_name in county_specific:
    try:

        print("Processing " + county_name + "...")
        #     county =
        # county_name = "San Francisco"
        print((county_name + " County") in population.COUNTY)
        if county_name + " County" not in population.COUNTY:
            continue
        if isinstance(population.loc[county_name + " County"], pd.DataFrame):
            continue
        county = county_specific[county_name]
        county_population = population.loc[county_name +
                                           " County"].POPESTIMATE2019
        indexes_before_stay_at_home = len(
            county[county.stay_at_home_effective == 'no'].index)
        buffer = indexes_before_stay_at_home - \
            20 if indexes_before_stay_at_home >= 20 else 0
        county_pre = county[buffer:indexes_before_stay_at_home]
        sir = SIRModel(county_population, len(county_pre.index))
        sir.set_contact_rate(0.216)
        sir.set_mean_recovery_rate(1./10)

        def find_best_interval(min, interval, number, parameter_function):
            parameters = []
            minimum_cost = -1
            min_index = None
            for i in range(0, number):
                parameter_function(min + i * interval)
                sir.integrate()
                S, I, R, t = sir.S, sir.I, sir.R, sir.t
                parameters.append(min + i * interval)

                cost = sum(((I+R) ** 2) - (county_pre.cases ** 2))
                if minimum_cost == -1 or abs(cost) < minimum_cost:
                    minimum_cost = abs(cost)
                    min_index = i
            return parameters[min_index]

        contact_rate = find_best_interval(
            0.04, 0.005, 100, sir.set_contact_rate)
        contact_rate_accurate = find_best_interval(
            contact_rate - 0.003, 0.001, 5, sir.set_contact_rate)
        mean_recovery_rate = find_best_interval(
            1./100, 0.01, 50, sir.set_mean_recovery_rate)

        model_sir = SIRModel(county_population, len(county.index))
        model_sir.set_contact_rate(contact_rate_accurate)
        model_sir.set_mean_recovery_rate(mean_recovery_rate)
        model_sir.integrate()

        stay_at_home_sir = SIRModel(county_population, len(county.index) - indexes_before_stay_at_home, R0=(
            model_sir.R[indexes_before_stay_at_home-buffer]), I0=model_sir.I[indexes_before_stay_at_home-buffer], contact_rate=0.18)
        stay_at_home_sir.integrate()

        S, I, R, t = model_sir.S, model_sir.I, model_sir.R, model_sir.t
        # Plot the data on three separate curves for S(t), I(t) and R(t)
        # fig = plt.figure(facecolor='w')
        # ax = fig.add_subplot(111, facecolor='#dddddd',
        #                      axisbelow=True, title=county_name)
        # # ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
        # # ax.plot(t +buffer, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
        # # ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        # ax.plot(t+buffer, (I+R)/1000, 'k', alpha=0.5, lw=2, label="Expected cases")
        # ax.plot(t, (county.cases/1000), 'm', alpha=0.5, lw=2, label="Actual cases")
        # # ax.plot(np.linspace(0, len(county.index) - indexes_before_stay_at_home-1, len(county.index) - indexes_before_stay_at_home) + indexes_before_stay_at_home, (stay_at_home_sir.I + stay_at_home_sir.R)/1000,  'b', alpha=0.5, lw=2, label="Expected cases stay at home")
        # stay_at_home_order_index = len(
        #     county[county.stay_at_home_effective == "no"].index)
        # ax.axvline(stay_at_home_order_index, label="Stay At Home Order Effective")
        # ax.axvline(stay_at_home_order_index + 14,
        #            label="Stay At Home Order Effective + 14 days", color="g")
        # ax.set_xlabel('Time /days')
        # ax.set_ylabel('Number (1000s)')
        # ax.set_ylim(0, max(county.cases)/1000)

        # ax.yaxis.set_tick_params(length=0)
        # ax.xaxis.set_tick_params(length=0)
        # ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        # legend = ax.legend()
        # legend.get_frame().set_alpha(0.5)
        # for spine in ('top', 'right', 'bottom', 'left'):
        #     ax.spines[spine].set_visible(False)
        # print(buffer)
        # plt.show()
        print("Processing r2 score for " + county_name)
        from sklearn.metrics import r2_score
        sir.set_contact_rate(contact_rate_accurate)
        sir.set_mean_recovery_rate(mean_recovery_rate)
        sir.integrate()
        if len(county_pre.cases) <= 0 or len(sir.I) <= 0:
            continue
        beforer2 = r2_score((county_pre.cases/1000), (sir.I+sir.R)/1000)
        if len(county.cases[buffer:]) != len((I+R)[:-buffer]):
            continue
        afterr2 = r2_score(county.cases[buffer:]/1000, (I+R)[:-buffer]/1000)

        r2_score_by_name.append([county_name, beforer2, afterr2])
    except:
        continue


# %%
r2_score_by_name_df = pd.DataFrame(r2_score_by_name, columns=[
                                   "COUNTY", "R2SCOREBEFORE", "R2SCOREAFTER"])
r2_score_by_name_df.to_csv("./r2_score.csv")
