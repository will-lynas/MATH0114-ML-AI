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
    alpha_slider = mo.ui.slider(1.5, 10, step=0.01, value=5, label="α")
    beta_slider = mo.ui.slider(1.5, 10, step=0.01, value=3, label="β")
    mo.vstack([alpha_slider, beta_slider])
    return alpha_slider, beta_slider


@app.cell
def _(mo, alt, alpha_slider, beta_slider, np, stats):
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
        title=f"Beta Distribution",
        config=alt.Config(axis=alt.AxisConfig(grid=False))
    )
    
    mo.ui.altair_chart(chart)
    return


if __name__ == "__main__":
    app.run()
