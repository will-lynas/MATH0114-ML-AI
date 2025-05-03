import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    slider = mo.ui.slider(1,9)
    slider
    return (slider,)


@app.cell
def _():
    import matplotlib.pyplot as plt
    return (plt,)


@app.cell
def _(plt, slider):
    plt.bar([1,2,3], [slider.value, 2, 4])
    return


if __name__ == "__main__":
    app.run()
