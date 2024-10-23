import os

import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor

NOTEBOOKS_PATH = "./notebooks"


@pytest.mark.parametrize("notebook", [nb for nb in os.listdir(NOTEBOOKS_PATH) if nb.endswith(".ipynb")])
def test_notebook_exec(notebook):
    with open(os.path.join(NOTEBOOKS_PATH, notebook)) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
        assert ep.preprocess(nb) is not None, f"Got empty notebook for {notebook}"
