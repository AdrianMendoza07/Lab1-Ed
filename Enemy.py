Enemy_data = {
  "Enemy": {
    "frames": [
      "cop1.png",
      "cop2.png",
      "cop3.png",
      "cop4.png",
      "cop5.png",
      "cop6.png",
      "cop7.png",
      "cop8.png",
      "cop9.png",
      "cop10.png"
    ],
    "animation": {
      "current_frame": 0,
      "animation_speed": 0.2
    },
    "movement": {
      "speed": 6,
      "delay_ms": 500,
      "active": False,
      "spawn_time": 0
    },
    "physics": {
      "vel_y": 0,
      "gravity": 1,
      "jump_force": -15,
      "on_ground": True,
      "ground_y": 300
    },
    "rect": {
      "x": 0,
      "y": 0,
      "width": 60,
      "height": 60
    },
    "methods": {
      "update": {
        "parameters": ["player_rect", "obstacles"],
        "description": "Controla animación, aparición, movimiento, salto automático, gravedad y colisión con el jugador"
      }
    }
  }
}