import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import altair as alt
    import scipy.stats as stats
    return alt, mo, np, stats


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
    return


@app.cell
def _(mo):
    alpha_slider = mo.ui.slider(1.5, 10, step=0.01, value=5, label="α")
    beta_slider = mo.ui.slider(1.5, 10, step=0.01, value=3, label="β")
    mo.vstack([alpha_slider, beta_slider])
    return alpha_slider, beta_slider


@app.cell
def _(alpha_slider, alt, beta_slider, mo, np, stats):
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
def _(alpha_slider, beta_slider, mo):
    mo.md(f"""
        The **Expected Value** of the Beta distribution is given by

        $$
         \\mathbb{{E}}[p] = \\frac{{\\alpha}}{{\\alpha + \\beta}}
          = \\frac{{{alpha_slider.value}}}{{{alpha_slider.value} + {beta_slider.value}}}
          = {alpha_slider.value / (alpha_slider.value + beta_slider.value):.3f}
        $$

        So this represents our single point estimate of $p$ before we have observed any data.
         """)
    return


@app.cell
def _(mo):
    mo.md(r"""
        Now, let's observe some data by doing a Binomial experiment with $n$ trials.
        """)
    return


@app.cell
def _(mo):
    n_slider = mo.ui.slider(1, 100, step=1, value=10, label="n")
    n_slider
    return (n_slider,)


@app.cell
def _(alpha_slider, beta_slider, mo, n_slider):
    mean_p = alpha_slider.value / (alpha_slider.value + beta_slider.value)
    mo.md(f"""
        With  $n = {n_slider.value}$ trials, we expect to see
        $n * \\mathbb{{E}}[p] = {n_slider.value} * {mean_p:.3f} = {n_slider.value * mean_p:.1f}$ successes, based on our prior belief.
        """)
    return


@app.cell
def _(mo, n_slider):
    k_slider = mo.ui.slider(0, n_slider.value, step=1, value=0, label="k")
    k_slider
    return (k_slider,)


@app.cell
def _(k_slider, mo):
    mo.md(f"""
        What if, instead, we observe $k = {k_slider.value}$ successes?

        Well, we can use Bayes' theorem to update our **prior** belief about $p$, using the observed data, to obtain a **posterior** belief.

        In the case of a $Beta(\\alpha, \\beta)$ prior, with a Binomial likelihood, the posterior is also a Beta distribution:

        $$
        p \\sim \\text{{Beta}}(\\alpha + k, \\beta + n - k)
        $$
        """
        )
    return


@app.cell
def _(alpha_slider, alt, beta_slider, k_slider, mo, n_slider, np, stats):
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
    return posterior_chart


@app.cell
def _(alpha_slider, beta_slider, k_slider, mo, n_slider):
    mo.md(f"""
        After seeing the data, the new **Expected Value** of $p$ is given by

        $$
         \\mathbb{{E}}[p] = \\frac{{\\alpha + k}}{{\\alpha + \\beta + n - k}}
          = \\frac{{{alpha_slider.value} + {k_slider.value}}}{{{alpha_slider.value} + {beta_slider.value} + {n_slider.value} - {k_slider.value}}}
          = {((alpha_slider.value + k_slider.value) / (alpha_slider.value + beta_slider.value + n_slider.value - k_slider.value)):.3f}
        $$
         """)
    return

@app.cell
def _(mo):
    mo.md(r"""
        Notice, the higher the value of $n$, the more confident we are about the value of $p$.
          This is reflected in a tighter posterior distribution.
        """)
    return

@app.cell
def _(mo):
    mo.md(r"""
        Here are the sliders and the graph again, without the text in the way:
        """)
    return

@app.cell
def _(mo, k_slider, n_slider, alpha_slider, beta_slider):
    mo.vstack([alpha_slider, beta_slider, n_slider, k_slider])
    return

@app.cell
def _(mo, posterior_chart):
    mo.ui.altair_chart(posterior_chart())
    return


if __name__ == "__main__":
    app.run()
