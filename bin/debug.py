import subprocess

"""This file exists for debugging purposes only"""

# subprocess.call(["python", "bin/foxlator-tools.py",
#                 'test-stt', '--create-general-report', '--report-dir', "bin/raports/clean"])

subprocess.call(["python", "bin/foxlator-tools.py",
                'test-stt', '--create-general-report', '--report-dir', "bin/raports/clean", "Vosk"])
