# NetComply
## AI-Driven Multi-Vendor Network Security Compliance Auditor

> An AI-augmented, vendor-agnostic platform for analyzing network configurations, detecting security deviations, mapping configurations to compliance controls, and maintaining a tamper-evident audit trail.

---

## Smart India Hackathon 2026

| Field | Details |
|---|---|
| Problem Statement ID | SIH26155 |
| Problem Statement | AI-Driven Multi-Vendor Network Security Compliance Auditor |
| Theme | Blockchain & Cybersecurity |
| Category | Software |
| Team | Samyak |

---

# 1. Overview

Modern enterprise networks are built using heterogeneous infrastructure from multiple vendors such as Cisco, Juniper, Fortinet, and Palo Alto.

Although these devices may implement similar security controls, their configuration syntaxes differ significantly across vendors, platforms, and firmware versions.

This creates several challenges:

- Manual configuration auditing is time-consuming.
- Security teams need different parsers and workflows for different vendors.
- New or previously unseen configuration syntax can break static parsers.
- Compliance verification against CIS, NIST, and STIG controls requires normalization.
- Audit evidence and compliance reports need integrity and traceability.
- Configuration data may contain sensitive information and should not be stored directly on a blockchain.

**NetComply** addresses these challenges through a unified AI-assisted compliance platform.

The system accepts configurations from multiple network vendors, normalizes their security-related settings into a common Security Baseline Model, evaluates them against compliance controls, provides evidence and remediation guidance, and maintains a tamper-evident audit history.

---

# 2. Problem Statement

Enterprise networks commonly contain devices from multiple vendors.

For example:

```text
Cisco       → IOS / IOS-XE
Juniper     → Junos
Fortinet    → FortiOS
Palo Alto   → PAN-OS
