"""
Links:
    https://towardsdatascience.com/how-to-validate-your-json-using-json-schema-f55f4b162dce
    https://json-schema.org/understanding-json-schema/reference/object.html

This means that no additional properties are allowed on the object:
"additionalProperties": False

"""
schema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "openai": {
            "type": "object",
            "required": ["model", "temperature", "max_tokens"],
            "additionalProperties": False,
            "properties": {
                "model": {"type": "string"},
                "temperature": {"type": "number"},
                "max_tokens": {"type": "number"},
            },
        },
        "discord": {
            "type": "object",
            "required": ["dedicated_channel_id", "log_folder", "log_path_channel", "log_path_command"],
            "additionalProperties": False,
            "properties": {
                "dedicated_channel_id": {"type": "number"},
                "log_folder": {"type": "string"},
                "log_path_channel": {"type": "string"},
                "log_path_command": {"type": "string"},
                "log_path_discord": {"type": "string"},
                "discord_log_level": {"type": "string"},
            },
        },
        "logger": {
            "type": "object",
            "required": ["log_path_info", "log_level", "log_rotation", "log_retention", "log_compression_format"],
            "properties": {
                "log_path_info": {"type": "string"},
                "log_level": {"type": "string"},
                "log_rotation": {"type": "number"},
                "log_retention": {"type": "string"},
                "log_compression_format": {"type": "string"},
            },
        },
        "schedule": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]},
        "github": {
            "type": "object",
            "required": ["user_stats", "streak_stats", "default_user"],
            "additionalProperties": False,
            "properties": {
                "user_stats": {"type": "string"},
                "streak_stats": {"type": "string"},
                "default_user": {"type": "string"},
            },
        },
    },
    "required": ["openai", "discord", "logger", "schedule", "github"],
}
