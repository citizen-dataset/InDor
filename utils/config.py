import yaml

def load_config(config_path: str) -> dict:
    """Loads configuration from a YAML file."""
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        raise
    except Exception as e:
        print(f"Error parsing configuration file {config_path}: {e}")
        raise 