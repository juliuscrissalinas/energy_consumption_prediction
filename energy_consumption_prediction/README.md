# energy_consumption_prediction

Predicts energy consumption using time series

## Project Structure

```text
energy_consumption_prediction
|-- bin/                         # CLI scripts
|-- notebooks
|   |-- *.ipynb                  # Jupyter notebooks
|   `-- my_nb_path.py            # Imported by *.ipynb to treat src/ as PYTHONPATH
|-- requirements/                # Dependencies required by this project
|-- src                          # Python modules developed in this project
|   |-- ec_prediction
|   `-- my_nb_color.py           # Imported by *.ipynb to colorize their outputs
|-- tests/                       # Unit tests
|-- MANIFEST.in                  # Required by setup.py
|-- setup.py                     # To pip install ec_prediction

# Miscellaneous files
|-- .editorconfig                # Editor config (for IDE / editor that support this)
|-- .gitattributes               # Files that Git must give special treatments
|-- .gitignore                   # Git ignore list
|-- .pre-commit-config.yaml      # Precommit hooks
|-- LICENSE                      # License
|-- README.md                    # Template document
|-- pyproject.toml               # Settings for select Python toolchains
`-- tox.ini                      # Settings for select Python toolchains
```

## Credits

This project was initialized by Julius Cris Salinas using:

```bash
cookiecutter https://github.com/aws-samples/python-data-science-template
```

## License

This library is licensed under the No license file.
