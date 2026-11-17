# What remains the same in AEM

**Short answer:** This is still the same AEM idea, developed into a more precise and testable prototype. The goal remains a separate gate between a controller's request and a defined effect.

## The enduring principles

| Principle | Meaning | Where we are now |
| --- | --- | --- |
| A separate decision | The controller proposes an action; AEM decides whether that exact request may reach the effect path. | The QEMU client sends fixed requests through a Gateway Authority and child trusted application. A physical sidecar path has not been built. |
| Veto before effect | A denied or malformed request must not activate the controlled output. A missing answer is not permission. | The nine-request QEMU run produced five effect markers for five permits and none for four vetoes. The marker is a virtual client output, not an actuator. |
| Constrained authority | The requester should not be able to rewrite the rule or bypass the gate. | The QEMU decision sequence tests ordering and some failure cases. It does not prove resistance to a privileged attacker, a protected physical output, or a production trust root. |
| Inspectable evidence | A reviewer should be able to trace a request to its decision and observed effect, including after interruption. | The QEMU run retained a ledger and separate effect capture. The exact public bytes pass an offline checker after a controlled restart. General power-loss durability and independent provenance remain open. |

## What became more precise

The early public pages described the intended architecture in broad terms, including an immutable exclusion list, hardware isolation, predictive foresight and a physically severed signal. Those are goals or earlier configuration claims. The current QEMU demonstration makes a narrower, checkable statement.

The TFP forward check in this demo repeats one proposed action over five modeled steps. Its rule and threshold are fixed and published. It is not a general prediction of what an autonomous system will do. The ledger is inspectable in this run; it is not yet proven immutable against a privileged attacker. The separate effect capture proves what this QEMU client recorded, not what a physical actuator did.

## The next proof

A stable sidecar prototype would route one harmless physical action through a separate AEM unit and measure the effect with an independent instrument. It must show permit, veto, malformed input, interruption, restart and replay under a frozen test plan. A qualified reviewer should be able to inspect the raw results and the ways the test could have failed.

That is the same safety proposition made concrete. [Read the current QEMU milestone](QEMU_MILESTONE_2026_11.md) for the tested software result and its limits.

## Intellectual-property status

AEM is not being presented as patent pending. The project is not currently pursuing patent protection. Earlier references to an application number were part of historical materials and do not describe the present project status. This page does not determine the legal status of any past filing or change the repository's [license terms](LICENSE.md).
