# Alternative: Use github-script

The logic is simple enough that you can do without this custom Action
and use `github-script` instead, as such, with your own modification
as necessary:

```yaml
    steps:
    - name: Check base branch
      uses: actions/github-script@v3
      if: github.event_name == 'pull_request'
      with:
        script: |
          const skip_label = 'skip-basebranch-check';
          const allowed_basebranch = 'master';
          const pr = context.payload.pull_request;
          if (pr.labels.find(lbl => lbl.name === skip_label)) {
            core.info(`Base branch check is skipped due to the presence of ${skip_label} label`);
            return;
          }
          if (pr.base.ref !== allowed_basebranch) {
            core.setFailed(`PR opened against ${pr.base.ref}, not ${allowed_basebranch}`);
          } else {
            core.info(`PR opened correctly against ${allowed_basebranch}`);
          }
```

Or if you want to check it without any labeling:

```yaml
    steps:
    - name: Check base branch
      uses: actions/github-script@v3
      if: github.event_name == 'pull_request'
      with:
        script: |
          const allowed_basebranch = 'master';
          const pr = context.payload.pull_request;
          if (pr.base.ref !== allowed_basebranch) {
            core.setFailed(`PR opened against ${pr.base.ref}, not ${allowed_basebranch}`);
          } else {
            core.info(`PR opened correctly against ${allowed_basebranch}`);
          }
```

# GitHub Action to check if PR is opened against allowed base branch

Check if pull request is opened against the allowed base branch upstream.
Create a `.github/workflows/check_pr_basebranch.yml` with this:

```yaml
name: Check PR base branch

on:
  pull_request:
    types: [opened, synchronize, labeled, unlabeled]

jobs:
  basebranch:
    name: Check if base branch is correct
    runs-on: ubuntu-latest
    steps:
    - name: Check base branch
      uses: pllim/action-check_pr_basebranch@main
      with:
        BASEBRANCH_NAME: master
        SKIP_BASEBRANCH_CHECK_LABEL: skip-basebranch-check
```

The allowed base branch is defined by `BASEBRANCH_NAME` (default is `main`).

Optionally, you can also define a label to skip this check using
`SKIP_BASEBRANCH_CHECK_LABEL`. This label must already exist in the upstream
repository. This feature is useful when your workflow involves occasional
pull requests to other branches upstream; e.g., manual backport to an older
release branch.

If this action is triggered by something other than a pull request, it
will exit successfully with a no-op.
