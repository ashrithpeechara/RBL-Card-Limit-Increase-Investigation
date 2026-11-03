# RBL Card Limit Increase – Android Malware Investigation

<p align="center">
  <img src="https://img.shields.io/badge/Investigation-Android%20Malware%20Analysis-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Analysis-Static-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Platform-Android-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Research-Digital%20Forensics-purple?style=for-the-badge" />
</p>

<p align="center">
  <b>Static Reverse Engineering | Android Security | Digital Forensics</b>
</p>

## Overview

This repository documents a static malware investigation of a suspicious Android application distributed under the name **RBL Card Limit Increase**.

The investigation focuses on understanding the application's internal architecture, identifying suspicious functionality, examining its embedded components, and tracing code paths associated with SMS operations, Firebase backend communication, call-forwarding functionality, and WebView-based interfaces.

Through Android reverse engineering and code-level examination, the investigation aims to document security-relevant capabilities and preserve technical findings in a structured, evidence-oriented format.

## Research Context

Financial-service-themed Android applications can use familiar branding and interfaces to create an appearance of legitimacy while implementing functionality that may expose users to security and privacy risks.

This investigation examines a suspicious application impersonating an RBL-related card-limit service to understand its implementation, backend integration, and potentially harmful capabilities.

The analysis is based on static examination of the available APK artifacts. Runtime behavior and real-world impact are not assumed unless independently verified.

## Application Information

| Attribute | Identified Value |
|---|---|
| Application name | RBL Card Limit Update |
| Original APK | `RBL CARD LIMIT UPDATE.apk` |
| Outer package | `com.rblcard_jagtd` |
| Inner package | `com.onnl.qapp.xtxr` |
| Analysis platform | Android |
| Investigation type | Static malware analysis |
| Firebase project identifier | `rbl-card-73-29-7-26` |

### Original APK SHA-256

`712ec1d0018c5e45e6472e585f6e989618567a4fdf059b753f221472c1d91056`

## Investigation Areas

### 1. APK Structure and Payload Analysis
- Examined the APK structure and application components.
- Investigated the embedded application architecture.
- Examined available payload and package artifacts.
- Recorded cryptographic hashes for artifact identification.

### 2. Android Manifest Analysis
- Examined application permissions.
- Identified services and broadcast receivers.
- Reviewed exported Android components.
- Investigated application-level security-relevant configurations.

### 3. SMS Functionality Analysis
- Examined SMS-related permissions and implementation.
- Traced available SMS handling code paths.
- Investigated remote SMS command functionality.
- Documented suspicious message-handling mechanisms.

### 4. Firebase Backend Analysis
- Identified Firebase project integration.
- Examined database references and application communication paths.
- Investigated backend-related functionality and data structures.

### 5. Call-Forwarding Analysis
- Investigated call-forwarding-related implementation.
- Examined relevant application code paths and configuration mechanisms.
- Documented potential remote-control functionality.

### 6. WebView Analysis
- Examined embedded WebView implementation.
- Investigated the banking-themed interface and associated endpoint.
- Reviewed application interaction with web-based components.

### 7. VPN Service Analysis
- Examined VPN-related application components and configuration.
- Investigated relevant permissions and service implementation.
- Documented findings and technical limitations.

## Methodology

The investigation follows a static-analysis workflow:

1. APK identification and cryptographic hashing.
2. Application structure inspection.
3. Android manifest examination.
4. Embedded payload and package analysis.
5. DEX-level reverse engineering.
6. SMS and call-forwarding code-flow investigation.
7. Firebase integration analysis.
8. WebView and VPN implementation examination.
9. IOC identification and documentation.
10. Technical reporting and evidence review.

## Repository Structure

```text
RBL-Card-Limit-Increase-Investigation/
│
├── README.md
│
├── analysis/
│   ├── apk-analysis.md
│   ├── manifest-analysis.md
│   ├── payload-analysis.md
│   ├── firebase-analysis.md
│   ├── sms-analysis.md
│   ├── call-forwarding-analysis.md
│   ├── webview-analysis.md
│   ├── vpn-analysis.md
│   └── installation-analysis.md
│
├── ioc/
│   └── indicators.csv
│
├── scripts/
│   ├── hash_verification.py
│   └── analysis-scripts.py
│
└── LICENSE
```

*The structure represents the planned documentation layout. Individual reports and scripts should be added only after their contents have been prepared and reviewed.*

## Tools and Technologies

- Kali Linux
- Python
- JADX
- Androguard
- Apktool
- AAPT2
- ADB
- SHA-256
- Android Reverse Engineering
- Static Malware Analysis

## Indicators of Compromise

The `ioc/` directory contains a structured register of relevant technical indicators identified during the investigation.

Indicators should be interpreted in context. Shared infrastructure, application identifiers, and API endpoints are not automatically malicious in isolation.

## Limitations

- This investigation focuses on static analysis.
- Runtime execution and successful malicious activity have not been established through this analysis.
- The presence of a code path does not independently establish that the functionality executed successfully.
- Firebase communication, SMS delivery, call forwarding, and other external actions require separate authorized validation.
- No claims about confirmed victim impact are made without supporting evidence.

## Evidence Handling

- Original evidence should be preserved separately from working copies.
- Cryptographic hashes should be retained for artifact identification.
- Sensitive evidence, credentials, tokens, personal information, and raw backend data must not be published.
- Public documentation should contain sanitized technical findings only.

## Disclaimer

This repository is intended for cybersecurity research, Android application security analysis, and digital forensics education.

All analysis should be performed on applications and artifacts obtained through authorized means. The findings documented here describe technical observations and do not establish attribution, successful execution, or real-world victim impact.

---

<p align="center">
  <b>Android Security | Malware Research | Digital Forensics</b>
</p>
