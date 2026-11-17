# Agnostic Equalization Mechanism (AEM)

AEM is a research architecture for deciding whether an autonomous controller's request may reach a defined effect. Its decision logic is intended to run outside the requester’s operating system. In the current QEMU test, fixed requests pass through a Gateway Authority to an OP-TEE trusted application in an **emulated Arm TrustZone secure world**. That application applies an exclusion list, an exact action vocabulary, an immediate risk check (FCP) and a five-step forward check (TFP), in that order. It keeps decision state and a ledger through OP-TEE storage.

AEM could be integrated into a new system or deployed as a separate pass-through unit. Either form must eventually make the controlled output inaccessible to the requester without a permit. The current QEMU client writes a marker after a permit; the client itself controls that marker, so this run does not prove protected output enforcement.

Read [what remains the same and what has changed](AEM_PRINCIPLES_AND_STATUS.md) for a plain-language account of the project.

## Current evidence (November 2026)

The latest public milestone is a [two-boot QEMU decision and evidence test](QEMU_MILESTONE_2026_11.md). Nine fixed requests went through a Gateway Authority and child trusted application. Five permits produced five markers on a separate QEMU effect capture; the four vetoes produced none. A controlled restart preserved the readback state, and the final ledger and effect capture pass the published offline checker.

The [small replay packet](QEMU_MILESTONE_2026_11.md#replay-the-public-subset) contains the exact final ledger and effect bytes, checker source, its model and fixtures. The full run packet, including firmware images, disk snapshots, console logs and build inputs, is retained locally and is **not** included here. This public subset supports inspection of the captured decision and effect sequence; it cannot independently establish everything that ran in QEMU.

### What this run does not show

- **Production trust:** The signing material and demo HMAC key are development fixtures. QEMU emulates the secure world; it does not demonstrate physical isolation.
- **Protected output:** The effect is a client marker, not a physical actuator. Privileged normal-world code could bypass the marker path.
- **Rollback or crash durability:** The controlled restart shows state readback in this run. It does not prove rollback resistance or general crash durability; privileged code could also interfere with the storage backing.
- **Independent implementation audit:** The public replay subset omits the trusted-application and Authority source. It checks the captured scenario, but cannot independently audit the secure-world implementation or establish hardware safety.

## Where this is going

The QEMU run is a software baseline. The next proof work is to establish resistant state and evidence storage, and an output path the requester cannot drive without a permit. Board B's RPMB work is one research route for the storage question; it has not established safe target use or rollback resistance. A bench sidecar controlling one harmless load is a possible test configuration for output enforcement. An integrated design would have to prove the same boundary. Product hardware and deployment form have not been selected.

## Earlier work and documents

The January 2026 [Pi 3 HIL validation page](AEM_TRL4_Validation_Data.md) and [benchmark page](BENCHMARKS.md) report self-conducted measurements from an earlier configuration. Their TRL, latency and security claims should be read in that dated context. They are not validation of the current QEMU path or the proposed sidecar. The [executive summary](EXECUTIVE_SUMMARY.md), [technical synopsis](TECHNICAL_SYNOPSIS.md) and [threat model](THREAT_MODEL.md) also contain architecture goals and earlier claims; this README and the QEMU milestone state the current demonstrated boundary.

The archived [technical volume](Zenith_HR0011SB20254XL-01_TechVolume.pdf) is an older proposal artifact; any patent or readiness language in it is historical and is not a current status claim. The [license](LICENSE.md) sets the terms for this repository. Research questions and technical scrutiny are welcome through GitHub issues.

© 2026 Zenith Structural Holdings LLC.
