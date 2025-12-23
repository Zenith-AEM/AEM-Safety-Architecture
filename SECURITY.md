# Security Policy

## Supported Versions
As the AEM/DMSA kernel is currently in a verified Python simulation environment (Transitioning to ARM TrustZone), we support security reporting for the following:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability
We take the safety and determinism of the AEM kernel seriously. If you discover a "Semantic Bypass," a "False Negative," or a method to circumvent the Foundational Control Plane (FCP), please report it to us immediately.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please email technical reports to: **[Your Professional Email Here]**

### Our Response Process
1. **Validation:** We will test the bypass against our 1,016 operational scenarios.
2. **CFV Loop:** We will utilize the Continuous Formal Verification protocol to analyze the execution trace.
3. **Amendment:** We will generate a hardware-locked amendment (ADD_TO_IEL) to close the gap at machine speed.
4. **Disclosure:** Once the amendment is verified, we will publicly update the repository.
