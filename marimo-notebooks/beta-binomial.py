import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import altair as alt
    import scipy.stats as stats
    return mo, np, alt, stats

@app.cell
def _(mo):
    mo.md(r"""
         Suppose we are modeling some Binomial process. The probability of success $p$ is unknown to us. It is a latent variable.
         We wish to estimate $p$.
         
         At this stage, we have observed no data, but from our knowledge of the process, we have a prior belief about the value of $p$.
        
         Let's say we believe $p$ is distributed according to a Beta distribution with parameters $\alpha$ and $\beta$. That is
         
         $$
         p \sim \text{Beta}(\alpha, \beta)
         $$
         
          """)



@app.cell
def _(mo):
    alpha_slider = mo.ui.slider(1.5, 10, step=0.01, value=5, label="α")
    beta_slider = mo.ui.slider(1.5, 10, step=0.01, value=3, label="β")
    mo.vstack([alpha_slider, beta_slider])
    return alpha_slider, beta_slider


@app.cell
def _(mo, alt, alpha_slider, beta_slider, np, stats):
    def prior_chart():
        x = np.linspace(0, 1, 1000)
        pdf = stats.beta.pdf(x, alpha_slider.value, beta_slider.value)

        source = alt.Data(values=[
            {"x": float(x_val), "pdf": float(pdf_val)} 
            for x_val, pdf_val in zip(x, pdf)
        ])

        chart = alt.Chart(source).mark_line().encode(
            x='x:Q',
            y=alt.Y('pdf:Q', scale=alt.Scale(domain=[0, 6])),
        ).properties(
            title=f"Beta Distribution - Prior",
            config=alt.Config(axis=alt.AxisConfig(grid=False))
        )
        
        return chart

    mo.ui.altair_chart(prior_chart())
    return

@app.cell
def _(mo):
    n_slider = mo.ui.slider(1, 100, step=1, value=10, label="n")
    n_slider
    return n_slider

@app.cell
def _(mo, n_slider):
    k_slider = mo.ui.slider(0, n_slider.value, step=1, value=0, label="k")
    k_slider
    return k_slider




@app.cell
def _(mo, alt, alpha_slider, beta_slider, np, stats, n_slider, k_slider):
    def posterior_chart():
        x = np.linspace(0, 1, 1000)
        pdf_posterior = stats.beta.pdf(x, alpha_slider.value + k_slider.value, beta_slider.value + n_slider.value - k_slider.value)
        pdf_prior = stats.beta.pdf(x, alpha_slider.value, beta_slider.value)

        source = alt.Data(values=[
            {"x": float(x_val), "type": "Posterior", "pdf": float(pdf_posterior_val)}
            for x_val, pdf_posterior_val in zip(x, pdf_posterior)
        ] + [
            {"x": float(x_val), "type": "Prior", "pdf": float(pdf_prior_val)}
            for x_val, pdf_prior_val in zip(x, pdf_prior)
        ])

        chart = alt.Chart(source).mark_line().encode(
            x='x:Q',
            y=alt.Y('pdf:Q', scale=alt.Scale(domain=[0, 24])),
            color=alt.Color('type:N', scale=alt.Scale(domain=['Prior', 'Posterior'], range=['#1f77b4', 'orange']))
        ).properties(
            title=f"Beta Distribution - Prior and Posterior",
            config=alt.Config(axis=alt.AxisConfig(grid=False))
        )
        return chart

    mo.ui.altair_chart(posterior_chart())


if __name__ == "__main__":
    app.run()
