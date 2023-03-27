import os

import nox


@nox.session(python=["3.7", "3.8", "3.9"], venv_backend="venv")
def tests(session: nox.Session):
    session.install("-r", "requirements/requirements-tests.txt")
    session.install(".")
    session.run("pytest")


@nox.session
def docs(session: nox.Session):
    session.install("-r", "requirements/requirements-docs.txt")
    session.install(".")

    if "--serve" in session.posargs:
        session.run(
            "sphinx-autobuild",
            "-b",
            "dirhtml",
            "docs/",
            "docs/_build/html/",
            "--open-browser",
        )
    else:
        session.run(
            "sphinx-build", "-b", "dirhtml", "docs/", "docs/_build/html/"
        )


@nox.session
def lint(session: nox.Session):
    session.install("pre-commit")
    session.run("pre-commit", "run", *session.posargs)


@nox.session
def example(session: nox.Session):
    session.install(".")
    with session.chdir("examples/microsoft_flask"):
        session.install("-r", "requirements.txt")
        session.run("python", "app.py")


@nox.session
def build(session: nox.Session):
    session.install("build")
    session.run("python", "-m", "build")


@nox.session
def upload(session: nox.Session):
    session.install("twine")
    upload_cmd = []
    if os.path.exists(".env.deploy"):
        session.install("python-dotenv[cli]")
        upload_cmd = ["dotenv", "-f", ".env.deploy", "run", "--"]

    upload_cmd.extend(["twine", "upload", "dist/*"])
    session.run(*upload_cmd)
