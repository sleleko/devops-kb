import requests
import json
from datetime import datetime
import pytz
from typing import Dict, List, Optional, Union
import logging
from collections import defaultdict

class LokiLogger:
    def __init__(
        self, 
        loki_url: str,
        tenant_id: Optional[str] = None,
        timezone: str = 'Asia/Yekaterinburg'
    ):
        """
        Initialize Loki logger
        
        Args:
            loki_url: URL of Loki server (e.g. 'http://localhost:3100')
            tenant_id: Optional X-Scope-OrgID header for multi-tenant setups
            timezone: Timezone for timestamps
        """
        self.loki_url = f"{loki_url.rstrip('/')}/loki/api/v1/push"
        self.timezone = pytz.timezone(timezone)
        
        self.headers = {
            'Content-Type': 'application/json'
        }
        if tenant_id:
            self.headers['X-Scope-OrgID'] = tenant_id
        
    def _get_timestamp_ns(self) -> str:
        """Get current timestamp in nanoseconds as string"""
        return str(int(datetime.now(self.timezone).timestamp() * 1e9))
    
    def _format_stream_entry(
        self,
        message: str,
        timestamp: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> List[str]:
        """Format a single stream entry"""
        entry = [timestamp or self._get_timestamp_ns(), message]
        if metadata:
            entry.append(json.dumps(metadata))
        return entry

    def send_log(
        self, 
        message: str,
        labels: Dict[str, str],
        metadata: Optional[Dict[str, str]] = None,
        timestamp: Optional[str] = None
    ) -> requests.Response:
        """
        Send single log message to Loki
        
        Args:
            message: Log message
            labels: Dictionary of labels
            metadata: Optional metadata to attach to the log line
            timestamp: Optional timestamp in nanoseconds
            
        Returns:
            Response from Loki API
        """
        payload = {
            "streams": [
                {
                    "stream": labels,
                    "values": [
                        self._format_stream_entry(message, timestamp, metadata)
                    ]
                }
            ]
        }

        return self._send_payload(payload)

    def send_batch(
        self,
        entries: List[Dict[str, Union[str, Dict[str, str]]]],
        group_by_labels: bool = True
    ) -> requests.Response:
        """
        Send multiple log entries in a single request
        
        Args:
            entries: List of dictionaries with keys:
                - message: str (required)
                - labels: Dict[str, str] (required)
                - metadata: Dict[str, str] (optional)
                - timestamp: str (optional)
            group_by_labels: If True, groups entries with same labels into single stream
            
        Returns:
            Response from Loki API
        """
        if group_by_labels:
            # Group entries by labels
            streams = defaultdict(list)
            for entry in entries:
                labels = frozenset(entry['labels'].items())
                stream_entry = self._format_stream_entry(
                    entry['message'],
                    entry.get('timestamp'),
                    entry.get('metadata')
                )
                streams[labels].append(stream_entry)

            payload = {
                "streams": [
                    {
                        "stream": dict(labels),
                        "values": values
                    }
                    for labels, values in streams.items()
                ]
            }
        else:
            # Each entry becomes a separate stream
            payload = {
                "streams": [
                    {
                        "stream": entry['labels'],
                        "values": [
                            self._format_stream_entry(
                                entry['message'],
                                entry.get('timestamp'),
                                entry.get('metadata')
                            )
                        ]
                    }
                    for entry in entries
                ]
            }

        return self._send_payload(payload)

    def _send_payload(self, payload: Dict) -> requests.Response:
        """Send payload to Loki"""
        try:
            response = requests.post(
                self.loki_url,
                json=payload,
                headers=self.headers,
                timeout=5
            )
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send logs to Loki: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    # Initialize logger
    logger = LokiLogger(
        loki_url="http://localhost:3100",
        tenant_id="tenant1"
    )
    
    try:
        # Example 1: Simple batch of logs with different labels
        entries = [
            {
                "message": "User login successful",
                "labels": {
                    "job": "auth_service",
                    "environment": "production",
                    "level": "info"
                }
            },
            {
                "message": "Database query completed",
                "labels": {
                    "job": "db_service",
                    "environment": "production",
                    "level": "info"
                }
            }
        ]
        
        logger.send_batch(entries)
        
        # Example 2: Batch with metadata and custom timestamps
        entries_with_metadata = [
            {
                "message": "API request failed",
                "labels": {
                    "job": "api_service",
                    "level": "error"
                },
                "metadata": {
                    "trace_id": "0242ac120002",
                    "user_id": "12345"
                },
                "timestamp": "1645123456000000000"  # Optional custom timestamp
            },
            {
                "message": "Cache miss",
                "labels": {
                    "job": "api_service",
                    "level": "warn"
                },
                "metadata": {
                    "cache_key": "user:12345"
                }
            }
        ]
        
        # sending with groiups via labels (entries with equilent labels will be in one stream)
        logger.send_batch(entries_with_metadata, group_by_labels=True)
        
    except Exception as e:
        print(f"Error: {e}")
