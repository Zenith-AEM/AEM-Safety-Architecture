"""Pure reference model of the TFP algorithm in the supplied 2025 filing.

This module intentionally has no target, file, network, clock, or random I/O.
It models the disclosed five-state calculation; it is not production code and
does not assert patentability.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Sequence


HORIZON = 5
WEIGHTS = (
    Fraction(1, 2),
    Fraction(1, 4),
    Fraction(1, 8),
    Fraction(1, 16),
    Fraction(1, 32),
)

FUTURE_VETO_FLAG = "FUTURE_VETO_FLAG"
TFP_PASS = "TFP_PASS"


class InvalidModelInput(ValueError):
    """Raised when the deterministic transition input is malformed."""


@dataclass(frozen=True)
class ProjectedState:
    risk: Fraction
    violates_invariant: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.risk, Fraction):
            raise InvalidModelInput("RISK_NOT_FRACTION")
        if self.risk < 0:
            raise InvalidModelInput("NEGATIVE_RISK")
        if type(self.violates_invariant) is not bool:
            raise InvalidModelInput("VIOLATION_NOT_BOOL")


@dataclass(frozen=True)
class TFPResult:
    decision: str
    reason: str
    future_risk: Fraction
    evaluated_steps: int
    projected_risks: tuple[Fraction, ...]


Transition = Callable[[str, Fraction, int], ProjectedState]


def check_temporal_foresight(
    action: str,
    current_risk: Fraction,
    safety_tolerance_threshold: Fraction,
    transition: Transition,
) -> TFPResult:
    """Execute the filed five-state deterministic TFP calculation.

    Each step receives the proposed action, the previous projected risk, and a
    one-based step index. A projected invariant violation vetoes immediately.
    Otherwise, all five risks are combined using the filed fixed weights and
    compared with the FCP safety-tolerance threshold.
    """

    if not isinstance(action, str) or not action:
        raise InvalidModelInput("ACTION")
    if not isinstance(current_risk, Fraction) or current_risk < 0:
        raise InvalidModelInput("CURRENT_RISK")
    if (
        not isinstance(safety_tolerance_threshold, Fraction)
        or safety_tolerance_threshold < 0
    ):
        raise InvalidModelInput("THRESHOLD")
    if not callable(transition):
        raise InvalidModelInput("TRANSITION")

    projected_risk = current_risk
    future_risk = Fraction(0)
    observed: list[Fraction] = []

    for step, weight in enumerate(WEIGHTS, start=1):
        state = transition(action, projected_risk, step)
        if not isinstance(state, ProjectedState):
            raise InvalidModelInput("TRANSITION_RESULT")
        projected_risk = state.risk
        observed.append(projected_risk)
        future_risk += projected_risk * weight

        if state.violates_invariant:
            return TFPResult(
                FUTURE_VETO_FLAG,
                "PROJECTED_INVARIANT_VIOLATION",
                future_risk,
                step,
                tuple(observed),
            )

    if future_risk > safety_tolerance_threshold:
        return TFPResult(
            FUTURE_VETO_FLAG,
            "FUTURE_RISK_THRESHOLD",
            future_risk,
            HORIZON,
            tuple(observed),
        )

    return TFPResult(
        TFP_PASS,
        "WITHIN_TOLERANCE",
        future_risk,
        HORIZON,
        tuple(observed),
    )


def sequence_transition(states: Sequence[ProjectedState]) -> Transition:
    """Create a deterministic transition fixture with exactly five states."""

    frozen = tuple(states)
    if len(frozen) != HORIZON:
        raise InvalidModelInput("SEQUENCE_LENGTH")
    for state in frozen:
        if not isinstance(state, ProjectedState):
            raise InvalidModelInput("SEQUENCE_STATE")

    def transition(_action: str, _prior: Fraction, step: int) -> ProjectedState:
        if step < 1 or step > HORIZON:
            raise InvalidModelInput("STEP")
        return frozen[step - 1]

    return transition
