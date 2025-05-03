import marimo

__generated_with = "0.13.4"
app = marimo.App(
    width="columns",
    layout_file="layouts/output-functions.grid.json",
)


@app.cell(column=0)
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    return (np,)


@app.cell
def _():
    import matplotlib.pyplot as plt
    return (plt,)


@app.cell(column=1)
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


@app.cell(column=2)
def _(max_val, plt, sliders):
    plt.ylim((-max_val, max_val))
    plt.axhline(y=0, color='black', alpha=0.4, linewidth=1)
    plt.bar([f"a{i}" for i in range(len(sliders))],
            [slider.value for slider in sliders]
           )
    return


@app.cell
def _(plt, sliders, softmax_values):
    plt.ylim((0, 1))
    plt.bar([f"a{i}" for i in range(len(sliders))],
            softmax_values
           )
    return


@app.cell
def _(plt, sigmoid_values, sliders):
    plt.ylim((0, 1))
    plt.axhline(y=0.5, color='red', alpha=0.4, linewidth=1)
    plt.bar([f"a{i}" for i in range(len(sliders))],
            sigmoid_values
           )
    return


@app.cell(column=3)
def _(mo):
    mo.md(
        r"""
    ## Activations

    This shows the raw activations of the ouput layer (the slider values) before any activation function has been applied.
    """
    )
    return


@app.cell
def _(mo, sigmoid_result):
    mo.md(
        f"""
    ## Sigmoid

    Here, each activation is passed through a sigmoid function that maps its output to value between 0 and 1.

    The output of a neuron only depends on its own activation, and is independent of the activations of the other neurons.

    This is useful for a network that is making multiple independent binary classifications. E.g. one neuron could answer the question "Does this image contain a dog?" and another might answer the question "Does this image contain a tree?".

    Since the outputs are between 0 and 1, we can interpret each ouput as the probability of a positive classification. E.g. take >0.5 as a "yes" and "no" otherwise.

    In this case the classifications would be:

    {sigmoid_result}
    """
    )
    return


@app.cell
def _(sigmoid_values):
    sigmoid_answers = [(f"a{i}",
                        "Yes ✅" if value > 0.5 else "No ❌" )
                       for (i,value) in enumerate(sigmoid_values)]
    sigmoid_result = "\n".join(f"* {answer[0]}: **{answer[1]}**"
                              for answer in sigmoid_answers)
    return (sigmoid_result,)


@app.cell
def _(mo, softmax_answer):
    mo.md(
        f"""
    ## Softmax

    Here each output is passed through an exponential function then normalised so that the sum of all outputs is 1.

    This is suitable for classification problems with mutually exclusive classes, where the goal is to pick a single class.

    We can just take the largest value as the "selection" of the network.

    Here, that's **{softmax_answer}**
    """
    )
    return


app._unparsable_cell(
    r"""
    _pairs = [(f\"a{i}\", value) for i, value in enumerate(softmax_values)]
    softmax_answer = max(_pairs, keyhlambda x: x[1])[0]
    """,
    name="_"
)


@app.cell(column=4)
def _(np):
    def softmax(x):
        exp_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
        return exp_x / np.sum(exp_x)
    return (softmax,)


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
def _(sigmoid, slider_values):
    sigmoid_values = sigmoid(slider_values)
    return (sigmoid_values,)


@app.cell
def _(slider_values, softmax):
    softmax_values = softmax(slider_values)
    return (softmax_values,)


if __name__ == "__main__":
    app.run()
