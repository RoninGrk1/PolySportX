from app.observability.metrics import signals_generated
from app.signals.rules import SignalInputs, compute_signal_score
from app.signals.strength import label_for


class SignalEngine:
    def evaluate(self, inputs: SignalInputs) -> tuple[int, str]:
        score = compute_signal_score(inputs)
        strength = label_for(score)
        signals_generated.inc()
        return score, strength
