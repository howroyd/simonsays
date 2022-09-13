import pathlib
import pytest
import sys

if __name__ == "__main__":
    path = pathlib.Path().resolve()

    sys.exit(
        pytest.main(
            [
                f'--cov={path}',
                '--cov-report=html',
                'tests'
            ]
        )
    )