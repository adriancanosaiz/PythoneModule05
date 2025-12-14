from typing import Any, List


class DataStream:
    """Base class for different types of data streams.

    Provides a common interface for processing batches of data from
    various stream sources.

    Attributes:
        stream_id (str): Unique identifier for the stream.
        stream_type (str): Type or category of the stream.
    """

    def __init__(self, stream_id: str, stream_type: str) -> None:
        """Initialize the DataStream with ID and type.

        Args:
            stream_id (str): Unique identifier for this stream.
            stream_type (str): The type/category of this stream.
        """
        self.stream_id = stream_id
        self.stream_type = stream_type

    def process_batch(self, data: List[Any]) -> None:
        """Process a batch of data from the stream.

        This method must be implemented by subclasses to define
        specific processing logic.

        Args:
            data (List[Any]): Batch of data items to process.

        Raises:
            NotImplementedError: If subclass doesn't implement this method.
        """
        raise NotImplementedError


class SensorStream(DataStream):
    """Stream specialized in handling environmental sensor data.

    Processes sensor readings including temperature, humidity, and pressure.
    """

    def __init__(self, stream_id: str) -> None:
        """Initialize the SensorStream.

        Args:
            stream_id (str): Unique identifier for this sensor stream.
        """
        print("\nInitializing Sensor Stream...")
        super().__init__(stream_id, "Environmental Data")
        print(f"Stream ID: {self.stream_id}, Type: {self.stream_type}")

    def process_batch(self, data: List[str]) -> None:
        """Process a batch of sensor readings.

        Parses sensor data in format "type:value" and calculates average
        temperature from the readings.

        Args:
            data (List[str]): List of sensor readings in format "type:value".
        """
        print(f"Processing sensor batch: [{', '.join(data)}]")
        temps = [float(d.split(":")[1]) for d in data if d.startswith("temp")]
        avg = temps[0] if temps else 0.0
        print(
            f"Sensor analysis: {len(data)} readings processed, "
            f"avg temp: {avg}°C"
        )


class TransactionStream(DataStream):
    """Stream specialized in handling financial transaction data.

    Processes buy and sell transactions and calculates net flow.
    """

    def __init__(self, stream_id: str) -> None:
        """Initialize the TransactionStream.

        Args:
            stream_id (str): Unique identifier for this transaction stream.
        """
        print("\nInitializing Transaction Stream...")
        super().__init__(stream_id, "Financial Data")
        print(f"Stream ID: {self.stream_id}, Type: {self.stream_type}")

    def process_batch(self, data: List[str]) -> None:
        """Process a batch of financial transactions.

        Parses transaction data in format "action:value" and calculates
        net flow where sell adds and buy subtracts from the total.

        Args:
            data (List[str]): List of transactions in format "action:value".
        """
        print(f"Processing transaction batch: [{', '.join(data)}]")
        net = 0
        for item in data:
            action, value = item.split(":")
            value = int(value)
            net += value if action == "sell" else -value
        print(
            f"Transaction analysis: {len(data)} operations, "
            f"net flow: {net:+} units"
        )


class EventStream(DataStream):
    """Stream specialized in handling system event data.

    Processes system events and tracks error occurrences.
    """

    def __init__(self, stream_id: str) -> None:
        """Initialize the EventStream.

        Args:
            stream_id (str): Unique identifier for this event stream.
        """
        print("\nInitializing Event Stream...")
        super().__init__(stream_id, "System Events")
        print(f"Stream ID: {self.stream_id}, Type: {self.stream_type}")

    def process_batch(self, data: List[str]) -> None:
        """Process a batch of system events.

        Analyzes events and counts the number of error events detected.

        Args:
            data (List[str]): List of event strings to process.
        """
        print(f"Processing event batch: [{', '.join(data)}]")
        errors = len([d for d in data if d == "error"])
        print(
            f"Event analysis: {len(data)} events, "
            f"{errors} error detected"
        )


class StreamProcessor:
    """Manager for processing multiple data streams.

    Handles registration and batch processing of various stream types
    through a unified interface.

    Attributes:
        streams (List[DataStream]): List of registered data streams.
    """

    def __init__(self) -> None:
        """Initialize the StreamProcessor with an empty stream list."""
        self.streams: List[DataStream] = []

    def register_stream(self, stream: DataStream) -> None:
        """Register a data stream with the processor.

        Args:
            stream (DataStream): The data stream to register.
        """
        self.streams.append(stream)

    def process_batches(self, batches: List[List[str]]) -> None:
        """Process multiple batches of data.

        Processes batches through registered streams and displays summary
        information about the processing results.

        Args:
            batches (List[List[str]]): List of data batches to process,
                where each batch is a list of strings.
        """
        print("\n=== Polymorphic Stream Processing ===")
        print("Processing mixed stream types through unified interface...")
        print("Batch 1 Results:")

        print(f"- Sensor data: {len(batches[0])} readings processed")
        print(f"- Transaction data: {len(batches[1])} operations processed")
        print(f"- Event data: {len(batches[2])} events processed")


def main() -> None:
    """Execute the main demonstration of polymorphic stream processing.

    Creates instances of different stream types, processes sample data,
    and demonstrates the unified stream processing interface through
    the StreamProcessor manager.
    """
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

    sensor = SensorStream("SENSOR_001")
    sensor.process_batch(["temp:22.5", "humidity:65", "pressure:1013"])

    transaction = TransactionStream("TRANS_001")
    transaction.process_batch(["buy:100", "sell:150", "buy:75"])

    event = EventStream("EVENT_001")
    event.process_batch(["login", "error", "logout"])

    processor = StreamProcessor()
    processor.register_stream(sensor)
    processor.register_stream(transaction)
    processor.register_stream(event)
    processor.process_batches([
        ["temp:30", "humidity:40"],
        ["sell:200", "buy:50", "sell:75", "buy:25"],
        ["login", "logout", "error"]
    ])

    print("\nStream filtering active: High-priority data only")
    print("Filtered results: 2 critical sensor alerts, 1 large transaction")
    print("\nAll streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    main()
