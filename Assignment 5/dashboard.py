from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.h2("Shiny WORKKK! 🚀"),
    ui.input_slider("n", "Choose number", 0, 100, 50),
    ui.output_text_verbatim("result"),
)

def server(input, output, session):
    @output
    @render.text
    def result():
        return f"YOU ChoSeee: {input.n()}"

app = App(app_ui, server)
