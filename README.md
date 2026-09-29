# NetComply — AI-Driven Multi-Vendor Network Security Compliance Auditor

> **Smart India Hackathon 2026 | SIH26155 | Blockchain & Cybersecurity**

NetComply is an AI-augmented, vendor-agnostic platform that analyzes network configurations, normalizes vendor-specific security settings, evaluates compliance, provides remediation guidance, and maintains a tamper-evident audit history.

---

## 1. Problem

Enterprise networks use heterogeneous devices such as **Cisco, Juniper, Fortinet and Palo Alto**. Different vendors and firmware versions use different configuration syntaxes, making manual auditing and vendor-specific compliance workflows difficult.

NetComply addresses:

- Manual and repetitive configuration auditing
- Vendor-specific compliance workflows
- Previously unseen configuration syntax
- Multi-framework compliance assessment
- Auditable and verifiable compliance records

---

## 2. Proposed Solution

NetComply provides:

- **Unified Configuration Ingestion** — supports single or bulk configuration files.
- **AI-Powered Normalization** — converts vendor-specific syntax into a common Security Baseline Model.
- **Multi-Framework Compliance** — evaluates CIS, NIST and STIG controls.
- **Adaptive AI Training** — unknown commands are interpreted and validated by administrators.
- **Blockchain Trust Layer** — stores hashes of configurations, reports, approved mappings and audit events for tamper-evident history.

---

## 3. AI / NLP

The prototype uses:

- TF-IDF vectorization
- N-gram features
- Logistic Regression
- Pattern matching
- Network configuration command dataset

The architecture can also integrate **Ollama and open-source LLMs** for complex or previously unseen commands.

Example:

```text
"enable ssh version 2"
        ↓
NLP Intent: ssh_version
        ↓
Parameter: ssh.version
        ↓
Value: 2
        ↓
Compliance Check
```

---

## 4. Compliance Engine

Configurations are converted into a common security model containing:

- SSH
- Telnet
- Authentication
- Logging
- NTP
- SNMP
- ACLs
- Cryptographic controls

The engine produces:

**PASS / FAIL / UNKNOWN + Severity + Evidence + Remediation**

Example:

```text
SSH Version 2        → PASS
Telnet Disabled      → FAIL
HTTP Management      → FAIL
Centralized Logging  → PASS
NTP                  → PASS
```

---

## 5. Human-in-the-Loop Learning

Unknown commands are processed through an administrator validation workflow:

```text
Unknown Command
      ↓
AI Interpretation
      ↓
Confidence Score
      ↓
Administrator Review
      ↓
Approve / Reject / Edit
      ↓
Reusable Mapping
```

Validated mappings can become reusable knowledge, allowing the system to adapt to previously unseen vendor syntax while keeping the administrator in control.

---

## 6. Blockchain Trust Layer

Blockchain is used as an **integrity and audit layer**, not for configuration parsing.

```text
Configuration / Report
        ↓
     SHA-256
        ↓
Hash + Audit Metadata
        ↓
Blockchain / Audit Ledger
```

The system can record hashes of:

- Configurations
- Compliance reports
- AI-approved mappings
- Administrator approvals
- Remediation events

Sensitive configuration data remains **off-chain**.

---

## 7. System Architecture

```text
React + Tailwind Frontend
          ↓
FastAPI Backend
          ↓
Configuration Parser
          ↓
AI / NLP Layer
          ↓
Security Baseline Model
          ↓
CIS / NIST / STIG Compliance
          ↓
Remediation + Audit Hash
          ↓
Blockchain Trust Layer
          ↓
Dashboard / PDF Reports
```

---

## 8. Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, Tailwind CSS, Lucide React |
| Backend | Python, FastAPI, Uvicorn |
| Parsing | Python, Regex, Pattern Matching, TextFSM |
| AI / NLP | Scikit-learn, TF-IDF, Logistic Regression, spaCy, Ollama |
| Database | SQLite / PostgreSQL |
| Integrity | SHA-256, Blockchain Frameworks |
| Reporting | ReportLab |
| Development | Git, GitHub, Docker |

---

## 9. Installation & Usage

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
python main.py
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Train NLP Model

```bash
cd backend/nlp
python train_nlp.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 10. Impact, Research Gap & Future Scope

### Impact

**Cybersecurity**
- Detects insecure configurations.
- Identifies deviations from security controls.
- Provides severity, evidence and remediation.

**AI-Driven Adaptability**
- Reduces dependency on manually written vendor-specific parsers.
- Interprets previously unseen configuration syntax.
- Learns from administrator feedback.

**Blockchain-Based Trust**
- Provides a tamper-evident compliance history.
- Enables audit traceability for approvals and remediation.

**Operational Efficiency**
- Automates repetitive audits.
- Supports bulk configuration analysis.
- Centralizes multi-vendor compliance monitoring.
- Generates structured reports.

### Target Users

- Network Administrators
- SOC Teams
- Cybersecurity Teams
- Compliance Auditors
- Enterprise IT Teams

### Research Gap

Existing research addresses **network configuration verification, policy extraction, LLM-based networking and blockchain audit protection** largely as separate areas.

NetComply combines these concepts into a single:

```text
AI + Cybersecurity + Human-in-the-Loop + Blockchain
```

compliance platform for previously unseen vendor configuration syntax.

### Future Scope

- More vendor and firmware support
- Advanced Ollama/LLM integration
- Larger NLP training dataset
- Netmiko/NAPALM/NETCONF integration
- Full permissioned blockchain integration
- Role-based access control
- Docker deployment
- Enterprise-scale bulk auditing

### Research References

- Birkner et al., *Config2Spec*, USENIX NSDI 2020
- Beckett et al., *A General Approach to Network Configuration Verification*, ACM SIGCOMM 2017
- Liu et al., *Large Language Models for Networking: Workflow, Advances and Challenges*, 2024
- *BlockAudit 2.0*, ISCON 2021
- Yaga et al., *NIST IR 8202: Blockchain Technology Overview*, NIST 2018
- CIS Benchmarks
- NIST SP 800-53 / SP 800-53A
- DISA STIGs

---

### NetComply

**One Compliance Engine. Multiple Vendors. Adaptive Security.**

**Built for Smart India Hackathon 2026 — SIH26155**
