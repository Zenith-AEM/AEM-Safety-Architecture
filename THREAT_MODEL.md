# Threat Model & Security Posture

> **Historical architecture threat sketch (January 2026).** The mitigations below are design intentions, not proof that a privileged host attacker cannot bypass the current prototype or alter its ledger. See the [current status](README.md) and [bounded QEMU milestone](QEMU_MILESTONE_2026_11.md).


The AEM architecture assumes a Zero-Trust posture regarding the "Normal World" (Host OS). The system is designed to mitigate the following specific threat vectors:

## A. Stochastic Command Failure (AI Safety)

**The Threat:** A "Mission AI" trained on high-entropy data (e.g., SYNTHIA) enters an edge-case state and issues a command that is logically sound but physically hazardous.

**AEM Mitigation:** The Structural Veto intercepts the command string in the Secure World. If the string matches a restricted pattern in the IEL (e.g., `THROTTLE_100` in a geo-fenced zone), the signal is severed in 54.4 μs.

---

## B. OS-Level Kernel Compromise (Cybersecurity)

**The Threat:** An attacker gains root access to the Ubuntu Host OS and attempts to bypass software guardrails to exfiltrate data or hijack actuators.

**AEM Mitigation:** Because the AEM resides in ARM TrustZone, it is hardware-isolated from the Host OS. Even a full kernel compromise cannot modify the Immutable Exclusion List (IEL) or the Immutable Audit Ledger (IAL).

---

## C. Unauthorized Data State-Changes (Healthcare)

**The Threat:** A database management AI attempts an unauthorized bulk-export of synthetic patient records (e.g., Synthea datasets) to an external IP.

**AEM Mitigation:** The AEM treats the data-export command as a state-change request. The Foundational Control Plane (FCP) denies the request if it violates the structural integrity rules defined for patient privacy, logging the attempt as a high-priority event in the IAL.
