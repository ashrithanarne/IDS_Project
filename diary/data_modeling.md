## Data Modeling

For modeling we used the monthly-level master dataset produced in the wrangling stage.
The target variable is log-transformed monthly coverage, which we chose to reduce the
heavy skew caused by Gaza and Ukraine months with extremely high article counts.

We compared four models: Linear Regression, Ridge Regression, Decision Tree, and
Random Forest. Linear and Ridge are both linear models -- Ridge adds a small penalty
to prevent coefficients from getting unreasonably large, which is useful when some
features are correlated with each other as ours are. Decision Tree builds a set of
if-else rules to split the data, and Random Forest averages predictions across many
trees to get a more stable result.

We used an 80/20 temporal train/test split, meaning the model was trained on older
months and tested on more recent ones. This is more realistic than random splitting
for time-based data since we are effectively asking the model to predict coverage
it has not seen yet.

Decision Tree achieved the highest test R2 at 0.674, followed closely by Linear
and Ridge Regression around 0.653-0.656. Random Forest underperformed at 0.472,
which was unexpected but makes sense given that the relationships in this dataset
are largely linear and the framing features are sparse.

Looking at feature importance, fund_required and crisis_days were consistently the
most influential features across both the linear coefficients and the Random Forest
importance rankings. The onset flag and months since start also contributed, while
people_affected showed a negative coefficient despite the intuition that larger
crises should attract more coverage.

The residual analysis showed errors roughly centered around zero with a near-normal
distribution, suggesting the models are not systematically biased in one direction.