from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

def setup_tracing(app):
    """Configure OpenTelemetry with Jaeger exporter"""
    # Create a resource with service name
    resource = Resource.create({
        ResourceAttributes.SERVICE_NAME: "ecommerce-api"
    })
    
    # Set up the tracer with resource
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    
    # Configure the Jaeger exporter
    jaeger_exporter = JaegerExporter(
        # Use the collector endpoint instead of agent
        collector_endpoint='http://localhost:14268/api/traces',
        max_tag_value_length=4096
    )
    
    # Add SpanProcessor to the tracer
    provider.add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )
    
    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(
        app,
        excluded_urls="/metrics"
    )