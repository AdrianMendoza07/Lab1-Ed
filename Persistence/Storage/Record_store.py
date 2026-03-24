RecordStore_data = {
    "RecordStore": {
        "attributes": {
            "filename": "data.log"
        },
        "methods": {
            "get_all_records": {
                "description": "Devuelve todos los registros como lista de strings"
            },
            "add_record": {
                "parameters": ["record"],
                "description": "Agrega un registro nuevo al final del archivo"
            },
            "update_record": {
                "parameters": ["record"],
                "description": (
                    "Actualiza un registro existente según la clave (campo 6 = key). "
                    "Si no existe, lo agrega al final"
                )
            }
        }
    }
}