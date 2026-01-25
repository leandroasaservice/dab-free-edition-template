# Custom DAB Template - Databricks Free Edition

This repository aims to create a scafolding for running projects on [Databricks Free-Edition](https://www.databricks.com/learn/free-edition). Beware of this version limitations before deciding to use this template.

The structure of the template repository is presented below:

```bash
template
 ┣ adr
 ┣ docker
 ┣ docs
 ┣ one-time
 ┣ reports
 ┣ resources
 ┣ sql
 ┃ ┣ ddl
 ┃ ┗ dml
 ┣ src
 ┣ tests
 ┣ .coveragerc
 ┣ databricks.yml.tmpl
 ┣ docker-compose.yml
 ┣ pytest.toml
 ┣ README.md
 ┣ ruff.toml
 ┗ taskfile.dist.yaml
```

## Structure description

- `adr`: directory with Architecture Decision Records. See patterns at Joel Parker Henderson's [repository](https://github.com/joelparkerhenderson/architecture-decision-record).
- `docker`: Docker images needed to develop, run code and tests locally.
- `docs`: directory with general Markdown document files to contribute to the project.
- `one-time`: directory with one-time jobs. These files are not subject to lint or tests. They are considered ad-hoc, and they may be Notebook files, Python files, SQL Files for either exploratory analysis or for a task such as dropping an Unity Catalog Object. It's important to put these jobs within folders referencing the Jira Task/Ticket.
- `reports`: test coverage and other generated reports.
- `resources`: contains YAML files describing Databricks Asset Bundles resources. For more information, read the [official documentation](https://docs.databricks.com/aws/en/dev-tools/bundles/resources).
- `sql`: SQL files ready to production.
  - `ddl`: statements to define catalogs, schemas, volumes, tables, and any other Unity Catalog object.
  - `dml` statements to insert or update Unity Catalog objects.
- `src`: Python files ready to production.
- `tests`: application tests, such as Unity Tests and Integration Tests.
- `.coveragerc`: pytest-cov configuration.
- `docker-compose.yml`: Docker Compose configuration for running tests.
- `pytest.toml`: pytest configuration.
- `ruff.toml`: Ruff linter configuration.
- `taskfile.dist.yaml`: Taskfile template for running common tasks.

## Running Tests Unit Tests

Requires [Taskfile](https://taskfile.dev) and Docker.

```bash
task test
```

Available tasks: `task build`, `task test`, `task test-cov`, `task test-file`, `task shell`, `task clean`.
