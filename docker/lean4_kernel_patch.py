"""
lean4_kernel_patch.py

lean4-jupyter の Lean4Kernel に --% python マジックコマンドを追加するパッチ。

--% python で始まるセルはPythonとして実行し、IPython.display の出力を
Jupyter に返す。これにより lean4_viz などのPythonライブラリを
Lean4カーネルのnotebookから直接呼び出せる。

使用例（notebookセル内）:
    --% python
    import lean4_viz
    lean4_viz.show_latex(r"\forall n \in \mathbb{N},\ n + 0 = n")
"""

import re
import sys

KERNEL_PATH = "/usr/local/lib/python3.12/dist-packages/lean4_jupyter/kernel.py"

PYTHON_MAGIC_CODE = '''
    def _exec_python_magic(self, code: str):
        """Execute Python code from a --% python magic cell and send display outputs."""
        import io
        import traceback
        from IPython.core.interactiveshell import InteractiveShell
        from IPython.utils.capture import capture_output

        # Remove the --% python header line
        lines = code.splitlines()
        python_code = "\\n".join(
            line for line in lines if line.strip() != "--% python"
        )

        shell = getattr(self, "_python_shell", None)
        if shell is None:
            shell = InteractiveShell.instance()
            self._python_shell = shell

        outputs = []

        def _display_pub_handler(msg):
            data = msg.get("content", {}).get("data", {})
            metadata = msg.get("content", {}).get("metadata", {})
            if data:
                outputs.append((data, metadata))

        # Capture display_data messages via display publisher
        original_publish = shell.display_pub.publish

        def patched_publish(data=None, metadata=None, **kwargs):
            if data:
                outputs.append((data, metadata or {}))
            original_publish(data=data, metadata=metadata, **kwargs)

        shell.display_pub.publish = patched_publish
        try:
            with capture_output() as captured:
                result = shell.run_cell(python_code)
        finally:
            shell.display_pub.publish = original_publish

        # Send captured display outputs
        for data, metadata in outputs:
            self.send_response(self.iopub_socket, "display_data", {
                "metadata": metadata,
                "data": data,
            })

        # Send stdout if any
        if captured.stdout:
            self.send_response(self.iopub_socket, "stream", {
                "name": "stdout",
                "text": captured.stdout,
            })

        # Send stderr or error info
        if captured.stderr:
            self.send_response(self.iopub_socket, "stream", {
                "name": "stderr",
                "text": captured.stderr,
            })

        if result.error_in_exec is not None:
            tb = traceback.format_exception(
                type(result.error_in_exec),
                result.error_in_exec,
                result.error_in_exec.__traceback__,
            )
            return {
                "status": "error",
                "execution_count": self.execution_count,
                "ename": type(result.error_in_exec).__name__,
                "evalue": str(result.error_in_exec),
                "traceback": tb,
            }

        return {
            "status": "ok",
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }

'''

DO_EXECUTE_PATCH = '''    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        # --% python magic: execute as Python and return IPython display outputs
        stripped = code.strip()
        if stripped.startswith("--% python"):
            return self._exec_python_magic(stripped)

        # try:
'''

with open(KERNEL_PATH, "r") as f:
    src = f.read()

# Insert _exec_python_magic method before do_execute
if "_exec_python_magic" in src:
    print("Patch already applied, skipping.")
    sys.exit(0)

# Find the do_execute method and insert the new method before it
old_do_execute = '''    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        # try:'''

if old_do_execute not in src:
    print(f"ERROR: Could not find do_execute signature in {KERNEL_PATH}", file=sys.stderr)
    print("Current do_execute area:", file=sys.stderr)
    idx = src.find("def do_execute")
    print(src[idx:idx+200], file=sys.stderr)
    sys.exit(1)

patched = src.replace(
    old_do_execute,
    PYTHON_MAGIC_CODE + DO_EXECUTE_PATCH
)

with open(KERNEL_PATH, "w") as f:
    f.write(patched)

print(f"Successfully patched {KERNEL_PATH}")
print("Added --% python magic command support to Lean4Kernel.")
