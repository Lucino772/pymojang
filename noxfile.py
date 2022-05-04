import nox


@nox.session(python=["3.6", "3.7", "3.8", "3.9"])
def tests(session: nox.Session):
    session.install("-r", "requirements-dev.txt")
    session.run("pytest")


@nox.session
def docs(session: nox.Session):
    session.install("-r", "requirements-dev.txt")
    with session.chdir("docs/"):
        session.run("make", "html")


@nox.session
def lint(session: nox.Session):
    session.install("pre-commit")
    session.run("pre-commit", "run", *session.posargs)
