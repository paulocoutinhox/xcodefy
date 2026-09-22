# Contributing to Xcodefy

Thanks for contributing to Xcodefy.

The complete development guide is available in [docs/contribution.md](docs/contribution.md).

Before opening a pull request, run:

```bash
make lint
make coverage
make build
make check
```

The project requires 100% statement and branch coverage. Every top-level class or enum must live in its own module, every source module must have a mirrored unit test module, and every `__init__.py` must remain empty.
