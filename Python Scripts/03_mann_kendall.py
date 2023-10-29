    from mk_test import mk_test



    def mk_test_p_values(self):
        self.mk_dict = dict.fromkeys(self.projections)
        for projection in self.projections:
           self. mk_dict[projection] = dict.fromkeys(self.policies)
            for policy in self.policies:
                trend, _, p, _ = mk_test(np.array(self.all_flows[projection][policy]))
                self.mk_dict[projection][policy] = [trend, p]

    def mk_stats(self):
        self.trend_dict = {}

        for k in pct_dict:
            pct_dict[k] = {
                "No Trend": [],
                "Increasing": [],
                "Decreasing": [],
                "Percents": []
            }

        for projection in PROJECTIONS:
            for policy in self.polcicies:
                if self.mk_dict[projection][policy] == 'no trend':
                    self.pct_dict[policy]['No Trend'].append(projection)




def mk_test_p_values(self):
        self.mk_dict = dict.fromkeys(self.projections)
        for projection in self.projections:
           self. mk_dict[projection] = dict.fromkeys(self.policies)
            for policy in self.policies:
                trend, _, p, _ = mk_test(np.array(self.all_flows[projection][policy]))
                self.mk_dict[projection][policy] = [trend, p]

    def mk_stats(self):
        self.trend_results = dict.fromkeys(self.policies)

        for policy in self.policies:
            self.trend_results[k] = {
                "No Trend": [],
                "Increasing": [],
                "Decreasing": [],
                "Percents": []
            }

        for projection in PROJECTIONS:
            for policy in self.polcicies:
                if self.mk_dict[projection][policy] == 'no trend':
                    self.trend_results[policy]['No Trend'].append(projection)
                elif self.mk_dict[projection][policy] == 'increasing':
                    self.trend_results[policy]['Increasing'].append(projection)
                else:
                    self.trend_results[policy]['Decreasing'].append(projection)

        for policy in self.trend_results:
            no_trend = len(self.trend_results[policy]['No Trend']) / len(PROJECTIONS)
            increasing = len(self.trend_results[policy]['Increasing']) / len(PROJECTIONS)
            decreasing = len(self.trend_results[policy]['Decreasing']) / len(PROJECTIONS)
            self.trend_results[policy] = [no_trend, increasing, decreasing]


    
    def mann_kendall_test(self):
        self.sevenQ.mk_test_p_values()
        self.sevenQ.mk_stats()
        self.ams.mk_test_p_values()
        self.ams.mk_stats()
        self.compromise.mk_test_p_values()
        self.compromise.mk_stats()
dps.mann_kendall_test()
uc.mann_kendall_test()


### 6. Mann Kendall Plotter

ams_no_trend = []
ams_increasing = []
ams_decreasing = []

low_no_trend = []
low_increasing = []
low_decreasing = []


def add_policies(low_flows, high_flows, policy):
    low_no_trend.append(low_flows[policy]['Percents'][0])
    ams_no_trend.append(high_flows[policy]['Percents'][0])
    
    low_increasing.append(low_flows[policy]['Percents'][1])
    ams_increasing.append(high_flows[policy]['Percents'][1])
    
    low_decreasing.append(low_flows[policy]['Percents'][2])
    ams_decreasing.append(high_flows[policy]['Percents'][2])


policy = 'PUC'
add_policies(uc.sevenQ.trend_results, uc.ams.trend_results, policy)

for policy in [dps.sevenQ.robust_policy, dps.ams.robust_policy, dps.comproise.robust_policy]:
    add_policies(dps.sevenQ.trend_results, dps.ams.trend_results, policy)


def prep_mk_plot(no_trend, increasing, decreasing):
    df = pd.DataFrame({
        "No Trend":no_trend,
        "Increasing":increasing, 
        "Decreasing":decreasing
        }, index=['PUC', 'Low Flow\nPolicy', 'High Flow\nPolicy', 'Compromise\nPolicy']
    )
    df = df.reindex(index=df.index[::-1])
    return df

plotdata = prep_mk_plot(ams_no_trend, ams_increasing, ams_decreasing)
plotdata_7q = prep_mk_plot(low_no_trend, low_increasing, low_decreasing)




def mk_plotter():




fig, (ax1, ax2) = plt.subplots(1,2)
sns.set(style="dark")
plotdata_7q.plot(kind="barh", stacked=True, color=['darkgrey', 'cornflowerblue', 'orange'], ax = ax1, legend = False)
plotdata.plot(kind="barh", stacked=True, color=['darkgrey', 'cornflowerblue', 'orange'], ax = ax2, legend=False)
for (ax,i) in zip([ax1, ax2], range(2)):
    ax.set_xticklabels([0, 25, 50, 75, 100])
    ax.set_xlabel("Projections (%)")
    ax.text(0.008, 1.01, "("+ string.ascii_lowercase[i] + ")", transform=ax.transAxes, 
        size=13, weight='bold')
ax1.set_title("7QS Trend")
ax2.set_title("AMS Trend")
fig.set_size_inches([7.35, 3.5])
fig.tight_layout()

# ax2.legend(bbox_to_anchor=(1.02, 1.0))
fig.tight_layout()
plt.savefig('../Figures/Trends.svg')