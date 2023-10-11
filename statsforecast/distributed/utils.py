# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/src/distributed.utils.ipynb.

# %% auto 0
__all__ = ['forecast', 'cross_validation']

# %% ../../nbs/src/distributed.utils.ipynb 4
from typing import Optional

from ..core import ParallelBackend

# %% ../../nbs/src/distributed.utils.ipynb 5
def forecast(
    df,
    models,
    freq,
    h,
    fallback_model=None,
    X_df=None,
    level=None,
    parallel: Optional["ParallelBackend"] = None,
):
    backend = parallel if parallel is not None else ParallelBackend()
    return backend.forecast(
        df, models, freq, fallback_model, h=h, X_df=X_df, level=level
    )

# %% ../../nbs/src/distributed.utils.ipynb 6
def cross_validation(
    df,
    models,
    freq,
    h,
    n_windows=1,
    step_size=1,
    test_size=None,
    input_size=None,
    parallel: Optional["ParallelBackend"] = None,
):
    backend = parallel if parallel is not None else ParallelBackend()
    return backend.cross_validation(
        df,
        models,
        freq,
        h=h,
        n_windows=n_windows,
        step_size=step_size,
        test_size=test_size,
        input_size=input_size,
    )
