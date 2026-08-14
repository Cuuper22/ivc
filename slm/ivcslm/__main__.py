"""Entry point for `python -m ivcslm`.

Exists so the package can be launched without installing a console script,
which is how the GPU runner starts it inside a container.
"""

from .cli import main

main()

