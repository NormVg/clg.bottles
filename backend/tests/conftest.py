import os
import tempfile

# Point every test at a throwaway database before the app is imported.
os.environ["CLG_BOTTLES_DB"] = os.path.join(tempfile.mkdtemp(), "test.db")
