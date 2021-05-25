from invoke import task


@task
def setup_dev(c):
    c.run("pre-commit install")
