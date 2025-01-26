# Loki Logger

A Python client library for sending logs to Grafana Loki with support for batch operations, metadata, and multi-tenancy.

## Features

- Single and batch log sending
- Support for structured metadata
- Multi-tenant support via X-Scope-OrgID
- Automatic timestamp generation in nanoseconds
- Custom timestamp support
- Label-based log grouping for efficient storage
- Timezone awareness
- Error handling and retries

## Installation

```bash
pip install requests pytz
```

## Quick Start

```python
from loki_logger import LokiLogger

# Initialize the logger
logger = LokiLogger(
    loki_url="http://localhost:3100",
    tenant_id="tenant1"  # Optional
)

# Send a single log
logger.send_log(
    message="Application started",
    labels={
        "job": "app_service",
        "environment": "production"
    }
)
```

## Usage

### Single Log Entry

Send a single log entry with labels and optional metadata:

```python
logger.send_log(
    message="User authentication failed",
    labels={
        "job": "auth_service",
        "environment": "production",
        "level": "error"
    },
    metadata={
        "user_id": "12345",
        "trace_id": "0242ac120002"
    }
)
```

### Batch Operations

Send multiple logs in a single request:

```python
entries = [
    {
        "message": "API request received",
        "labels": {
            "job": "api_service",
            "level": "info"
        },
        "metadata": {
            "request_id": "req123"
        }
    },
    {
        "message": "Database query executed",
        "labels": {
            "job": "api_service",
            "level": "info"
        },
        "metadata": {
            "query_time_ms": "150"
        }
    }
]

# Send batch with grouping by labels (logs with same labels will be in one stream)
logger.send_batch(entries, group_by_labels=True)
```

### Custom Timestamps

You can specify custom timestamps for your logs:

```python
logger.send_log(
    message="Scheduled task completed",
    labels={"job": "scheduler"},
    timestamp="1645123456000000000"  # Unix timestamp in nanoseconds
)
```

### Batch with Mixed Content

Send a batch of logs with different labels, metadata, and timestamps:

```python
mixed_entries = [
    {
        "message": "Cache miss",
        "labels": {"service": "cache", "level": "warn"},
        "metadata": {"key": "user:12345"},
        "timestamp": "1645123456000000000"
    },
    {
        "message": "Payment processed",
        "labels": {"service": "payment", "level": "info"},
        "metadata": {"amount": "100.00", "currency": "USD"}
    }
]

logger.send_batch(mixed_entries)
```

## API Reference

### LokiLogger Class

#### Constructor

```python
LokiLogger(
    loki_url: str,
    tenant_id: Optional[str] = None,
    timezone: str = 'UTC'
)
```

Parameters:
- `loki_url`: Base URL of your Loki instance
- `tenant_id`: Optional tenant ID for multi-tenant setups
- `timezone`: Timezone for timestamp generation (default: 'UTC')

#### Methods

##### send_log

```python
send_log(
    message: str,
    labels: Dict[str, str],
    metadata: Optional[Dict[str, str]] = None,
    timestamp: Optional[str] = None
) -> requests.Response
```

Parameters:
- `message`: Log message string
- `labels`: Dictionary of log labels
- `metadata`: Optional metadata dictionary
- `timestamp`: Optional custom timestamp in nanoseconds

##### send_batch

```python
send_batch(
    entries: List[Dict[str, Union[str, Dict[str, str]]]],
    group_by_labels: bool = True
) -> requests.Response
```

Parameters:
- `entries`: List of log entry dictionaries
- `group_by_labels`: Whether to group entries by labels (default: True)

## Best Practices

1. **Label Management**:
   - Use consistent label names across your application
   - Keep the number of unique label combinations low
   - Avoid using high-cardinality values in labels

2. **Batch Processing**:
   - Use batch operations when sending multiple logs
   - Enable `group_by_labels` for efficient storage
   - Consider implementing a local buffer for batch processing

3. **Error Handling**:
   - Implement proper error handling around logger calls
   - Consider setting up retry mechanisms for failed requests
   - Monitor the logger's performance in production

4. **Metadata Usage**:
   - Use metadata for detailed information that shouldn't be indexed
   - Keep metadata size reasonable
   - Avoid putting sensitive information in metadata

## Error Handling

The logger includes built-in error handling:

```python
try:
    logger.send_log(
        message="Important operation",
        labels={"service": "critical_service"}
    )
except requests.exceptions.RequestException as e:
    # Handle network errors, timeouts, etc.
    print(f"Failed to send log: {e}")
```

## Performance Considerations

- Batch operations are more efficient than individual log sends
- Grouping by labels reduces storage overhead in Loki
- Consider implementing a local buffer for high-volume logging
- Use appropriate timeout values for your network conditions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
