data = {
  "runLeaderboardMenu": {
    "screen": {
      "width": None,
      "height": None
    },
    "assets": {
      "background": None,
      "fonts": {
        "title_font": "assets/fonts/Orbitron-Bold.ttf",
        "text_font": "assets/fonts/Orbitron-Regular.ttf"
      }
    },
    "ui": {
      "title": "LEADERBOARD",
      "button": {
        "text": "Volver",
        "width": 300,
        "height": 60,
        "position": None
      },
      "table": {
        "width": 600,
        "height": 400,
        "columns": ["POS", "NAME", "SCORE"],
        "max_rows": 10
      }
    },
    "state": {
      "initialized": False,
      "action": None,
      "leaderboard": []
    },
    "data_source": {
      "repository": "ProfileRepository",
      "method": "get_all_profiles",
      "sorting": {
        "by": "score",
        "order": "descending"
      }
    },
    "logic": {
      "events": {
        "quit": 0,
        "back_button": "back"
      },
      "processing": {
        "limit_name_length": 12,
        "score_cast": "int",
        "top_n": 10
      },
      "ranking_colors": {
        "1": [255, 215, 0],
        "2": [192, 192, 192],
        "3": [205, 127, 50],
        "default": [220, 240, 255]
      }
    },
    "render": {
      "background": True,
      "title_glow": True,
      "table": True,
      "headers": True,
      "rows": True,
      "button": True
    },
    "return_values": {
      "quit": 0,
      "back": 1,
      "continue": 3,
      "error": 1
    }
  }
}