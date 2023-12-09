import platform
import nox
import cProfile, pstats, io
from pstats import SortKey


@nox.session(python=[platform.python_version()])
def tests(session):
    args = session.posargs or ["--cov"]
    session.install("-r", "../requirements.txt")

    pr = cProfile.Profile()
    pr.enable()

    session.run("coverage", "run", "-m", "pytest", *args)
    session.run("coverage", "report")

    pr.disable()

    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    
    print(s.getvalue())
