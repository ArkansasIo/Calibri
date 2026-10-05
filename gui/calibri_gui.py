import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

ROOT = Path(__file__).resolve().parents[1]

MODELS = {
    "FLUX.1-dev — Calibri Gates": {
        "config": "configs/calibri.py:cmaes_hpsv3_flux_gates",
        "checkpoint": "weights/flux_gates.json",
    },
    "Qwen-Image — Calibri": {
        "config": "configs/calibri.py:cmaes_qwen_clean_hpsv3_2models_cfg",
        "checkpoint": "weights/qwenimage.json",
    },
    "FLUX.1-dev — Layer": {
        "config": "configs/calibri.py:cmaes_hpsv3_flux_layer",
        "checkpoint": "weights/flux_gates.json",
    },
}

class CalibriGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calibri — Diffusion Calibration Studio")
        self.geometry("1120x760")
        self.minsize(900, 620)
        self.configure(bg="#07111f")
        self.proc = None
        self.log_queue = queue.Queue()
        self.status_queue = queue.Queue()
        self._build_style()
        self._build_ui()
        self.after(100, self._drain_log)
        self._write("Calibri GUI ready. Select a model and run a system check.")

    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#07111f")
        style.configure("Card.TFrame", background="#0b1c2e")
        style.configure("TLabel", background="#0b1c2e", foreground="#d9e8f5", font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#07111f", foreground="#62d9ff", font=("Segoe UI Semibold", 22))
        style.configure("Sub.TLabel", background="#07111f", foreground="#8ea9bd", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI Semibold", 10), padding=(12, 8))
        style.configure("Accent.TButton", background="#087ea4", foreground="white")
        style.map("Accent.TButton", background=[("active", "#0aa6d3")])
        style.configure("TCombobox", fieldbackground="#10283d", background="#10283d", foreground="#e7f5ff")
        style.configure("TEntry", fieldbackground="#10283d", foreground="#e7f5ff")
        style.configure("Status.TLabel", background="#07111f", foreground="#66e3a5", font=("Segoe UI Semibold", 10))

    def _build_ui(self):
        header = ttk.Frame(self)
        header.pack(fill="x", padx=22, pady=(18, 8))
        ttk.Label(header, text="CALIBRI", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Diffusion Transformer calibration and inference control panel", style="Sub.TLabel").pack(anchor="w")

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, padx=22, pady=10)
        left = ttk.Frame(body, style="Card.TFrame", padding=18)
        left.pack(side="left", fill="y", padx=(0, 10))
        right = ttk.Frame(body, style="Card.TFrame", padding=18)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="MODEL & GENERATION").pack(anchor="w", pady=(0, 10))
        self.model = ttk.Combobox(left, values=list(MODELS), state="readonly", width=34)
        self.model.current(0)
        self.model.pack(fill="x", pady=(0, 12))

        ttk.Label(left, text="Prompt").pack(anchor="w")
        self.prompt = tk.Text(left, height=7, width=38, bg="#10283d", fg="#e7f5ff",
                              insertbackground="white", relief="flat", wrap="word")
        self.prompt.insert("1.0", "a futuristic city at sunset")
        self.prompt.pack(fill="x", pady=(4, 12))

        ttk.Label(left, text="Output directory").pack(anchor="w")
        out = ttk.Frame(left)
        out.pack(fill="x", pady=(4, 12))
        self.output = ttk.Entry(out)
        self.output.insert(0, str(ROOT / "outputs" / "gui"))
        self.output.pack(side="left", fill="x", expand=True)
        ttk.Button(out, text="...", width=3, command=self._browse).pack(side="right", padx=(5, 0))

        ttk.Button(left, text="SYSTEM CHECK", command=self.system_check).pack(fill="x", pady=4)
        ttk.Button(left, text="GENERATE IMAGE", style="Accent.TButton", command=self.generate).pack(fill="x", pady=4)
        ttk.Button(left, text="STOP PROCESS", command=self.stop_process).pack(fill="x", pady=4)
        ttk.Button(left, text="OPEN OUTPUTS", command=self.open_outputs).pack(fill="x", pady=4)
        ttk.Button(left, text="BUILD WINDOWS EXE", command=self.build_exe).pack(fill="x", pady=4)

        ttk.Label(right, text="CONSOLE").pack(anchor="w", pady=(0, 8))
        self.console = tk.Text(right, bg="#050b12", fg="#bfe9ff", insertbackground="white",
                               relief="flat", wrap="none", font=("Cascadia Mono", 9))
        self.console.pack(fill="both", expand=True)
        self.status = ttk.Label(self, text="READY", style="Status.TLabel")
        self.status.pack(fill="x", padx=22, pady=(0, 14))

    def _browse(self):
        d = filedialog.askdirectory(initialdir=ROOT / "outputs")
        if d:
            self.output.delete(0, "end")
            self.output.insert(0, d)

    def _write(self, text):
        self.log_queue.put(text.rstrip())

    def _drain_log(self):
        while True:
            try:
                line = self.log_queue.get_nowait()
            except queue.Empty:
                break
            self.console.insert("end", line + "\n")
            self.console.see("end")
        while True:
            try:
                status = self.status_queue.get_nowait()
            except queue.Empty:
                break
            self.status.configure(text=status)
        self.after(100, self._drain_log)

    def _run(self, args, label):
        if self.proc and self.proc.poll() is None:
            messagebox.showwarning("Calibri", "A process is already running.")
            return
        self.status_queue.put(label.upper())
        self._write("$ " + " ".join(map(str, args)))
        def worker():
            try:
                env = os.environ.copy()
                env["PYTHONUNBUFFERED"] = "1"
                self.proc = subprocess.Popen(
                    args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, bufsize=1, env=env
                )
                for line in self.proc.stdout:
                    self._write(line)
                code = self.proc.wait()
                self._write(f"Process exited with code {code}.")
                self.status_queue.put("READY" if code == 0 else f"FAILED ({code})")
            except Exception as e:
                self._write(f"ERROR: {e}")
                self.status_queue.put("ERROR")
            finally:
                self.proc = None
        threading.Thread(target=worker, daemon=True).start()

    def _python(self):
        venv = ROOT / ".venv" / "Scripts" / "python.exe"
        return str(venv if venv.exists() else sys.executable)

    def _accelerate(self):
        venv = ROOT / ".venv" / "Scripts" / "accelerate.exe"
        return str(venv) if venv.exists() else "accelerate"

    def system_check(self):
        code = ("import sys,torch; print('Python:',sys.version); "
                "print('PyTorch:',torch.__version__); "
                "print('CUDA available:',torch.cuda.is_available()); "
                "print('GPU:',torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'); "
                "print('CUDA version:',torch.version.cuda)")
        self._run([self._python(), "-c", code], "System check")

    def generate(self):
        item = MODELS[self.model.get()]
        prompt = self.prompt.get("1.0", "end").strip()
        if not prompt:
            messagebox.showwarning("Calibri", "Enter a prompt.")
            return
        out = Path(self.output.get()).expanduser()
        out.mkdir(parents=True, exist_ok=True)
        args = [
            self._python(), "-m", "accelerate.commands.launch", "scripts/inference.py",
            "--config", item["config"],
            "--checkpoint_path", str(ROOT / item["checkpoint"]),
            "--prompt", prompt,
            "--save_dir", str(out),
        ]
        self._run(args, "Generating")

    def stop_process(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            self._write("Process termination requested.")
            self.status_queue.put("STOPPING")

    def open_outputs(self):
        out = Path(self.output.get()).expanduser()
        out.mkdir(parents=True, exist_ok=True)
        os.startfile(out) if os.name == "nt" else subprocess.Popen(["xdg-open", str(out)])

    def build_exe(self):
        script = ROOT / "scripts" / "build_gui_exe.bat"
        if not script.exists():
            messagebox.showerror("Calibri", "Build script is missing.")
            return
        subprocess.Popen(["cmd", "/c", str(script)], cwd=ROOT)
        self._write("Started Windows EXE build. See the build window for PyInstaller output.")

if __name__ == "__main__":
    CalibriGUI().mainloop()
