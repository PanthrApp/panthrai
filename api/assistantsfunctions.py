menufunc = {
  "type": "function",
  "function": {
    "name": "get_menu",
    "description": "Get the school lunch menu for a date",
    "parameters": {
      "type": "object",
      "properties": {
      "date": {"type": "string", "description": "The date in mm/dd/yyyy format"}
      },
      "required": ["date"]
    }
  }
}