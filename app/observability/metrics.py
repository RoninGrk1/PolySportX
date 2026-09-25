from prometheus_client import Counter, Gauge, Histogram

trades_processed = Counter("polysportx_trades_processed_total", "Trades processed")
markets_processed = Counter("polysportx_markets_processed_total", "Markets processed")
wallets_processed = Counter("polysportx_wallets_processed_total", "Wallets processed")
signals_generated = Counter("polysportx_signals_generated_total", "Signals generated")
alerts_sent = Counter("polysportx_alerts_sent_total", "Alerts sent")
alerts_failed = Counter("polysportx_alerts_failed_total", "Alerts failed")
api_errors = Counter("polysportx_api_errors_total", "Upstream API errors", ["source"])
processing_latency = Histogram(
    "polysportx_processing_latency_seconds",
    "Worker processing latency",
    ["worker"],
)
queue_depth = Gauge("polysportx_queue_depth", "Redis stream depth", ["stream"])
