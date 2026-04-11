## Data Visualization and Dashboard

For the visualization stage we built a static dashboard in a Jupyter notebook using
ipywidgets. The goal was to present the key findings from all three stages of the
pipeline in a way that is interactive and easy to follow.

The dashboard is organized into eight sections. The first few cover the coverage
landscape and how it varies across crises, including comparisons normalized by
funding and people affected. We then look at how coverage relates to severity
metrics, monthly trends over time, and how different outlets behave across crises.

The framing and sentiment sections focus on the narrative angle. Since framing and
sentiment data is only available for Gaza and Ukraine, we added a note to make that
limitation clear rather than letting it look like incomplete work.

The final sections present the modeling results, including model comparison, feature
importance from both the linear and tree models, actual vs predicted plots, and
residual analysis. The dashboard closes with a composite summary panel that brings
the key findings together in a single view.

Building the dashboard required going back and adjusting some of the earlier modeling
outputs to make sure the visualizations connected cleanly with the wrangling and
modeling notebooks. Overall this stage helped clarify which findings were the most
communicable and where the story of the data was strongest.