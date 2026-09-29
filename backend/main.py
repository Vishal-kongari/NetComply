from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="AI-Augmented Network Compliance Engine",
    description="Vendor-agnostic network configuration compliance API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATA DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

CONFIG_DIR = DATA_DIR / "configurations"
REPORT_DIR = DATA_DIR / "reports"
AUDIT_DIR = DATA_DIR / "audit"

CONFIG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():

    return {
        "name": "Network Compliance Engine",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/api/health")
def health():

    return {
        "status": "healthy",
        "service": "network-compliance-engine"
    }


# ============================================================
# VENDOR DETECTION
# ============================================================

def detect_vendor(config: str):

    config_lower = config.lower()

    # Cisco
    if (
        re.search(r"^\s*version\s+\d+", config_lower, re.MULTILINE)
        or "ip ssh version" in config_lower
        or "transport input ssh" in config_lower
        or "hostname " in config_lower
    ):
        return "Cisco"

    # Juniper
    if (
        "set system services ssh" in config_lower
        or "set system services telnet" in config_lower
        or "set interfaces " in config_lower
        or "set system syslog" in config_lower
    ):
        return "Juniper"

    # Fortinet
    if (
        "config system global" in config_lower
        or "config system interface" in config_lower
        or "config system settings" in config_lower
    ):
        return "Fortinet"

    # Palo Alto
    if (
        "set deviceconfig" in config_lower
        or "set mgt-config" in config_lower
        or "set network" in config_lower
    ):
        return "Palo Alto"

    # Arista
    if (
        "management api http-commands" in config_lower
        or "daemon terminattr" in config_lower
    ):
        return "Arista"

    return "Unknown"


# ============================================================
# DEVICE INFORMATION
# ============================================================

def extract_device_information(config: str, vendor: str):

    device = {
        "vendor": vendor,
        "hostname": None,
        "model": None,
        "os": None,
        "version": None
    }

    # Cisco hostname
    hostname_match = re.search(
        r"^\s*hostname\s+(.+)$",
        config,
        re.MULTILINE
    )

    if hostname_match:
        device["hostname"] = hostname_match.group(1).strip()

    # Cisco version
    version_match = re.search(
        r"^\s*version\s+([\w.\-]+)",
        config,
        re.MULTILINE
    )

    if version_match:
        device["version"] = version_match.group(1)
        device["os"] = "IOS / IOS-XE"

    # Generic model
    model_match = re.search(
        r"(?:model|Model|MODEL)[\s:=]+([A-Za-z0-9._\-]+)",
        config
    )

    if model_match:
        device["model"] = model_match.group(1)

    return device


# ============================================================
# CONFIGURATION NORMALIZATION
# ============================================================

def normalize_config(config: str, vendor: str):

    normalized = {

        "ssh": {
            "enabled": None,
            "version": None
        },

        "telnet": {
            "enabled": None
        },

        "http": {
            "enabled": None
        },

        "logging": {
            "enabled": False
        },

        "ntp": {
            "enabled": None
        },

        "snmp": {
            "enabled": None,
            "version": None
        }
    }


    # ========================================================
    # CISCO
    # ========================================================

    if vendor == "Cisco":

        # SSH
        if re.search(
            r"ip ssh version 2",
            config,
            re.IGNORECASE
        ):
            normalized["ssh"]["enabled"] = True
            normalized["ssh"]["version"] = 2

        elif re.search(
            r"ip ssh version 1",
            config,
            re.IGNORECASE
        ):
            normalized["ssh"]["enabled"] = True
            normalized["ssh"]["version"] = 1

        elif re.search(
            r"transport input ssh",
            config,
            re.IGNORECASE
        ):
            normalized["ssh"]["enabled"] = True


        # Telnet
        if re.search(
            r"transport input.*telnet",
            config,
            re.IGNORECASE
        ):
            normalized["telnet"]["enabled"] = True

        elif re.search(
            r"transport input ssh",
            config,
            re.IGNORECASE
        ):
            normalized["telnet"]["enabled"] = False


        # HTTP
        if re.search(
            r"^\s*ip http server",
            config,
            re.MULTILINE | re.IGNORECASE
        ):
            normalized["http"]["enabled"] = True

        elif re.search(
            r"^\s*no ip http server",
            config,
            re.MULTILINE | re.IGNORECASE
        ):
            normalized["http"]["enabled"] = False


        # Logging
        if re.search(
            r"logging host",
            config,
            re.IGNORECASE
        ):
            normalized["logging"]["enabled"] = True


        # NTP
        if re.search(
            r"^\s*ntp server",
            config,
            re.MULTILINE | re.IGNORECASE
        ):
            normalized["ntp"]["enabled"] = True


        # SNMP
        if re.search(
            r"snmp-server",
            config,
            re.IGNORECASE
        ):
            normalized["snmp"]["enabled"] = True

            if re.search(
                r"snmp-server.*group.*v3",
                config,
                re.IGNORECASE
            ):
                normalized["snmp"]["version"] = 3


    # ========================================================
    # JUNIPER
    # ========================================================

    elif vendor == "Juniper":

        # SSH
        if re.search(
            r"set system services ssh",
            config,
            re.IGNORECASE
        ):
            normalized["ssh"]["enabled"] = True

        if re.search(
            r"protocol-version\s+v2",
            config,
            re.IGNORECASE
        ):
            normalized["ssh"]["version"] = 2


        # Telnet
        if re.search(
            r"set system services telnet",
            config,
            re.IGNORECASE
        ):
            normalized["telnet"]["enabled"] = True

        else:
            normalized["telnet"]["enabled"] = False


        # HTTP
        if re.search(
            r"set system services web-management",
            config,
            re.IGNORECASE
        ):
            normalized["http"]["enabled"] = True

        else:
            normalized["http"]["enabled"] = False


        # Logging
        if re.search(
            r"set system syslog",
            config,
            re.IGNORECASE
        ):
            normalized["logging"]["enabled"] = True


        # NTP
        if re.search(
            r"set system ntp",
            config,
            re.IGNORECASE
        ):
            normalized["ntp"]["enabled"] = True


    # ========================================================
    # UNKNOWN VENDOR
    # ========================================================

    else:

        normalized = normalize_generic(config)


    return normalized


# ============================================================
# GENERIC NORMALIZATION
# ============================================================

def normalize_generic(config: str):

    normalized = {

        "ssh": {
            "enabled": None,
            "version": None
        },

        "telnet": {
            "enabled": None
        },

        "http": {
            "enabled": None
        },

        "logging": {
            "enabled": False
        },

        "ntp": {
            "enabled": None
        },

        "snmp": {
            "enabled": None,
            "version": None
        }
    }


    # SSH
    if re.search(
        r"ssh.*version.*2",
        config,
        re.IGNORECASE
    ):
        normalized["ssh"]["enabled"] = True
        normalized["ssh"]["version"] = 2


    # Telnet
    if re.search(
        r"(disable|no).*telnet",
        config,
        re.IGNORECASE
    ):
        normalized["telnet"]["enabled"] = False

    elif re.search(
        r"enable.*telnet",
        config,
        re.IGNORECASE
    ):
        normalized["telnet"]["enabled"] = True


    # HTTP
    if re.search(
        r"(disable|no).*http",
        config,
        re.IGNORECASE
    ):
        normalized["http"]["enabled"] = False

    elif re.search(
        r"enable.*http",
        config,
        re.IGNORECASE
    ):
        normalized["http"]["enabled"] = True


    # Logging
    if re.search(
        r"(logging|syslog)",
        config,
        re.IGNORECASE
    ):
        normalized["logging"]["enabled"] = True


    return normalized


# ============================================================
# KNOWN COMMAND PATTERNS
# ============================================================

KNOWN_PATTERNS = [

    r"^\s*version\s+",
    r"^\s*hostname\s+",
    r"^\s*ip ssh",
    r"^\s*transport input",
    r"^\s*ip http",
    r"^\s*no ip http",
    r"^\s*logging",
    r"^\s*ntp",
    r"^\s*snmp",
    r"^\s*line vty",

    r"^\s*set system services ssh",
    r"^\s*set system services telnet",
    r"^\s*set system services web-management",
    r"^\s*set system syslog",
    r"^\s*set system ntp",

    r"^\s*config system",
    r"^\s*config firewall",

    r"^\s*set deviceconfig",
    r"^\s*set network"
]


# ============================================================
# UNKNOWN COMMAND DETECTION
# ============================================================

def find_unknown_commands(config: str):

    unknown = []

    for line in config.splitlines():

        line = line.strip()

        if not line:
            continue

        # comments
        if line.startswith("!"):
            continue

        # check known patterns
        known = False

        for pattern in KNOWN_PATTERNS:

            if re.search(
                pattern,
                line,
                re.IGNORECASE
            ):
                known = True
                break

        if not known:
            unknown.append(line)


    # Limit result
    return unknown[:20]


# ============================================================
# COMPLIANCE ENGINE
# ============================================================

def check_compliance(normalized):

    results = []


    # ========================================================
    # RULE 1 - SSH VERSION 2
    # ========================================================

    ssh_version = normalized["ssh"]["version"]

    if ssh_version == 2:

        results.append({

            "rule": "SSH Version 2",

            "status": "PASS",

            "severity": "LOW",

            "evidence":
                "SSH version 2 is configured.",

            "remediation":
                "No action required."
        })

    else:

        results.append({

            "rule": "SSH Version 2",

            "status": "FAIL",

            "severity": "HIGH",

            "evidence":
                "SSH version 2 was not detected.",

            "remediation":
                "Enable SSH version 2."
        })


    # ========================================================
    # RULE 2 - TELNET
    # ========================================================

    telnet = normalized["telnet"]["enabled"]

    if telnet is False:

        results.append({

            "rule": "Disable Telnet",

            "status": "PASS",

            "severity": "LOW",

            "evidence":
                "Telnet is disabled.",

            "remediation":
                "No action required."
        })

    else:

        results.append({

            "rule": "Disable Telnet",

            "status": "FAIL",

            "severity": "CRITICAL",

            "evidence":
                "Telnet is enabled or could not be verified.",

            "remediation":
                "Disable Telnet and use SSH."
        })


    # ========================================================
    # RULE 3 - HTTP
    # ========================================================

    http = normalized["http"]["enabled"]

    if http is False:

        results.append({

            "rule": "Disable HTTP",

            "status": "PASS",

            "severity": "LOW",

            "evidence":
                "HTTP management service is disabled.",

            "remediation":
                "No action required."
        })

    else:

        results.append({

            "rule": "Disable HTTP",

            "status": "FAIL",

            "severity": "HIGH",

            "evidence":
                "HTTP management service is enabled or unknown.",

            "remediation":
                "Disable HTTP management and use HTTPS."
        })


    # ========================================================
    # RULE 4 - LOGGING
    # ========================================================

    if normalized["logging"]["enabled"]:

        results.append({

            "rule": "Enable Centralized Logging",

            "status": "PASS",

            "severity": "LOW",

            "evidence":
                "Logging configuration detected.",

            "remediation":
                "No action required."
        })

    else:

        results.append({

            "rule": "Enable Centralized Logging",

            "status": "FAIL",

            "severity": "MEDIUM",

            "evidence":
                "Centralized logging configuration was not detected.",

            "remediation":
                "Configure a centralized syslog server."
        })


    # ========================================================
    # RULE 5 - NTP
    # ========================================================

    ntp = normalized["ntp"]["enabled"]

    if ntp:

        results.append({

            "rule": "Enable NTP",

            "status": "PASS",

            "severity": "LOW",

            "evidence":
                "NTP configuration detected.",

            "remediation":
                "No action required."
        })

    else:

        results.append({

            "rule": "Enable NTP",

            "status": "FAIL",

            "severity": "MEDIUM",

            "evidence":
                "NTP configuration was not detected.",

            "remediation":
                "Configure a trusted NTP server."
        })


    return results


# ============================================================
# AI-LIKE COMMAND ANALYSIS
# ============================================================

def analyze_unknown_command(command: str):

    """
    Temporary rule-based AI placeholder.

    Replace this function with Ollama later.
    """

    command_lower = command.lower()

    if "ssh" in command_lower:

        return {

            "parameter": "ssh.version",

            "suggested_value": "2",

            "confidence": 0.90,

            "reason":
                "Command appears related to SSH configuration."
        }


    if "telnet" in command_lower:

        return {

            "parameter": "telnet.enabled",

            "suggested_value":
                "true",

            "confidence": 0.88,

            "reason":
                "Command appears related to Telnet."
        }


    if "logging" in command_lower or "syslog" in command_lower:

        return {

            "parameter": "logging.enabled",

            "suggested_value":
                "true",

            "confidence": 0.87,

            "reason":
                "Command appears related to logging."
        }


    return {

        "parameter": "unknown",

        "suggested_value": None,

        "confidence": 0.30,

        "reason":
            "No matching security parameter identified."
    }


# ============================================================
# AI ANALYSIS
# ============================================================

def run_ai_analysis(commands):

    suggestions = []

    for command in commands:

        analysis = analyze_unknown_command(
            command
        )

        suggestions.append({

            "command": command,

            "suggestion": analysis
        })

    return suggestions


# ============================================================
# SHA-256 BLOCKCHAIN-STYLE AUDIT HASH
# ============================================================

def generate_hash(data):

    serialized = json.dumps(
        data,
        sort_keys=True,
        default=str
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()


# ============================================================
# SAVE AUDIT RECORD
# ============================================================

def save_audit_record(report, audit_hash):

    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    audit_file = (
        AUDIT_DIR /
        f"audit_{timestamp}.json"
    )

    record = {

        "hash": audit_hash,

        "algorithm": "SHA-256",

        "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "report": report
    }

    with open(
        audit_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            record,
            f,
            indent=4
        )

    return audit_file


# ============================================================
# SAVE CONFIGURATION
# ============================================================

def save_configuration(
    filename,
    content
):

    safe_name = Path(filename).name

    path = (
        CONFIG_DIR /
        safe_name
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(content)

    return path


# ============================================================
# MAIN ANALYSIS API
# ============================================================

@app.post("/analyze")
async def analyze_configuration(
    file: UploadFile = File(...)
):

    # --------------------------------------------------------
    # Read file
    # --------------------------------------------------------

    raw_data = await file.read()

    config = raw_data.decode(
        "utf-8",
        errors="ignore"
    )


    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    if not config.strip():

        return {

            "success": False,

            "error":
                "Configuration file is empty."
        }


    # --------------------------------------------------------
    # Detect vendor
    # --------------------------------------------------------

    vendor = detect_vendor(
        config
    )


    # --------------------------------------------------------
    # Device information
    # --------------------------------------------------------

    device = extract_device_information(
        config,
        vendor
    )


    # --------------------------------------------------------
    # Normalize
    # --------------------------------------------------------

    normalized = normalize_config(
        config,
        vendor
    )


    # --------------------------------------------------------
    # Unknown commands
    # --------------------------------------------------------

    unknown_commands = (
        find_unknown_commands(
            config
        )
    )


    # --------------------------------------------------------
    # AI analysis
    # --------------------------------------------------------

    ai_analysis = run_ai_analysis(
        unknown_commands
    )


    # --------------------------------------------------------
    # Compliance
    # --------------------------------------------------------

    compliance = check_compliance(
        normalized
    )


    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    passed = sum(
        1
        for item in compliance
        if item["status"] == "PASS"
    )

    failed = sum(
        1
        for item in compliance
        if item["status"] == "FAIL"
    )


    # --------------------------------------------------------
    # Base report
    # --------------------------------------------------------

    report = {

        "success": True,

        "file": file.filename,

        "vendor": vendor,

        "device": device,

        "normalized_configuration":
            normalized,

        "unknown_commands":
            unknown_commands,

        "ai_analysis":
            ai_analysis,

        "compliance":
            compliance,

        "statistics": {

            "total_checks":
                len(compliance),

            "passed":
                passed,

            "failed":
                failed
        },

        "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()
    }


    # --------------------------------------------------------
    # Generate audit hash
    # --------------------------------------------------------

    audit_hash = generate_hash(
        report
    )


    # --------------------------------------------------------
    # Blockchain-style record
    # --------------------------------------------------------

    report["blockchain"] = {

        "hash":
            audit_hash,

        "algorithm":
            "SHA-256",

        "status":
            "Recorded"
    }


    # --------------------------------------------------------
    # Save files
    # --------------------------------------------------------

    save_configuration(
        file.filename,
        config
    )

    save_audit_record(
        report,
        audit_hash
    )


    return report


# ============================================================
# AUDIT HISTORY
# ============================================================

@app.get("/audit-history")
def audit_history():

    records = []

    for file in AUDIT_DIR.glob(
        "audit_*.json"
    ):

        try:

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                records.append(
                    json.load(f)
                )

        except Exception:
            continue


    return {

        "count": len(records),

        "records": records
    }


# ============================================================
# VERIFY AUDIT RECORD
# ============================================================

@app.post("/verify-hash")
async def verify_hash(
    audit_file: str
):

    path = AUDIT_DIR / Path(
        audit_file
    ).name

    if not path.exists():

        return {

            "valid": False,

            "message":
                "Audit record not found."
        }


    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        record = json.load(f)


    original_hash = record["hash"]

    report = record["report"]

    recalculated_hash = generate_hash(
        report
    )


    return {

        "valid":
            original_hash ==
            recalculated_hash,

        "stored_hash":
            original_hash,

        "calculated_hash":
            recalculated_hash
    }


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )