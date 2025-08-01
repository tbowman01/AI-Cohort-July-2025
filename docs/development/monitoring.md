---
layout: page
title: "Monitoring Setup"
parent: "Development"
permalink: /docs/development/monitoring/
---

# 📊 Monitoring Setup

Comprehensive monitoring and observability setup for AutoDevHub to ensure system reliability, performance tracking, and proactive issue detection.

## 🎯 Monitoring Overview

AutoDevHub implements a multi-layered monitoring approach:

- **Application Monitoring**: Performance metrics and business KPIs
- **Infrastructure Monitoring**: System resources and container health
- **Log Aggregation**: Centralized logging and analysis
- **Alerting**: Proactive notification system

## 📈 Application Metrics

### FastAPI Backend Metrics
```python
# backend/monitoring.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# Request metrics
REQUEST_COUNT = Counter(
    'autodevhub_requests_total',
    'Total app requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'autodevhub_request_duration_seconds',
    'Request latency',
    ['method', 'endpoint']
)

# Business metrics
STORY_GENERATION_COUNT = Counter(
    'autodevhub_stories_generated_total',
    'Total stories generated'
)

AI_API_CALLS = Counter(
    'autodevhub_ai_api_calls_total',
    'Total AI API calls',
    ['status']
)

ACTIVE_USERS = Gauge(
    'autodevhub_active_users',
    'Current active users'
)

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(time.time() - start_time)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### React Frontend Metrics
```javascript
// frontend/src/monitoring/metrics.js
class MetricsCollector {
  constructor() {
    this.metrics = {
      pageLoads: 0,
      apiCalls: 0,
      errors: 0,
      userActions: {}
    };
  }

  trackPageLoad(pageName) {
    this.metrics.pageLoads++;
    this.sendMetric('page_load', { page: pageName });
  }

  trackApiCall(endpoint, status, duration) {
    this.metrics.apiCalls++;
    this.sendMetric('api_call', {
      endpoint,
      status,
      duration
    });
  }

  trackError(error, context) {
    this.metrics.errors++;
    this.sendMetric('error', {
      message: error.message,
      stack: error.stack,
      context
    });
  }

  async sendMetric(type, data) {
    try {
      await fetch('/api/metrics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, data, timestamp: Date.now() })
      });
    } catch (error) {
      console.warn('Failed to send metric:', error);
    }
  }
}

export const metrics = new MetricsCollector();
```

## 🐳 Docker Monitoring

### Container Health Checks
```dockerfile
# Backend Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Frontend Dockerfile  
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:80/health || exit 1
```

### Docker Compose Monitoring
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'

volumes:
  prometheus_data:
  grafana_data:
```

## 📊 Prometheus Configuration

### Prometheus Config
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'autodevhub-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s

  - job_name: 'autodevhub-frontend'
    static_configs:
      - targets: ['frontend:80']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

### Alerting Rules
```yaml
# monitoring/rules/autodevhub.yml
groups:
  - name: autodevhub.rules
    rules:
      - alert: HighErrorRate
        expr: rate(autodevhub_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} requests per second"

      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(autodevhub_request_duration_seconds_bucket[5m])) > 0.5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is {{ $value }}s"

      - alert: ServiceDown
        expr: up{job="autodevhub-backend"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "AutoDevHub backend is down"
          description: "Backend service has been down for more than 5 minutes"
```

## 📈 Grafana Dashboards

### Main Application Dashboard
```json
{
  "dashboard": {
    "id": null,
    "title": "AutoDevHub Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(autodevhub_requests_total[5m])",
            "legendFormat": "{{ method }} {{ endpoint }}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(autodevhub_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(autodevhub_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(autodevhub_requests_total{status=~\"4..|5..\"}[5m])",
            "legendFormat": "Error rate"
          }
        ]
      },
      {
        "title": "Story Generation Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(autodevhub_stories_generated_total[1h])",
            "legendFormat": "Stories/hour"
          }
        ]
      }
    ]
  }
}
```

## 📝 Centralized Logging

### Log Configuration
```python
# backend/logging_config.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
            
        return json.dumps(log_entry)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/var/log/autodevhub/app.log')
    ]
)

# Set JSON formatter for structured logging
for handler in logging.root.handlers:
    handler.setFormatter(JSONFormatter())
```

### ELK Stack Integration
```yaml
# monitoring/docker-compose.elk.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.5.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.5.0
    ports:
      - "5044:5044"
    volumes:
      - ./monitoring/logstash/pipeline:/usr/share/logstash/pipeline
      - ./monitoring/logstash/config:/usr/share/logstash/config

  kibana:
    image: docker.elastic.co/kibana/kibana:8.5.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

volumes:
  elasticsearch_data:
```

## 🔔 Alerting Setup

### Alertmanager Configuration
```yaml
# monitoring/alertmanager.yml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'alerts@autodevhub.com'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'

receivers:
  - name: 'web.hook'
    email_configs:
      - to: 'devops@autodevhub.com'
        subject: 'AutoDevHub Alert: {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          {{ end }}
    
    slack_configs:
      - api_url: 'YOUR_SLACK_WEBHOOK_URL'
        channel: '#alerts'
        title: 'AutoDevHub Alert'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
```

## 🚀 Quick Setup Commands

### Start Monitoring Stack
```bash
# Start monitoring services
docker-compose -f docker-compose.monitoring.yml up -d

# Verify services
docker-compose -f docker-compose.monitoring.yml ps

# Access dashboards
echo "Prometheus: http://localhost:9090"
echo "Grafana: http://localhost:3001 (admin/admin)"
echo "Node Exporter: http://localhost:9100"
```

### Import Grafana Dashboard
```bash
# Import AutoDevHub dashboard
curl -X POST \
  http://admin:admin@localhost:3001/api/dashboards/db \
  -H 'Content-Type: application/json' \
  -d @monitoring/grafana/dashboards/autodevhub.json
```

## 📊 Key Metrics to Monitor

### Application Metrics
- **Request Rate**: Requests per second by endpoint
- **Response Time**: 50th, 95th, 99th percentiles
- **Error Rate**: 4xx and 5xx responses
- **Story Generation**: AI-powered story creation rate
- **User Sessions**: Active users and session duration

### Infrastructure Metrics
- **CPU Usage**: Container and host CPU utilization
- **Memory Usage**: Container memory consumption
- **Disk Usage**: Storage utilization and I/O
- **Network**: Ingress/egress traffic and latency

### Business Metrics
- **User Engagement**: Feature usage and adoption
- **AI Performance**: Claude API response times
- **Data Processing**: Document generation rates
- **System Health**: Service availability and uptime

## 🔗 Related Documentation

- **[Deployment Architecture](/docs/architecture/deployment-architecture/)**: Infrastructure setup
- **[Development Setup](/docs/development/setup-guide/)**: Local environment configuration
- **[System Overview](/docs/architecture/system-overview/)**: High-level architecture

---

*Comprehensive monitoring ensures AutoDevHub operates reliably and efficiently across all environments.*