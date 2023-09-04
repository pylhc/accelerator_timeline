# Continous Integration Workflows

This package implements different workflows for CI.
They are organised as follows.

### Documentation

The `documentation` workflow triggers on any push to master, builds the documentation and pushes it to the `gh-pages` branch (if the build is successful).
Also on pull requests, but then only uploads an artifact with the generated documentation instead of publishing it.
It runs on `ubuntu-latest` and the lowest supported Python version, `Python 3.9`.
