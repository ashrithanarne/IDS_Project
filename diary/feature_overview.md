## Feature Overview and Correlation Analysis

After building the master dataset, we ran a correlation analysis to understand how
each feature relates to the target variable, log-transformed monthly coverage.

The strongest positive correlation came from fund_required, which was somewhat
surprising since we expected time-based features to dominate. It seems crises with
larger internationally recognized funding needs also tend to attract more monthly
reporting. The is_onset flag was also positively correlated, confirming the spike
pattern we saw in EDA.

On the negative side, crisis_days had the strongest negative correlation overall.
Longer-running crises receive less coverage per month, which makes sense because
media attention tends to fade as a crisis becomes old news. months_since_start and
top3_outlet_ratio were also negative, with the outlet concentration finding being
particularly interesting -- crises where a few outlets dominate seem to accumulate
fewer total articles than those covered by a wider range of sources.

The framing ratios showed moderate positive correlations with log coverage, but
because they are only non-zero for two crises, we treat their signal carefully.

Based on this analysis, we finalized the feature set and moved into modeling.