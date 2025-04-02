# Core Documentation

## Overview

The Core module provides shared functionality and utilities used across all layers of the Cerebritron system. It includes components for communication, configuration management, logging, security, and health monitoring. The Core module serves as the foundation upon which all other layers are built.

## Key Components

### Communication

The Communication component facilitates message exchange between different layers and services:

- **Message Broker**: Provides a unified interface for message passing
  - Supports publish-subscribe pattern
  - Handles message routing and delivery
  - Ensures reliable message delivery
  - Supports different message priorities

- **Message Formats**: Defines standard message formats
  - JSON-based message structure
  - Schema validation for messages
  - Versioning support for backward compatibility

- **Communication Patterns**: Implements various communication patterns
  - Request-Response for synchronous operations
  - Publish-Subscribe for asynchronous notifications
  - Stream for continuous data flow

### Configuration Management

The Configuration component manages system and service configuration:

- **Configuration Storage**: Manages configuration data
  - File-based configuration
  - Environment variable integration
  - Secure storage for sensitive configuration

- **Configuration Access**: Provides interfaces for accessing configuration
  - Get/set operations for configuration values
  - Configuration validation
  - Default value handling

- **Dynamic Configuration**: Supports runtime configuration changes
  - Configuration update notifications
  - Configuration versioning
  - Configuration rollback

### Logging

The Logging component provides standardized logging across the system:

- **Log Levels**: Supports different log levels
  - DEBUG for detailed debugging information
  - INFO for general information
  - WARNING for potential issues
  - ERROR for error conditions
  - CRITICAL for critical failures

- **Log Formatting**: Standardizes log format
  - Timestamp
  - Log level
  - Service/component identifier
  - Message
  - Context information

- **Log Routing**: Directs logs to appropriate destinations
  - Console output
  - File output
  - Remote logging services

### Security

The Security component provides security features:

- **Authentication**: Verifies identity
  - API key authentication
  - Token-based authentication
  - Certificate-based authentication

- **Authorization**: Controls access
  - Role-based access control
  - Permission management
  - Access policy enforcement

- **Encryption**: Protects sensitive data
  - Data encryption at rest
  - Data encryption in transit
  - Key management

### Health Monitoring

The Health component provides health checking capabilities:

- **Health Checks**: Verifies service health
  - Liveness checks
  - Readiness checks
  - Dependency checks

- **Health Reporting**: Reports health status
  - Health status API
  - Health metrics
  - Health history

## Usage Examples

### Using the Message Broker

```python
# This is a simplified example
from core.communication import MessageBroker

# Create message broker
broker = MessageBroker()

# Subscribe to a topic
broker.subscribe("hal.sensor.data", handle_sensor_data)

# Publish a message
broker.publish("cc.command", {
    "type": "query",
    "text": "What's the weather like today?"
})
```

### Accessing Configuration

```python
# This is a simplified example
from core.config import ConfigManager

# Create config manager
config_manager = ConfigManager("/path/to/config")

# Get configuration value
database_url = config_manager.get_config("database.url", "default_url")

# Set configuration value
config_manager.set_config("logging.level", "INFO")
```

### Using the Logger

```python
# This is a simplified example
from core.logging import Logger

# Create logger
logger = Logger("my_service")

# Log messages
logger.debug("Detailed debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical failure")
```

### Using Security Features

```python
# This is a simplified example
from core.security import SecurityManager

# Create security manager
security_manager = SecurityManager("master_password")

# Encrypt data
encrypted_data = security_manager.encrypt("sensitive_data")

# Decrypt data
decrypted_data = security_manager.decrypt(encrypted_data)

# Verify authentication
is_authenticated = security_manager.verify_token(token)
```

### Performing Health Checks

```python
# This is a simplified example
from core.health import HealthChecker

# Create health checker
health_checker = HealthChecker()

# Register health check
health_checker.register_check("database", check_database_connection)

# Get health status
health_status = health_checker.check_health()
```

## Integration with Layers

The Core module is integrated with all layers of the Cerebritron system:

- **HAL**: Uses Core for configuration, communication, and logging
- **PS**: Uses Core for message passing, security, and health monitoring
- **CC**: Uses Core for configuration management and communication
- **AC**: Uses Core for logging, security, and message routing
- **SM**: Uses Core for health checking and configuration access

## Extending the Core

The Core module can be extended by:

1. **Adding New Communication Protocols**: Implementing new message transport mechanisms
2. **Enhancing Configuration**: Adding new configuration sources or formats
3. **Improving Logging**: Implementing new log destinations or formats
4. **Strengthening Security**: Adding new authentication or encryption methods
5. **Expanding Health Monitoring**: Implementing new health check types
