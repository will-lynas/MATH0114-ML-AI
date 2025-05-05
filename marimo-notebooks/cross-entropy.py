import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import altair as alt
    return alt, mo, np


@app.cell
def _(mo):
    mo.md("""
          ## Cross Entropy:

          $$
          t \\ln(y) + (1-t)\\ln(1-y)
          $$
          """)
    return


@app.cell
def _(np):
    def cross_entropy(t, y):
        return - (t * np.log(y) + (1 - t) * np.log(1 - y))
    return (cross_entropy,)


@app.cell
def _(mo):
    slider = mo.ui.slider(0.01, 0.99, step=0.01, value=0.5, label="y")
    slider
    return (slider,)


@app.cell
def _(cross_entropy, slider):
    y_value = slider.value
    ce_t0 = cross_entropy(0, y_value)
    ce_t1 = cross_entropy(1, y_value)
    return ce_t0, ce_t1


@app.cell
def _(alt, ce_t0, ce_t1):
    source = alt.Data(values=[
        {"t": "t=0", "cross_entropy": ce_t0},
        {"t": "t=1", "cross_entropy": ce_t1}
    ])

    chart = alt.Chart(source).mark_bar().encode(
        x='t:N',
        y=alt.Y('cross_entropy:Q', scale=alt.Scale(domain=(0, 5))),
        color='t:N'
    ).properties(title=f"Cross Entropy")

    chart
    return


if __name__ == "__main__":
    app.run()
