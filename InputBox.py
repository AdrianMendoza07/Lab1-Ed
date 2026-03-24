InputBox_data = {
  "InputBox": {
    "rect": {
      "x": 0,
      "y": 0,
      "width": 0,
      "height": 0
    },
    "font": "FontObject",
    "state": {
      "text": "",
      "active": False
    },
    "colors": {
      "baseColor": [20, 20, 50],
      "activeColor": [60, 20, 90],
      "textColor": [220, 240, 255],
      "glowColor": [0, 255, 200]
    },
    "methods": {
      "handle_event": {
        "parameters": ["event"],
        "description": "Maneja clics del mouse y entrada de teclado para editar el texto"
      },
      "update": {
        "description": "Actualización lógica (vacía en este caso)"
      },
      "draw": {
        "parameters": ["screen"],
        "description": "Dibuja el cuadro de texto, borde, efecto glow y contenido"
      }
    }
  }
}