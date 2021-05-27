import platform
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


@task
def build(c, target):
    if target == "package":
        c.run("python -m build --sdist")
        c.run("python -m build --wheel")
    elif target == "docs":
        if platform.system() == "Linux":
            c.run("make -C ./docs html")
        elif platform.system() == "Windows":
            c.run(".\\docs\\make.bat html")
