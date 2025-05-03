import marimo

__generated_with = "0.13.4"
app = marimo.App(
    width="medium",
    layout_file="layouts/output-functions.grid.json",
)


@app.cell
def _():
    import matplotlib.pyplot as plt
    return (plt,)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    max_val = 5
    return (max_val,)


@app.cell
def _(max_val, mo):
    start_values = [1,5,2,3]
    sliders = mo.ui.array([
        mo.ui.slider(0, max_val, label=f"a{i}", value=value, step=0.1)
        for i,value in enumerate(start_values)
    ])
    return (sliders,)


@app.cell
def _(mo, sliders):
    mo.vstack(sliders)
    return


@app.cell
def _(max_val, plt, sliders):
    plt.ylim(top=max_val)
    plt.bar([f"a{i}" for i in range(len(sliders))],
            [slider.value for slider in sliders]
           )
    return


if __name__ == "__main__":
    app.run()
