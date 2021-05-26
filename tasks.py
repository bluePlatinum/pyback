from invoke import task


@task
def setup_dev(c):
    c.run("pre-commit install")


@task
def lint(c, scope):
    if scope == "all":
        c.run("flake8 src tests tasks.py setup.py")
    elif scope == "src":
        c.run("flake8 src")
    elif scope == "tests":
        c.run("flake8 tests")
