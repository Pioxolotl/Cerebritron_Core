# Action Controller (AC) Documentation

## Overview

The Action Controller (AC) is responsible for executing actions based on decisions made by the Cognitive Core (CC). It translates high-level action plans into concrete commands for hardware devices, manages action scheduling, and collects feedback on action execution. The AC serves as the bridge between the system's cognitive functions and its physical interactions with the environment.

## Key Components

### Command Processor

The Command Processor interprets and executes commands from the Cognitive Core:

- **Command Parsing**: Parses command structures from the CC
- **Command Validation**: Validates commands for syntax and safety
- **Command Execution**: Executes commands through appropriate handlers
- **Command Monitoring**: Monitors command execution status

### Action Scheduler

The Action Scheduler manages the timing and sequencing of actions:

- **Action Queuing**: Queues actions for execution
- **Timing Control**: Manages execution timing for scheduled actions
- **Priority Management**: Handles action priorities and conflicts
- **Execution Monitoring**: Tracks execution status of scheduled actions

### Feedback Collector

The Feedback Collector gathers and processes feedback on action execution:

- **Success/Failure Detection**: Determines if actions succeeded or failed
- **Performance Metrics**: Collects metrics on action performance
- **User Feedback**: Processes explicit and implicit user feedback
- **Feedback Aggregation**: Combines feedback from multiple sources

### Handlers

The AC includes various handlers for different types of actions:

#### Text-to-Speech Handler
- Converts text to speech for audio output
- Supports multiple voices and languages
- Configurable for different speech characteristics
- Manages audio output through the HAL

#### Telegram Handler
- Sends messages through Telegram
- Receives messages from Telegram
- Manages Telegram bot interactions
- Supports various message formats

## Communication Patterns

The AC communicates with other layers through:

- **Message Queue**: For asynchronous communication
- **REST API**: For configuration, command submission, and management
- **Direct Function Calls**: For synchronous operations within the same process

## Service Architecture

The AC is implemented as a standalone service with:

- **REST API**: For external communication
- **Configuration Management**: For action settings
- **Health Monitoring**: For service health checks
- **Logging**: For diagnostic information

## Implementation Details

### Action Processing Pipeline

The AC implements a flexible action processing pipeline:

1. **Action Reception**: Actions are received from CC or external sources
2. **Action Validation**: Actions are validated for safety and feasibility
3. **Handler Selection**: Appropriate handlers are selected for the action
4. **Action Execution**: The action is executed through selected handlers
5. **Feedback Collection**: Feedback is collected on action execution
6. **Result Reporting**: Results are reported back to the CC

### Action Scheduling

The AC implements sophisticated action scheduling:

- **Immediate Execution**: For actions that need to be executed immediately
- **Delayed Execution**: For actions that need to be executed at a specific time
- **Periodic Execution**: For actions that need to be executed periodically
- **Conditional Execution**: For actions that depend on specific conditions

### Error Handling

The AC implements robust error handling:

- **Command Errors**: Handled at the command level
- **Execution Errors**: Handled at the execution level
- **Handler Errors**: Handled at the handler level
- **Service Errors**: Handled at the service level

## Usage Examples

### Initializing the AC Service

```python
# This is a simplified example
service = AcService(config_path, master_password)
if service.initialize():
    service.run()
```

### Scheduling an Action

```python
# This is a simplified example
result = action_manager.schedule_action(
    time=time.time() + 60,  # Execute in 60 seconds
    id="action_123",
    action={
        "type": "speech",
        "text": "Reminder: Your meeting starts in 5 minutes."
    }
)
# Handle result
```

### Converting Text to Speech

```python
# This is a simplified example
result = action_manager.text_to_speech(
    "Hello, how can I help you today?"
)
# Handle result
```

### Sending a Notification

```python
# This is a simplified example
result = action_manager.send_notification(
    "Your laundry is done."
)
# Handle result
```

## Configuration

The AC can be configured through:

- **Environment Variables**: For service configuration
- **Configuration Files**: For handler configuration
- **API**: For runtime configuration

### Configuration Options

- **Handlers**: Configuration for action handlers
  - Text-to-Speech settings
  - Telegram bot settings
  - Other handler-specific settings
  
- **Delivery Preferences**: Settings for action delivery
  - Speech output preferences
  - Notification preferences
  - Other delivery channel preferences
  
- **Scheduling**: Settings for action scheduling
  - Default timing parameters
  - Priority settings
  - Conflict resolution strategies

## Deployment

The AC is deployed as a Docker container with:

- **Exposed API**: For external communication
- **Volume Mounts**: For configuration and data
- **Resource Limits**: For CPU and memory management

## Extending the AC

The AC can be extended by:

1. **Creating New Handlers**: Implementing handlers for new action types
2. **Enhancing Scheduling**: Improving scheduling algorithms and capabilities
3. **Adding Feedback Mechanisms**: Implementing new feedback collection methods
4. **Integrating External Services**: Connecting to external action execution services
