# Security Policy

## Supported Versions
As of **January 9, 2026**, the AEM kernel has transitioned to **Hardware-Isolated Execution (ARM TrustZone)**.

| Version | Status | Environment |
| :--- | :--- | :--- |
| **1.0.x (Current)** | ✅ Supported | **ARMv8 TrustZone (OP-TEE)** |
| **< 1.0** | ❌ Deprecated | Python Simulation |

---

## Reporting a Vulnerability
If you discover any of the following, please report it immediately:

* **Semantic Bypass:** Tricking the DPI into allowing forbidden strings.
* **Side-Channel Leakage:** Information escaping the Secure World.
* **TEE Escape:** Circumventing the Trusted Application (TA) logic.

**Please do not report security vulnerabilities through public GitHub issues.** Email technical reports to: **jamiebalousek@gmail.com**

---

## Our Response Process
1. **Validation:** Testing against our hardware-in-the-loop (HIL) suite.
2. **Formal Analysis:** Utilizing Continuous Formal Verification (CFV).
3. **Hardened Amendment:** Generating a hardware-locked update to the TA.
4. **Disclosure:** Updating the public repository once verified.
