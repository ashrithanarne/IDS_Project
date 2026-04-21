Date: April 20, 2026

This week we completed the final milestone of the project. The main deliverable was the
written report, which required us to synthesize everything we had done across the previous
two milestones into a single coherent document. Writing the report helped clarify which
findings were actually central to the project and which were more peripheral.

One decision we made was to structure the report as a formal academic-style article rather
than a casual writeup. This felt more appropriate given that the project draws on an actual
published research report from the Media and Journalism Research Center, and because the
findings have genuine implications for how humanitarian journalism works in practice.

We set up GitHub Pages to host the report publicly. The docs folder serves as the deployment
source, containing the landing page and the PDF. Having a public URL makes the project feel
like a real finished artifact rather than just a collection of notebooks.

Looking back at the full project, the most significant technical decision was restructuring
the master dataset from the crisis level to the monthly level. The original 10-row table
was not sufficient for any meaningful modeling, and moving to 734 rows of monthly data
unlocked temporal features that turned out to be among the strongest predictors in the
regression models. The finding that crisis duration is the strongest negative predictor of
coverage -- meaning longer crises get less attention over time -- was not something we
anticipated at the start, and it only became visible because of that restructuring decision.

The framing and sentiment analysis, while limited to Gaza and Ukraine, added depth to the
quantitative findings and connected the data science work back to the original journalism
research question. Overall the project evolved from a descriptive EDA exercise into
something with a clear analytical argument, which is what we were aiming for.