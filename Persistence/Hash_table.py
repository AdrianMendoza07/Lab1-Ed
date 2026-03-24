HashTable_data = {
  "HashTable": {
    "capacity": 10,
    "buckets": [
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      [],
      []
    ],
    "methods": {
      "hash_function": {
        "description": "Suma los valores ASCII de los caracteres de la clave y aplica módulo con la capacidad"
      },
      "insert": {
        "parameters": ["key", "position"],
        "description": "Inserta o actualiza un HashEntry en el bucket correspondiente"
      },
      "search": {
        "parameters": ["key"],
        "description": "Busca una clave y retorna su posición o -1 si no existe"
      }
    }
  }
}