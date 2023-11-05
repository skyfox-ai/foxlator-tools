
import os
from typing import List
import pandas as pd
import json

from .stt_providers.ISTTBase import STTResult


def _get_all_reports_from_dir(dir: str):
    files = os.listdir(dir)
    reports_paths = [os.path.join(dir, file) for file in files if file.startswith(
        "report_") and file.endswith(".json")]
    reports: List[List[STTResult]] = []
    for report_path in reports_paths:
        with open(report_path) as user_file:
            stt_result: List[STTResult] = json.loads(user_file.read())
            reports.append(stt_result)
    if not reports:
        raise Exception(f"No reports in {dir}")
    return reports


def create_general_report(reports_dir: str):
    all_reports = _get_all_reports_from_dir(reports_dir)
    general_report = pd.DataFrame(columns=["Original transcription"])
    general_report["Original transcription"] = [
        trans["trans"] for trans in all_reports[0]]
