import marimo

__generated_with = "0.13.4"
app = marimo.App(
    width="medium",
    layout_file="layouts/output-functions.grid.json",
)


@app.cell
def _():
    max_val = 5
    return (max_val,)


@app.cell
def _(max_val, mo):
    start_values = [3,-1,5,-4]
    sliders = mo.ui.array([
        mo.ui.slider(-max_val, max_val, label=f"a{i}", value=value, step=0.1)
        for i,value in enumerate(start_values)
    ])
    return (sliders,)


@app.cell
def _(mo, sliders):
    mo.vstack(sliders)
    return


@app.cell
def _(max_val, plt, sliders):
    plt.ylim((-max_val, max_val))
    plt.axhline(y=0, color='black', alpha=0.4, linewidth=1)
    plt.bar([f"a{i}" for i in range(len(sliders))],
            [slider.value for slider in sliders]
           )
    return


@app.cell
def _(plt, sigmoid, slider_values, sliders):
    sigmoid_values = sigmoid(slider_values)

    plt.ylim((0, 1))
    plt.bar([f"a{i}" for i in range(len(sliders))],
            sigmoid_values
           )
    return


@app.cell
def _(np):
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
    return (sigmoid,)


@app.cell
def _(np, sliders):
    slider_values = np.array([slider.value for slider in sliders])
    return (slider_values,)


@app.cell
def _():
    import numpy as np
    return (np,)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import matplotlib.pyplot as plt
    return (plt,)


if __name__ == "__main__":
    app.run()
