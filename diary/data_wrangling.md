## Data Wrangling Process and Challenges

The main goal of this phase was to prepare a clean and structured dataset ready for
modeling. We started from the relational tables built in Milestone 1 and worked through
validation, feature engineering, and merging everything into a single master table.

For feature engineering, we kept the framing ratios and outlet concentration ideas from
our earlier planning and expanded on them. We added time-based features by calculating
how many months had passed since each crisis started, and flagged the first three months
as the onset period since EDA showed that coverage spikes sharply at the beginning of
a crisis and drops off quickly after.

We also computed a post-onset ratio for each crisis, which captures how much of the
initial coverage spike is retained over time. Some crises like Syria maintain relatively
steady attention while others collapse to near zero after the first few months, and this
feature helps the model pick up on that difference.

One recurring challenge was the partial availability of framing, sentiment, and victim
data. These are only present for Gaza and Ukraine, so we had to fill zeros for the
remaining crises and be clear about that limitation. We kept three framing ratio columns
in the final dataset since they still add signal for the two crises that have them,
but we noted that their predictive value is limited across the full dataset.

The master table came out at the monthly level, giving us a dataset with enough rows
for proper train/test evaluation in the modeling stage.