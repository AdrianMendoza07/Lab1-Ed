runGame_data = {
  "runGame": {
    "screen": {
      "width": 0,
      "height": 0
    },
    "assets": {
      "background": "bg",
      "obstacle_image": "assets/images/obstacle/obstaculo1.png"
    },
    "state": {
      "initialized": False,
      "spawn_timer": 0,
      "obstacles": []
    },
    "spawn": {
      "interval_ms": 1500,
      "obstacle": {
        "x": "screen_width",
        "ground_y": "screen_height - 100",
        "speed": 8
      }
    },
    "events": {
      "quit_action": "return 0"
    },
    "logic": {
      "update_obstacles": "Actualizar posición de cada obstáculo",
      "cleanup": "Eliminar obstáculos fuera de pantalla",
      "collision": {
        "on_hit": "return 1",
        "message": "Colisión detectada"
      }
    },
    "render": {
      "draw_background": True,
      "draw_obstacles": True
    },
    "return_values": {
      "quit": 0,
      "collision": 1,
      "continue": 6
    }
  }
}