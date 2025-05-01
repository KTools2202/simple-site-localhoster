import os
import json
import toml
import yaml
import json5

from typing import Optional

CONFIG_BASENAME = "simple-site-localhoster"
SUPPORTED_EXTS = ["json", "json5", "jsonc", "yaml", "toml"]

class ConfigError(Exception):
    pass

def load_config(host: Optional[str] = None,
                port: Optional[int] = None,
                ssr_dir: Optional[str] = None,
                ssg_dir: Optional[str] = None,
                ssr_provider: Optional[str] = None,
                cli_config: Optional[str] = None) -> dict:
    config = {}

    cwd = os.getcwd()
    # auto-detect config file if not provided explicitly
    if cli_config:
        if not os.path.exists(cli_config):
            raise ConfigError(f"Config file not found: {cli_config}")
        config = parse_config(cli_config)
    else:
        config_files = [
            os.path.join(cwd, f"{CONFIG_BASENAME}.{ext}") 
            for ext in SUPPORTED_EXTS
            if os.path.exists(os.path.join(cwd, f"{CONFIG_BASENAME}.{ext}"))
        ]
        if len(config_files) > 1:
            raise ConfigError(
                f"Multiple config files found: {', '.join(config_files)}. Please specify one with --config."
            )
        if len(config_files) == 1:
            config = parse_config(config_files[0])

    # Override with CLI options if provided
    if host:
        config["host"] = host
    if port:
        config["port"] = port
    if ssr_dir:
        config["ssr_dir"] = ssr_dir
    if ssg_dir:
        config["ssg_dir"] = ssg_dir
    if ssr_provider:
        config["ssr_provider"] = ssr_provider

    return config

def parse_config(path: str) -> dict:
    ext = path.split(".")[-1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            if ext == "json":
                return json.loads(content)
            elif ext in ("json5", "jsonc"):
                return json5.loads(content)
            elif ext == "yaml":
                return yaml.safe_load(content)
            elif ext == "toml":
                return toml.loads(content)
            else:
                raise ConfigError(f"Unsupported config file type: {ext}")
    except Exception as e:
        raise ConfigError(f"Failed to parse config file {path}: {str(e)}")