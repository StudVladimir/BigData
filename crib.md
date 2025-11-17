# Терминальные команды

## Созадниме python venv и запуск##
`python3 -m venv .venv`
`source .venv/bin/activate`
`deactivate`

## Скачивание jupiter, matlab и запуск jupiter сервера
`python3 -m pip install jupyter jupyterlab`
`python3 -m pip install matplotlib plotly`
`python3 -m jupyter lab hello.ipynb`

## Render quarto notebook to diffrent formats
`quarto render hello.ipynb --to html`
`quarto render hello.ipynb --to docx`

# Authoring
## Preview jupyter notebook
`quarto preview hello.ipynb`