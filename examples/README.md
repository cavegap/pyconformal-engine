# Examples

Standalone scripts that reproduce specific figures from the thesis. These are
thinner than the notebooks: a script does one thing (regenerate one figure)
and is suitable for inclusion in test suites and documentation builds.

When fully implemented, each example will be runnable as

```bash
python -m pyconformal.examples <name>
```

For example, the flagship lunar Mercator demo will be invokable as

```bash
python -m pyconformal.examples lunar_mercator
```

See `src/pyconformal/examples/__init__.py` for the planned catalog.
