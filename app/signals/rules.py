from dataclasses import dataclass, field


@dataclass
class SignalInputs:
    large_trade: bool = False
    whale_score: float = 0.0
    sports_specialist: bool = False
    position_increased: bool = False
    multiple_whales_agree: bool = False
    unusual_trade_size: bool = False
    extras: dict = field(default_factory=dict)


def compute_signal_score(inputs: SignalInputs) -> int:
    score = 0
    if inputs.large_trade:
        score += 25
    if inputs.whale_score >= 80:
        score += 20
    if inputs.sports_specialist:
        score += 15
    if inputs.position_increased:
        score += 10
    if inputs.multiple_whales_agree:
        score += 20
    if inputs.unusual_trade_size:
        score += 10
    return score
