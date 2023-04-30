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
            "properties": {
                "model": {"type": "string"},
                "temperature": {"type": "number"},
                "max_tokens": {"type": "number"},
            },
            "required": ["model", "temperature", "max_tokens"],
        },
        "discord": {
            "type": "object",
            "properties": {
                "dedicated_channel_id": {"type": "number"},
                "log_folder": {"type": "string"},
                "log_path_channel": {"type": "string"},
                "log_path_command": {"type": "string"},
            },
            "required": ["dedicated_channel_id", "log_folder", "log_path_channel", "log_path_command"],
        },
        "logger": {
            "type": "object",
            "properties": {
                "log_path_info": {"type": "string"},
                "log_level": {"type": "string"},
                "log_rotation": {"type": "number"},
                "log_retention": {"type": "string"},
                "log_compression_format": {"type": "string"},
            },
            "required": ["log_level", "log_rotation", "log_retention", "log_compression_format"],
        },
        "schedule": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]},
        "github": {
            "type": "object",
            "properties": {
                "user_stats": {"type": "string"},
                "streak_stats": {"type": "string"},
                "default_user": {"type": "string"},
            },
            "required": ["user_stats", "streak_stats", "default_user"],
        },
    },
    "required": ["openai", "discord", "logger", "schedule", "github"],
}
