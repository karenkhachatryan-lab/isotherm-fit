"""CustomTkinter desktop GUI for isotherm-fit.

Requires the 'gui' extra (`pip install isotherm-fit[gui]`). This module is
imported lazily by the CLI's `gui` command so that customtkinter is not a
hard dependency of the core package.
"""

from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from isotherm_fit import __version__
from isotherm_fit.citation import CITATION_APA, CITATION_BIBTEX
from isotherm_fit.data import load_isotherm_csv
from isotherm_fit.models import fit_all, get_monolayer_reference, select_best_model
from isotherm_fit.report import build_figure, export_json, save_report

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

MODEL_NAMES = ("GAB", "BET", "Peleg")


class IsothermFitApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"isotherm-fit v{__version__}")
        self.geometry("1050x780")
        self.minsize(800, 600)

        self.data = None
        self.results = None
        self.best = None
        self.m0_source = None
        self.canvas = None

        self._build_layout()

    def _build_layout(self) -> None:
        controls = ctk.CTkFrame(self)
        controls.pack(fill="x", padx=10, pady=(10, 5))

        self.path_label = ctk.CTkLabel(controls, text="No file selected", anchor="w")
        self.path_label.pack(side="left", padx=(5, 10), fill="x", expand=True)

        ctk.CTkButton(controls, text="Open CSV...", command=self.open_csv).pack(side="left", padx=5)
        self.fit_button = ctk.CTkButton(
            controls, text="Fit models", command=self.run_fit, state="disabled"
        )
        self.fit_button.pack(side="left", padx=5)

        model_frame = ctk.CTkFrame(self)
        model_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(model_frame, text="Models:").pack(side="left", padx=(5, 10))
        self.model_vars: dict[str, ctk.BooleanVar] = {}
        for name in MODEL_NAMES:
            var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(model_frame, text=name, variable=var).pack(side="left", padx=10)
            self.model_vars[name] = var

        body = ctk.CTkFrame(self)
        body.pack(fill="both", expand=True, padx=10, pady=5)

        self.plot_frame = ctk.CTkFrame(body)
        self.plot_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.metrics_box = ctk.CTkTextbox(body, width=340, font=("Courier New", 12))
        self.metrics_box.pack(side="right", fill="y")

        bottom = ctk.CTkFrame(self)
        bottom.pack(fill="x", padx=10, pady=(5, 10))

        self.save_report_button = ctk.CTkButton(
            bottom, text="Save report (PDF+PNG)", command=self.save_report_dialog, state="disabled"
        )
        self.save_report_button.pack(side="left", padx=5)
        self.save_json_button = ctk.CTkButton(
            bottom, text="Save JSON", command=self.save_json_dialog, state="disabled"
        )
        self.save_json_button.pack(side="left", padx=5)
        ctk.CTkButton(bottom, text="Cite...", command=self.show_citation).pack(side="right", padx=5)

        self.status_label = ctk.CTkLabel(bottom, text="", anchor="w")
        self.status_label.pack(side="left", padx=15, fill="x", expand=True)

    def open_csv(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not path:
            return
        try:
            data = load_isotherm_csv(path)
        except Exception as exc:
            messagebox.showerror("Error loading CSV", str(exc))
            return

        self.data = data
        self.csv_path = Path(path)
        self.results = self.best = self.m0_source = None
        self.path_label.configure(text=f"{self.csv_path.name}  ({len(self.data)} points)")
        self.fit_button.configure(state="normal")
        self.save_report_button.configure(state="disabled")
        self.save_json_button.configure(state="disabled")
        self.status_label.configure(text="")
        self._clear_plot()
        self.metrics_box.delete("1.0", "end")

    def run_fit(self) -> None:
        if self.data is None:
            return
        selected = tuple(name for name in MODEL_NAMES if self.model_vars[name].get())
        if not selected:
            messagebox.showwarning("No models selected", "Select at least one model to fit.")
            return
        try:
            self.results = fit_all(self.data, selected)
        except Exception as exc:
            messagebox.showerror("Fit failed", str(exc))
            return

        self.best = select_best_model(self.results, n_total=len(self.data))
        self.m0_source = get_monolayer_reference(self.results)
        self._render_plot()
        self._render_metrics()
        self.save_report_button.configure(state="normal")
        self.save_json_button.configure(state="normal")
        self.status_label.configure(
            text=f"Best model (AIC): {self.best.model_name}" +
            (f"   |   m0 ({self.m0_source.model_name}) = {self.m0_source.m0:.4f}" if self.m0_source else "")
        )

    def _clear_plot(self) -> None:
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

    def _render_plot(self) -> None:
        self._clear_plot()
        fig = build_figure(self.data, self.results, self.best, m0_source=self.m0_source)
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _render_metrics(self) -> None:
        self.metrics_box.delete("1.0", "end")
        lines = [f"Data points: {len(self.data)}", ""]
        for r in self.results:
            if r.model_name == self.best.model_name:
                marker = "  <- best (AIC)"
            elif r.n_points != len(self.data):
                marker = f"  (subset n={r.n_points}, AIC n/a)"
            else:
                marker = ""
            lines.append(f"{r.model_name}{marker}")
            lines.append(f"  R2   = {r.r2:.4f}")
            lines.append(f"  RMSE = {r.rmse:.4f}")
            lines.append(f"  AIC  = {r.aic:.2f}")
            for pname, pval in r.params.items():
                perr = r.param_errors.get(pname, float("nan"))
                lines.append(f"  {pname:>4s} = {pval:10.4f} +/- {perr:.4f}")
            lines.append("")
        if self.m0_source is not None:
            lines.append(f"m0 (stability), from {self.m0_source.model_name}: {self.m0_source.m0:.4f}")
        self.metrics_box.insert("1.0", "\n".join(lines))

    def save_report_dialog(self) -> None:
        if self.best is None:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf"), ("PNG", "*.png")]
        )
        if not path:
            return
        stem = Path(path).with_suffix("")
        saved = save_report(
            self.data, self.results, self.best, stem, formats=("pdf", "png"), m0_source=self.m0_source
        )
        messagebox.showinfo("Report saved", "Saved:\n" + "\n".join(str(p) for p in saved))

    def save_json_dialog(self) -> None:
        if self.best is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        stem = Path(path).with_suffix("")
        out = export_json(self.data, self.results, self.best, stem, m0_source=self.m0_source)
        messagebox.showinfo("JSON saved", f"Saved: {out}")

    def show_citation(self) -> None:
        win = ctk.CTkToplevel(self)
        win.title("Cite isotherm-fit")
        win.geometry("620x380")
        box = ctk.CTkTextbox(win, font=("Courier New", 12))
        box.pack(fill="both", expand=True, padx=10, pady=10)
        box.insert("1.0", CITATION_APA + "\n\n" + CITATION_BIBTEX)
        box.configure(state="disabled")


def main() -> None:
    app = IsothermFitApp()
    app.mainloop()


if __name__ == "__main__":
    main()
