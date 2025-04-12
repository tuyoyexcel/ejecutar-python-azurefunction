import azure.functions as func
import pandas as pd
import json
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()

        datos = body.get("datos")
        codigo = body.get("codigo")

        if not datos or not codigo:
            return func.HttpResponse("❌ Faltan datos o código", status_code=400)

        # Crear DataFrame
        df = pd.DataFrame(datos[1:], columns=datos[0])
        local_vars = {'df': df}

        # Ejecutar código recibido
        exec(codigo, {}, local_vars)

        # Obtener resultado final
        resultado = None
        for var in reversed(local_vars.keys()):
            if var not in ["df"]:
                resultado = local_vars[var]
                break

        return func.HttpResponse(
            json.dumps({"resultado": str(resultado)}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"❌ Error ejecutando código: {e}")
        return func.HttpResponse(
            json.dumps({"resultado": f"❌ Error: {str(e)}"}),
            mimetype="application/json",
            status_code=500
        )
