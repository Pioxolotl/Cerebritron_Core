# Perception System (PS) Documentation

## Overview

The Perception System (PS) processes raw data from sensors into semantic representations that can be used by the Cognitive Core. It acts as a bridge between the physical world (via HAL) and the cognitive functions of the system, transforming low-level sensor data into meaningful information.

## Key Components

### Perception Manager

The Perception Manager serves as the central component of the PS:

- **Data Processing**: Coordinates the processing of sensor data through various processors
- **Processor Registration**: Manages the registration and configuration of data processors
- **Data Routing**: Routes processed data to appropriate consumers
- **State Management**: Maintains the state of perception processes

### Processors

The PS includes various processors for different types of sensor data:

#### Speech-to-Text Processor
- Converts audio data from microphones into text
- Supports multiple languages and accents
- Configurable for different environments and noise levels
- Provides confidence scores for transcriptions

#### Keyword Detector
- Detects specific keywords in audio streams
- Configurable keyword lists and sensitivity
- Provides timestamps for detected keywords
- Supports wake word detection for system activation

### Database

The PS includes a database component for storing and retrieving perception data:

- **Speech Database**: Stores speech recognition results
  - Maintains history of recognized speech
  - Supports querying by time, content, and metadata
  - Provides data for training and improvement

### Models

The PS defines data models for different types of perceptual information:

- **Speech Model**: Represents recognized speech
  - Text content
  - Confidence scores
  - Speaker identification (when available)
  - Timestamps
  - Metadata (device, environment, etc.)

## Event Types

The PS processes and generates various types of events:

- **Audio Events**: Events from audio processing
  - Speech recognition results
  - Keyword detection
  - Audio classification

- **System Events**: Internal system events
  - Processor status changes
  - Configuration updates
  - Error conditions

## Communication Patterns

The PS communicates with other layers through:

- **Message Queue**: For asynchronous communication of perception events
- **REST API**: For configuration, querying, and management
- **Direct Function Calls**: For synchronous operations within the same process

## Service Architecture

The PS is implemented as a standalone service with:

- **REST API**: For external communication
- **Configuration Management**: For processor settings
- **Health Monitoring**: For service health checks
- **Logging**: For diagnostic information

## Implementation Details

### Data Processing Pipeline

The PS implements a flexible data processing pipeline:

1. **Data Reception**: Raw sensor data is received from HAL
2. **Preprocessing**: Data is preprocessed for specific processors
3. **Processing**: Data is processed by registered processors
4. **Postprocessing**: Results are formatted and enriched
5. **Distribution**: Processed data is distributed to consumers

### Processor Registration

Processors can be registered with the PS in several ways:

1. **Static Configuration**: Processors defined in configuration files
2. **Dynamic Registration**: Processors registered at runtime
3. **Auto-discovery**: Processors discovered based on available data types

### Error Handling

The PS implements robust error handling:

- **Processor Errors**: Handled at the processor level
- **Pipeline Errors**: Handled at the pipeline level
- **Service Errors**: Handled at the service level

## Usage Examples

### Initializing the PS Service

```python
# This is a simplified example
service = PsService(config_path, master_password)
if service.initialize():
    service.run()
```

### Registering a Processor

```python
# This is a simplified example
processor = SpeechToTextProcessor(
    id="stt_1",
    name="Speech to Text",
    config={"model": "default", "language": "en-US"}
)
perception_manager.register_processor(processor)
```

### Processing Sensor Data

```python
# This is a simplified example
result = perception_manager.process_data({
    "source": "hal",
    "sensor_id": "mic1",
    "data": audio_data
})
# Handle result
```

### Querying Speech Data

```python
# This is a simplified example
speech_data = perception_manager.get_speech_data(
    limit=100,
    offset=0
)
# Process speech data
```

## Configuration

The PS can be configured through:

- **Environment Variables**: For service configuration
- **Configuration Files**: For processor configuration
- **API**: For runtime configuration

### Configuration Options

- **Processors**: Configuration for individual processors
  - Speech-to-Text models and parameters
  - Keyword detection settings
  
- **Database**: Configuration for the perception database
  - Storage settings
  - Retention policies
  
- **Performance**: Settings affecting processing performance
  - Batch sizes
  - Threading options
  - Resource limits

## Deployment

The PS is deployed as a Docker container with:

- **Exposed API**: For external communication
- **Volume Mounts**: For configuration and data
- **Resource Limits**: For CPU and memory management

## Extending the PS

The PS can be extended by:

1. **Creating New Processors**: Implementing processor interfaces for new data types
2. **Enhancing Existing Processors**: Improving performance or capabilities
3. **Adding New Data Models**: Supporting new types of perceptual information
4. **Integrating External Services**: Connecting to external perception services
