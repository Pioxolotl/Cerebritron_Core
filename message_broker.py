"""
Message Broker module for the Core functionality.

This module provides publish-subscribe messaging between components.
"""

import threading
import time
import json
import re
from typing import Any, Dict, Optional, Set, Callable, Pattern

import zmq

from .logging import setup_logging


class MessageBroker:
    """Provides publish-subscribe messaging between components."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 5555):
        """Initialize the message broker.
        
        Args:
            host: Host to bind to
            port: Port to bind to
        """
        self._host = host
        self._port = port
        self._context = None
        self._socket = None
        self._subscribers = {}
        self._subscriber_thread = None
        self._stop_subscriber = threading.Event()
        self._lock = threading.RLock()
        self._initialized = False
        self._logger = setup_logging(__name__)
    
    def initialize(self) -> bool:
        """Initialize the message broker.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        with self._lock:
            if self._initialized:
                return True
            
            try:
                self._logger.info("Initializing message broker")
                
                # Initialize ZeroMQ context
                self._context = zmq.Context()
                
                # Create publisher socket
                self._socket = self._context.socket(zmq.PUB)
                self._socket.bind(f"tcp://{self._host}:{self._port}")
                
                # Start subscriber thread
                self._stop_subscriber.clear()
                self._subscriber_thread = threading.Thread(
                    target=self._subscriber_loop,
                    daemon=True,
                    name="message-broker"
                )
                self._subscriber_thread.start()
                
                self._initialized = True
                self._logger.info("Message broker initialized successfully")
                return True
            except Exception as e:
                self._logger.error(f"Error initializing message broker: {e}")
                return False
    
    def shutdown(self) -> bool:
        """Shutdown the message broker.
        
        Returns:
            True if shutdown was successful, False otherwise
        """
        with self._lock:
            if not self._initialized:
                return True
            
            try:
                self._logger.info("Shutting down message broker")
                
                # Stop subscriber thread
                self._stop_subscriber.set()
                if self._subscriber_thread:
                    self._subscriber_thread.join(timeout=5.0)
                    self._subscriber_thread = None
                
                # Close socket
                if self._socket:
                    self._socket.close()
                    self._socket = None
                
                # Terminate context
                if self._context:
                    self._context.term()
                    self._context = None
                
                self._initialized = False
                self._logger.info("Message broker shutdown successfully")
                return True
            except Exception as e:
                self._logger.error(f"Error shutting down message broker: {e}")
                return False
    
    def publish(self, topic: str, message: Dict[str, Any]) -> bool:
        """Publish a message to a topic.
        
        Args:
            topic: Topic to publish to
            message: Message to publish
            
        Returns:
            True if publishing was successful, False otherwise
        """
        if not self._initialized:
            self._logger.error("Message broker not initialized")
            return False
        
        try:
            # Add topic to message
            message["_topic"] = topic
            
            # Convert message to JSON
            message_json = json.dumps(message)
            
            # Publish message
            self._socket.send_multipart([topic.encode(), message_json.encode()])
            
            return True
        except Exception as e:
            self._logger.error(f"Error publishing message: {e}")
            return False
    
    def subscribe(self, topic_pattern: str, callback: Callable[[Dict[str, Any]], None]) -> bool:
        """Subscribe to messages matching a topic pattern.
        
        Args:
            topic_pattern: Pattern to match topics against (supports wildcards with +)
            callback: Function to call when a message is received
            
        Returns:
            True if subscription was successful, False otherwise
        """
        with self._lock:
            try:
                # Convert pattern to regex
                regex_pattern = topic_pattern.replace("+", "[^.]+")
                regex = re.compile(f"^{regex_pattern}$")
                
                # Add subscriber
                if topic_pattern not in self._subscribers:
                    self._subscribers[topic_pattern] = {
                        "regex": regex,
                        "callbacks": set()
                    }
                
                self._subscribers[topic_pattern]["callbacks"].add(callback)
                
                self._logger.info(f"Subscribed to topic pattern: {topic_pattern}")
                return True
            except Exception as e:
                self._logger.error(f"Error subscribing to topic pattern: {e}")
                return False
    
    def unsubscribe(self, topic_pattern: str, callback: Optional[Callable[[Dict[str, Any]], None]] = None) -> bool:
        """Unsubscribe from messages matching a topic pattern.
        
        Args:
            topic_pattern: Pattern to match topics against
            callback: Function to unsubscribe (optional, if None, unsubscribe all callbacks)
            
        Returns:
            True if unsubscription was successful, False otherwise
        """
        with self._lock:
            try:
                # Check if pattern exists
                if topic_pattern not in self._subscribers:
                    return True
                
                # Remove callback or all callbacks
                if callback:
                    self._subscribers[topic_pattern]["callbacks"].discard(callback)
                    
                    # Remove pattern if no callbacks left
                    if not self._subscribers[topic_pattern]["callbacks"]:
                        del self._subscribers[topic_pattern]
                else:
                    del self._subscribers[topic_pattern]
                
                self._logger.info(f"Unsubscribed from topic pattern: {topic_pattern}")
                return True
            except Exception as e:
                self._logger.error(f"Error unsubscribing from topic pattern: {e}")
                return False
    
    def _subscriber_loop(self) -> None:
        """Receive and dispatch messages."""
        self._logger.info("Starting subscriber loop")
        
        # Create subscriber socket
        subscriber = self._context.socket(zmq.SUB)
        subscriber.connect(f"tcp://{self._host}:{self._port}")
        subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
        
        # Set up poller
        poller = zmq.Poller()
        poller.register(subscriber, zmq.POLLIN)
        
        while not self._stop_subscriber.is_set():
            try:
                # Poll for messages with timeout
                socks = dict(poller.poll(timeout=100))
                
                if subscriber in socks and socks[subscriber] == zmq.POLLIN:
                    # Receive message
                    topic, message_json = subscriber.recv_multipart()
                    topic = topic.decode()
                    
                    # Parse message
                    message = json.loads(message_json.decode())
                    
                    # Dispatch message
                    self._dispatch_message(topic, message)
            except Exception as e:
                self._logger.error(f"Error in subscriber loop: {e}")
                # Sleep for a bit before retrying
                time.sleep(0.1)
        
        # Clean up
        subscriber.close()
        
        self._logger.info("Subscriber loop stopped")
    
    def _dispatch_message(self, topic: str, message: Dict[str, Any]) -> None:
        """Dispatch a message to subscribers.
        
        Args:
            topic: Topic of the message
            message: Message to dispatch
        """
        with self._lock:
            # Find matching patterns
            for pattern, subscriber in self._subscribers.items():
                regex = subscriber["regex"]
                
                if regex.match(topic):
                    # Call callbacks
                    for callback in list(subscriber["callbacks"]):
                        try:
                            callback(message)
                        except Exception as e:
                            self._logger.error(f"Error in subscriber callback: {e}")
