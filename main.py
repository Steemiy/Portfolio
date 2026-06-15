"""Conventional app entrypoint for local runs and Flet web builds."""

from pathlib import Path
import runpy


runpy.run_path(str(Path(__file__).with_name("main-page.py")), run_name="__main__")
