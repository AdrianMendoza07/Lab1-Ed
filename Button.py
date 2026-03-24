Button_data = {
  "Button": {
    "text": "",
    "font": "FontObject",
    "rect": {
      "x": 0,
      "y": 0,
      "width": 0,
      "height": 0,
      "center": [0, 0]
    },
    "colors": {
      "baseColor": [20, 20, 50, 160],
      "hoverColor": [60, 20, 90],
      "clickColor": [0, 255, 200],
      "textColor": [220, 240, 255],
      "currentColor": [20, 20, 50, 160]
    },
    "state": {
      "is_pressed": False,
      "press_time": 0,
      "delay": 150
    },
    "methods": {
      "handle_event": {
        "parameters": ["event"],
        "description": "Gestiona clics del mouse y actualiza el estado del botón"
      },
      "update": {
        "parameters": ["mouse_pos"],
        "description": "Actualiza el color según la interacción del mouse"
      },
      "is_ready": {
        "description": "Indica si el botón está listo (siempre True en este caso)"
      },
      "draw": {
        "parameters": ["screen", "selected"],
        "description": "Dibuja el botón en pantalla con su estado visual"
      }
    }
  }
}