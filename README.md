# Agnostic Equalization Mechanism (AEM)

AEM is a research effort to put a separate decision gate between an autonomous controller's request and a defined effect. The intended sidecar appliance would permit or veto the request before its output can act, then retain evidence a reviewer can inspect.

Read [what remains the same and what has changed](AEM_PRINCIPLES_AND_STATUS.md) for a plain-language account of the project.

## Current evidence (November 2026)

The latest public milestone is a [two-boot QEMU decision and evidence test](QEMU_MILESTONE_2026_11.md). Nine fixed requests went through a Gateway Authority and child trusted application. Five permits produced five markers on a separate QEMU effect capture; the four vetoes produced none. A controlled restart preserved the readback state, and the final ledger and effect capture pass the published offline checker.

The [small replay packet](QEMU_MILESTONE_2026_11.md#replay-the-public-subset) contains the exact final ledger and effect bytes, checker source, its model and fixtures. The full run packet, including firmware images, disk snapshots, console logs and build inputs, is retained locally and is **not** included here. This public subset supports inspection of the captured decision and effect sequence; it cannot independently establish everything that ran in QEMU.

This test uses development signing material and a public demo HMAC key. The effect is a client marker, not a physical actuator. It does not establish a production trust root, resistance to a privileged attacker, general crash durability or hardware safety.

## Where this is going

The next prototype target is a bench sidecar controlling one harmless physical load, with an independent effect measurement, repeatable permit and veto cases, fault tests, restart replay and a complete proof package. Product hardware has not been selected. The QEMU result is a software baseline for that work, not a completed sidecar.

## Earlier work and documents

The January 2026 [Pi 3 HIL validation page](AEM_TRL4_Validation_Data.md) and [benchmark page](BENCHMARKS.md) report self-conducted measurements from an earlier configuration. Their TRL, latency and security claims should be read in that dated context. They are not validation of the current QEMU path or the proposed sidecar. The [executive summary](EXECUTIVE_SUMMARY.md), [technical synopsis](TECHNICAL_SYNOPSIS.md) and [threat model](THREAT_MODEL.md) also contain architecture goals and earlier claims; this README and the QEMU milestone state the current demonstrated boundary.

The archived [technical volume](Zenith_HR0011SB20254XL-01_TechVolume.pdf) is an older proposal artifact; any patent or readiness language in it is historical and is not a current status claim. The [license](LICENSE.md) sets the terms for this repository. Research questions and technical scrutiny are welcome through GitHub issues.

© 2026 Zenith Structural Holdings LLC.
