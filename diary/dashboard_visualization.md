## **Dashboard Visualization**

This week we worked on building the static dashboard for Milestone 2 using ipywidgets
in a Jupyter notebook. The goal was to take all the findings from wrangling and modeling
and communicate them clearly through interactive visualizations.

We structured the dashboard into eight sections, each focused on a different angle of
the analysis: coverage distribution across crises, coverage vs severity metrics, monthly
trends over time, outlet behavior, narrative framing, entity sentiment, model results,
and a composite summary panel.

One decision we made early was to use ToggleButtons and RadioButtons instead of dropdowns
wherever possible, since they make the options immediately visible without clicking. This
made the dashboard feel more like a proper tool rather than just a notebook with plots.

The most interesting section to build was the outlet heatmap. Row-normalizing by outlet
rather than showing raw counts revealed something the bar chart alone would have missed:
every single outlet concentrated their Gaza coverage at the same high intensity. It was
not a case of Al Jazeera covering Gaza more than others — it was a pattern shared across
all newsrooms in the dataset.

We also ran into a limitation with the framing scatter plots. Because framing data was
only available for Gaza and Ukraine, every scatter had R² = 1.0, which sounds impressive
but is mathematically guaranteed with only two points. We added a note in the notebook
flagging this so the viewer does not misinterpret it as a strong result.

The sentiment section was the most constrained — only four entities across two crises —
so we removed the Top N slider since it added no value and simplified the widget to just
a crisis filter dropdown.

The main challenge this week was making sure the notebook ran end-to-end cleanly from
the database and processed CSV without hardcoded paths breaking on a different machine.
We adjusted the relative paths and tested from the correct working directory.

Next steps are to update the README with instructions for running the dashboard, update
requirements.txt, and make sure all five milestone 2 diary entries are complete before
the submission deadline.