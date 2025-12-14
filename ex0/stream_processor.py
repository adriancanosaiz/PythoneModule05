from typing import Any, List


class DataProcessor:
    """Base class for processing different types of data.

    This class provides a generic framework
    for data processing with validation,
    analysis, and output formatting capabilities.

    Attributes:
        name (str): The name identifier for this processor.
        silent (bool): Flag to suppress output messages during processing.
    """

    def __init__(self, name: str, silent: bool = False) -> None:
        """Initialize the DataProcessor.

        Args:
            name (str): The name of the processor.
            silent (bool): If True, suppresses initialization
                            and processing messages.
                Defaults to False.
        """
        self.name = name
        self.silent = silent
        if not self.silent:
            print(f"\nInitializing {self.name}...")

    def process(self, data: Any) -> str:
        """Process data through validation, analysis, and formatting stages.

        Typical flow:
        1) Validate input data
        2) Analyze/transform the data
        3) Format output

        Args:
            data (Any): The data to be processed.

        Returns:
            str: Formatted output string with processing results.
        """
        if not self.silent:
            if isinstance(data, str):
                print(f'Processing data: "{data}"')
            else:
                print(f"Processing data: {data}")

        if not self.validate(data):
            return "Invalid data"

        result = self.analyze(data)
        return self.format_output(result)

    def validate(self, data: Any) -> bool:
        """Validate the input data.

        Default implementation accepts any data type. Subclasses should
        override this method for stricter validation.

        Args:
            data (Any): The data to validate.

        Returns:
            bool: True if data is valid, False otherwise.
        """
        return True

    def analyze(self, data: Any) -> Any:
        """Analyze the validated data.

        Default implementation returns data as-is. Subclasses should
        override this method for specific analysis logic.

        Args:
            data (Any): The validated data to analyze.

        Returns:
            Any: Analysis results.
        """
        return data

    def format_output(self, result: Any) -> str:
        """Format the analysis result into a string output.

        Default implementation provides basic formatting. Subclasses can
        override for custom formatting.

        Args:
            result (Any): The result from data analysis.

        Returns:
            str: Formatted output string.
        """
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    """Processor specialized in handling numeric data.

    Processes lists of numeric values and computes statistical measures
    such as count, sum, and average.
    """

    def __init__(self, silent: bool = False) -> None:
        """Initialize the NumericProcessor.

        Args:
            silent (bool): If True, suppresses validation
                            and processing messages.
                Defaults to False.
        """
        super().__init__("Numeric Processor", silent)

    def validate(self, data: Any) -> bool:
        """Validate that data is a list of numbers.

        Args:
            data (Any): The data to validate.

        Returns:
            bool: True if data is a list of int/float, False otherwise.
        """
        if (isinstance(data, list) and
                all(isinstance(x, (int, float)) for x in data)):
            if not self.silent:
                print("Validation: Numeric data verified")
            return True
        return False

    def analyze(self, data: List[int]) -> dict:
        """Analyze numeric data and compute statistics.

        Calculates count, sum, and average of the numeric values.

        Args:
            data (List[int]): List of numeric values.

        Returns:
            dict: Dictionary containing count, sum, and avg keys.
        """
        return {
            "count": len(data),
            "sum": sum(data),
            "avg": sum(data) / len(data)
        }

    def format_output(self, result: dict) -> str:
        """Format numeric analysis results.

        Args:
            result (dict): The analysis result with count, sum, and avg keys.

        Returns:
            str: Formatted string with processing results.
        """
        return (
            f"Output: Processed {result['count']} numeric values, "
            f"sum={result['sum']}, avg={result['avg']}"
        )


class TextProcessor(DataProcessor):
    """Processor specialized in handling text data.

    Analyzes text strings and computes character and word counts.
    """

    def __init__(self, silent: bool = False) -> None:
        """Initialize the TextProcessor.

        Args:
            silent (bool): If True, suppresses validation
                            and processing messages.
                Defaults to False.
        """
        super().__init__("Text Processor", silent)

    def validate(self, data: Any) -> bool:
        """Validate that data is a string.

        Args:
            data (Any): The data to validate.

        Returns:
            bool: True if data is a string, False otherwise.
        """
        if isinstance(data, str):
            if not self.silent:
                print("Validation: Text data verified")
            return True
        return False

    def analyze(self, data: str) -> dict:
        """Analyze text data and compute metrics.

        Counts characters and words in the text.

        Args:
            data (str): String to analyze.

        Returns:
            dict: Dictionary containing chars and words keys.
        """
        return {
            "chars": len(data) + 1,
            "words": len(data.split())
        }

    def format_output(self, result: dict) -> str:
        """Format text analysis results.

        Args:
            result (dict): The analysis result with chars and words keys.

        Returns:
            str: Formatted string with processing results.
        """
        return (
            f"Output: Processed text: "
            f"{result['chars']} characters, {result['words']} words"
        )


class LogProcessor(DataProcessor):
    """Processor specialized in handling log entries.

    Parses and analyzes log messages with level and message components.
    Expected format: "LEVEL: message"
    """

    def __init__(self, silent: bool = False) -> None:
        """Initialize the LogProcessor.

        Args:
            silent (bool): If True, suppresses validation
                            and processing messages.
                Defaults to False.
        """
        super().__init__("Log Processor", silent)

    def validate(self, data: Any) -> bool:
        """Validate that data is a log string with proper format.

        Expected format: "LEVEL: message"

        Args:
            data (Any): The data to validate.

        Returns:
            bool: True if data is a string containing ':', False otherwise.
        """
        if isinstance(data, str) and ":" in data:
            if not self.silent:
                print("Validation: Log entry verified")
            return True
        return False

    def analyze(self, data: str) -> dict:
        """Analyze log data and extract components.

        Parses log string into level and message components.

        Args:
            data (str): Log string in format "LEVEL: message".

        Returns:
            dict: Dictionary containing level and message keys.
        """
        level, message = data.split(":", 1)
        return {
            "level": level.strip().upper(),
            "message": message.strip()
        }

    def format_output(self, result: dict) -> str:
        """Format log analysis results.

        Adds an appropriate tag (ALERT or INFO) based on the log level.

        Args:
            result (dict): The analysis result with level and message keys.

        Returns:
            str: Formatted string with log level and message.
        """
        tag = "ALERT" if result["level"] == "ERROR" else "INFO"
        return (
            f"Output: [{tag}] {result['level']} level detected: "
            f"{result['message']}"
        )


def main() -> None:
    """Execute the main demonstration of data processors.

    Creates instances of each processor type and processes sample data
    to demonstrate the polymorphic processing capabilities. Shows both
    verbose and silent processing modes.
    """
    print("\n=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")

    num = NumericProcessor()
    print(num.process([1, 2, 3, 4, 5]))

    text = TextProcessor()
    print(text.process("Hello Nexus World"))

    log = LogProcessor()
    print(log.process("ERROR: Connection timeout"))

    print("\n=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")

    num_result = NumericProcessor(silent=True).process([1, 2, 3])
    num_result = num_result.replace("Output: ", "")
    print(f"Result 1: {num_result}")

    text_result = TextProcessor(silent=True).process("Hello World")
    text_result = text_result.replace("Output: ", "")
    print(f"Result 2: {text_result}")

    log_result = LogProcessor(silent=True).process("INFO: System ready")
    log_result = log_result.replace("Output: ", "")
    print(f"Result 3: {log_result}")

    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()
