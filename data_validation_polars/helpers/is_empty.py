import polars as pl
import polars.selectors as cs


def is_empty(df: pl.DataFrame) -> bool:
    return df.with_columns(
        pl.all().is_null()
    ).with_columns(
        cs.float().is_nan()
    )
