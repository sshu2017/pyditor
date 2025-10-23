import subprocess
import sys
import tempfile
from pathlib import Path

DEFALT_TIMEOUT = 5  # seconds


def run_code(source: str, timeout: int = DEFALT_TIMEOUT):
    with tempfile.NamedTemporaryFile(
        "w", suffix=".py", delete=False, encoding="utf-8"
    ) as tmp_file:
        tmp_file.write(source)
        tmp_file_path = Path(tmp_file.name)

    try:
        completed = subprocess.run(
            [sys.executable, str(tmp_file_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return completed.stdout, completed.stderr, completed.returncode
    except subprocess.TimeoutExpired:
        return "", f"Execution timed out after {timeout} seconds.", -1
    finally:
        try:
            tmp_file_path.unlink()  # Clean up the temporary file
        except Exception:
            pass
