from dataclasses import dataclass

from prometheus_fastapi_instrumentator import Instrumentator, metrics

from settings import settings

NAMESPACE = settings.prom_namespace
SUBSYSTEM = settings.prom_subsystem


@dataclass
class Prometheusmiddlewear:
    instrumentator: Instrumentator = Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=False,
        should_respect_env_var=False,
        should_instrument_requests_inprogress=False,
        excluded_handlers=[
            "/metrics",
            "/health",
            "/ready",
            "/status",
            "/",
            "/docs",
            "/redoc",
        ],
        env_var_name="ENABLE_METRICS",
        inprogress_name="fastapi_inprogress",
        inprogress_labels=True,
    )

    def __post_init__(self):
        self.instrumentator.add(
            metrics.request_size(
                should_include_handler=True,
                should_include_method=True,
                should_include_status=True,
                metric_namespace=NAMESPACE,
                metric_subsystem=SUBSYSTEM,
            )
        )

        self.instrumentator.add(
            metrics.response_size(
                should_include_handler=True,
                should_include_method=True,
                should_include_status=True,
                metric_namespace=NAMESPACE,
                metric_subsystem=SUBSYSTEM,
            )
        )
        self.instrumentator.add(
            metrics.latency(
                should_include_handler=True,
                should_include_method=True,
                should_include_status=True,
                metric_namespace=NAMESPACE,
                metric_subsystem=SUBSYSTEM,
            )
        )
        self.instrumentator.add(
            metrics.requests(
                should_include_handler=True,
                should_include_method=True,
                should_include_status=True,
                metric_namespace=NAMESPACE,
                metric_subsystem=SUBSYSTEM,
            )
        )

    def get_instrumentator(self):
        return self.instrumentator


instrumentator = Prometheusmiddlewear().get_instrumentator()
