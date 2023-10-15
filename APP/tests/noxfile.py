import platform
import nox


@nox.session(python=[platform.python_version()])
def tests(session):
    args = session.posargs or ["--cov"]
    session.install("-r", "../requirements.txt")
    session.run("coverage", "run", "-m", "pytest", *args)
    session.run("coverage", "report")
