# Contributing to Phatoscope

First of all, thanks for taking the time to contribute to Phatoscope! It's people like you that help Phatoscope come to fruition. :tada:

The following are a set of guidelines for contributing to Phatoscope. Following these guidelines helps contributing to this project easy and transparent. These are mostly guideline, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Contribution Checklist

Before you make any contributions, make sure you follow this list.

- Read [Contributing to Phatoscope](CONTRIBUTING.md).
- Check if the changes are consistent with the [coding style](CONTRIBUTING.md#coding-style), and format your code accordingly.
- Run [unit tests](CONTRIBUTING.md#run-unit-test-with-code-coverage) and check your code coverage rate.

## What contributions can I make?

Contributions to Phatoscope fall into the following categories.

1. To report a bug or a problem with documentation, please file an [issue](https://github.com/phatoscope-io/phatoscope/issues/new/choose) providing the details of the problem. If you believe the issue needs priority attention, please comment on the issue to notify the team.
2. To propose a new feature, please file a new feature request [issue](https://github.com/phatoscope-io/phatoscope/issues/new/choose). Describe the intended feature and discuss the design and implementation with the team and community. Once the team agrees that the plan looks good, go ahead and implement it, following the [Contributing code](CONTRIBUTING.md#contributing-code).
3. To implement a feature or bug-fix for an existing outstanding issue, follow the [Contributing code](CONTRIBUTING.md#contributing-code). If you need more context on a particular issue, comment on the issue to let people know.

## How can I contribute?

### Contributing code

If you have improvements to Phatoscope, send us your pull requests! For those just getting started, see [GitHub workflow](#github-workflow). Make sure to refer to the related issue in your pull request's comment and update CHANGELOG.md.

The Phatoscope team members will review your pull requests, and once it is accepted, the status of the projects to which it is associated will be changed to **Reviewer approved**. This means we are working on submitting your pull request to the internal repository. After the change has been submitted internally, your pull request will be merged automatically on GitHub.

### GitHub workflow

Please create a new branch from an up-to-date master on your fork.

1. Fork the repository on GitHub.
2. Clone your fork to your local machine with `git clone git@github.com:<yourname>/phantoscope.git`.
3. Create a branch with `git checkout -b my-topic-branch`.
4. Make your changes, commit, then push to to GitHub with `git push --set-upstream origin my-topic-branch`.
5. Visit GitHub and make your pull request.

If you have an existing local repository, please update it before you start, to minimize the chance of merge conflicts.

```shell
git remote add upstream https://github.com/zilliztech/phantoscope.git
git checkout master
git pull upstream master
git checkout -b my-topic-branch
```

### General guidelines

Before sending your pull requests for review, make sure your changes are consistent with the guidelines and follow the Phatoscope coding style.

- Include unit tests when you contribute new features, as they help to prove that your code works correctly, and also guard against future breaking changes to lower the maintenance cost.
- Bug fixes also require unit tests, because the presence of bugs usually indicates insufficient test coverage.
- Keep API compatibility in mind when you change code in Phatoscope. Reviewers of your pull request will comment on any API compatibility issues.
- When you contribute a new feature to Phatoscope, the maintenance burden is (by default) transferred to the Phatoscope team. This means that the benefit of the contribution must be compared against the cost of maintaining the feature.


## Coding Style
The coding style used in Phatoscope generally follow [PEP8 Style Guide](https://www.python.org/dev/peps/pep-0008/)


### Format code
Use [autopep8](https://github.com/hhatto/autopep8) for your code

```shell
make lint
```

## Run unit test with code coverage

Before submitting your PR, make sure you have run unit test, and your code coverage rate is >= 90%.


```shell
make test
```
