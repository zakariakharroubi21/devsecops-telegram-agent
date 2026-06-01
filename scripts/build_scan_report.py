import json

def safe_load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


report_lines = []

# SEMGREP
semgrep = safe_load("semgrep-report.json")
semgrep_count = len(semgrep.get("results", [])) if semgrep else "N/A"
report_lines.append(f"Semgrep: {semgrep_count} findings")

# PIP-AUDIT
pip = safe_load("pipaudit-report.json")
pip_count = len(pip.get("vulnerabilities", [])) if pip else "N/A"
report_lines.append(f"Pip-Audit: {pip_count} vulnerabilities")

# GITLEAKS
gitleaks = safe_load("gitleaks-report.json")
gitleaks_count = len(gitleaks) if isinstance(gitleaks, list) else 0
report_lines.append(f"Gitleaks: {gitleaks_count} secrets")

# TRIVY
trivy = safe_load("trivy-report.json")
trivy_count = 0

if trivy:
    for r in trivy.get("Results", []):
        trivy_count += len(r.get("Vulnerabilities", []))

report_lines.append(f"Trivy: {trivy_count} vulnerabilities")

with open("telegram-report.txt", "w") as f:
    f.write("\n".join(report_lines))