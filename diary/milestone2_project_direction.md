## Understanding the Project Direction

At the start of Milestone 2, we went back through our Milestone 1 findings to figure
out where to go next. The exploratory analysis gave us a solid picture of which crises
got the most coverage and how reporting varied across outlets and over time, but it was
mostly descriptive. Milestone 2 pushes us toward actually modeling these patterns and
explaining what drives them.

One thing that became clear early on is that the data has some gaps. Framing and
sentiment information is only available for Gaza and Ukraine, which limits how we
can use those features across the full dataset. We had to think carefully about how
to include them without introducing a lot of zeros that could mislead the model.

We also realized that the way we structure the dataset matters a lot for what kind
of modeling we can do. Monthly coverage data gives us a much richer view of how
attention changes over time within each crisis, and building the master table at that
level opened up more analytical possibilities than working at the crisis level alone.

Our overall direction for this milestone is to engineer features that capture real
patterns in the data, build models that can explain coverage variation, and present
the findings in a way that is clear and well-supported.