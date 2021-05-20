import os
import sys
import tempfile
import traceback

from .multicomp import run_cmd


def sage_code(s):
	tempname = ''
	with tempfile.NamedTemporaryFile(mode="w", delete=False, dir=os.getcwd(), suffix='.sage') as f:
		tempname = f.name
		f.write(s)
	res = run_cmd(['sage', tempname])
	try:
		os.unlink(tempname)
		os.unlink(tempname + '.py')
	except FileNotFoundError:
		pass
	return res


def add_sage_to_path(root=None):
	local: str = None
	if root is None:
		if "SAGE_ROOT" in os.environ:
			root = os.path.abspath(os.environ["SAGE_ROOT"])
			local = f"{root}/local"
		else:
			return False
	else:
		root = os.path.abspath(root)
		local = f"{root}/local"

	version = f"{sys.version_info.major}.{sys.version_info.minor}"
	# The first two are not present in my installation.
	# Maybe they are not needed but I can't say for sure.
	# There's no downside to adding these 2 in the path, so here goes nothing
	python_path = [
	    f"{local}/lib/python",
	    f"{local}/lib/python{version}/lib-dynload",
	    f"{local}/lib/python{version}/site-packages",
	]
	sys.path.extend(python_path)
	paths = {
	    "SAGE_ROOT": root,
	    "SAGE_LOCAL": f"{root}/local",
	    "DOT_SAGE": "~/.sage/",
	    "SAGE_SERVER": "http://www.sagemath.org/",
	    "PATH": f"{root}/local/bin:" + os.environ["PATH"],
	}
	os.environ.update(paths)
	try:
		import sage.all
	except:
		traceback.print_exc()
	return True
