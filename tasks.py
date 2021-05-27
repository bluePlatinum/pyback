import os
import platform
from invoke import task


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


@task
def clean(c, target):
    if target == "all":
        clean_build(c)
        clean_dist(c)
        clean_tox(c)
    elif target == "build":
        clean_build(c)
    elif target == "dist":
        clean_dist(c)
    elif target == "tox":
        clean_tox(c)


@task
def clean_build(c):
    if platform.system() == "Linux":
        c.run("rm -r ./build") if os.path.isdir("./build") else False
    elif platform.system() == "Windows":
        c.run("rd /s /q .\\build") if os.path.isdir(".\\build") else False


@task
def clean_dist(c):
    if platform.system() == "Linux":
        c.run("rm -r ./dist") if os.path.isdir("./dist") else False
    elif platform.system() == "Windows":
        c.run("rd /s /q .\\dist") if os.path.isdir(".\\dist") else False


@task
def clean_tox(c):
    if platform.system() == "Linux":
        c.run("rm -r ./.tox") if os.path.isdir("./.tox") else False
    elif platform.system() == "Windows":
        c.run("rd /s /q .\\.tox") if os.path.isdir(".\\.tox") else False


@task
def lint(c, scope):
    if scope == "all":
        c.run("flake8 src tests tasks.py setup.py")
    elif scope == "src":
        c.run("flake8 src")
    elif scope == "tests":
        c.run("flake8 tests")


@task
def setup_dev(c):
    c.run("pre-commit install")
