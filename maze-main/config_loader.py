class Config:
    """Configuration loader for the maze generator.

    Reads and validates parameters from a configuration file.
    """

    def __init__(self, filename: str) -> None:
        """Initialize configuration with default values and load the file."""
        self.WIDTH: int = 0
        self.HEIGHT: int = 0
        self.ENTRY: tuple[int, int] = (0, 0)
        self.EXIT: tuple[int, int] = (0, 0)
        self.OUTPUT_FILE: str = ""
        self.PERFECT: bool = False
        self.SEED: int | None = None

        self._load(filename)
        self.validate_data()

    @staticmethod
    def check_split(parts: list[str], original_text: str, delimiter: str) -> None:
        """Validate that a split operation produced exactly two parts."""
        if len(parts) != 2:
            raise ValueError(
                f"Bad syntax in configuration. Missing '{delimiter}' in: '{original_text.strip()}'"
            )
        if not parts[0].strip() or not parts[1].strip():
            raise ValueError(
                f"Bad syntax in configuration. Missing value for key in: '{original_text.strip()}'"
            )

    def _load(self, filename: str) -> None:
        """Load configuration from file."""
        seen_keys: set[str] = set()

        try:
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or line == "":
                        continue

                    parts = line.split("=", 1)
                    self.check_split(parts, line, "=")

                    key, value = parts
                    key = key.strip().upper()
                    value = value.strip()

                    if key in seen_keys:
                        raise ValueError(f"Duplicate key found in configuration: {key}")
                    seen_keys.add(key)

                    if key in ["WIDTH", "HEIGHT", "SEED"]:
                        try:
                            numeric_value = int(value)
                            if key == "WIDTH":
                                self.WIDTH = numeric_value
                            elif key == "HEIGHT":
                                self.HEIGHT = numeric_value
                            elif key == "SEED":
                                self.SEED = numeric_value
                        except ValueError:
                            raise ValueError(f"Invalid configuration: The value for {key} must be a number.")

                    elif key in ["ENTRY", "EXIT"]:
                        coords = value.split(",")
                        self.check_split(coords, value, ",")
                        try:
                            x = int(coords[0].strip())
                            y = int(coords[1].strip())
                            if key == "ENTRY":
                                self.ENTRY = (x, y)
                            elif key == "EXIT":
                                self.EXIT = (x, y)
                        except ValueError:
                            raise ValueError(f"Invalid configuration: Coordinates for {key} must be numbers.")

                    elif key == "OUTPUT_FILE":
                        self.OUTPUT_FILE = value
                    elif key == "PERFECT":
                        self.PERFECT = value.lower() == "true"

            # Check for required keys
            required_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
            for req_key in required_keys:
                if req_key not in seen_keys:
                    raise ValueError(f"Error: '{req_key}' is missing from the configuration file.")

        except FileNotFoundError:
            raise ValueError(f"Error: The configuration file '{filename}' was not found.")

    def validate_data(self) -> None:
        """Validate all configuration values."""
        if self.WIDTH <= 1 or self.HEIGHT <= 1:
            raise ValueError("WIDTH and HEIGHT must be greater than 1.")

        if self.ENTRY == self.EXIT:
            raise ValueError("ENTRY and EXIT points must be different.")

        if (self.ENTRY[0] < 0 or self.ENTRY[0] >= self.WIDTH or
                self.ENTRY[1] < 0 or self.ENTRY[1] >= self.HEIGHT):
            raise ValueError("ENTRY point must be inside the maze bounds.")

        if (self.EXIT[0] < 0 or self.EXIT[0] >= self.WIDTH or
                self.EXIT[1] < 0 or self.EXIT[1] >= self.HEIGHT):
            raise ValueError("EXIT point must be inside the maze bounds.")

        if self.OUTPUT_FILE == "":
            raise ValueError("OUTPUT_FILE is missing in the configuration.")


if __name__ == "__main__":
    try:
        c = Config("config.txt")
        print(c.WIDTH)
        print(c.HEIGHT)
        print(c.ENTRY)
        print(c.EXIT)
        print(c.OUTPUT_FILE)
        print(c.PERFECT)
        print(c.SEED)
    except Exception as e:
        print(e)
