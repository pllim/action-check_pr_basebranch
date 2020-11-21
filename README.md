# GitHub Action to check if PR is opened against allowed base branch

Check if pull request is opened against the allowed base branch upstream.
Create a `.github/workflows/check_pr_basebranch.yml` with this:

```
name: Check PR base branch

on:
  pull_request_target:
    types: [opened, synchronize, labeled, unlabeled]

jobs:
  basebranch:
    name: Check if base branch is correct
    runs-on: ubuntu-latest
    steps:
    - name: Check base branch
      uses: pllim/action-check_pr_basebranch@main
      env:
        BASEBRANCH_NAME: master
        SKIP_BASEBRANCH_CHECK_LABEL: skip-basebranch-check
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The allowed base branch is defined by `BASEBRANCH_NAME` (default is `main`).

Optionally, you can also define a label to skip this check using
`SKIP_BASEBRANCH_CHECK_LABEL`. This label must already exist in the upstream
repository. This feature is useful when your workflow involves occasional
pull requests to other branches upstream; e.g., manual backport to an older
release branch.
