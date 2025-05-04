import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    return (np,)


@app.cell
def _():
    import altair as alt
    return (alt,)


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
def _(alt, max_val, mo, sliders):
    def create_activation_chart():
        data = [{"name": f"a{i}", "value": slider.value} for i, slider in enumerate(sliders)]
        chart = alt.Chart(alt.Data(values=data)).mark_bar().encode(
            x='name:N',
            y=alt.Y('value:Q', scale=alt.Scale(domain=(-max_val, max_val))),
        ).properties(width=200, height=200)

        rule = alt.Chart(alt.Data(values=[{"y": 0}])).mark_rule(color='black', opacity=0.4).encode(y='y:Q')

        return chart + rule

    activation_chart = create_activation_chart()
    mo.ui.altair_chart(activation_chart)
    return


@app.cell
def _(alt, mo, softmax_values):
    def create_softmax_chart():
        data = [{"name": f"a{i}", "value": value} for i, value in enumerate(softmax_values)]
        chart = alt.Chart(alt.Data(values=data)).mark_bar().encode(
            x='name:N',
            y=alt.Y('value:Q', scale=alt.Scale(domain=(0, 1))),
        ).properties(width=200, height=200)
        return chart

    softmax_chart = create_softmax_chart()
    mo.ui.altair_chart(softmax_chart)
    return


@app.cell
def _(alt, mo, sigmoid_values):
    def create_sigmoid_chart():
        data = [{"name": f"a{i}", "value": value} for i, value in enumerate(sigmoid_values)]
        chart = alt.Chart(alt.Data(values=data)).mark_bar().encode(
            x='name:N',
            y=alt.Y('value:Q', scale=alt.Scale(domain=(0, 1))),
        ).properties(width=200, height=200)

        rule = alt.Chart(alt.Data(values=[{"y": 0.5}])).mark_rule(color='red', opacity=0.4).encode(y='y:Q')

        return chart + rule

    sigmoid_chart = create_sigmoid_chart()
    mo.ui.altair_chart(sigmoid_chart)
    return


@app.cell
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


@app.cell
def _(softmax_values):
    _pairs = [(f"a{i}", value) for i, value in enumerate(softmax_values)]
    softmax_answer = max(_pairs, key=lambda x: x[1])[0]
    return (softmax_answer,)


@app.cell
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
