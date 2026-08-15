import azure.functions as func
import json, datetime, uuid

app = func.FunctionApp()

@app.route(route="items", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_output(
    arg_name="outputDocument",
    database_name="CloudLabDB",
    container_name="CloudLabItems",
    connection="CosmosDbConnectionSetting")
def ProcessLabData(req: func.HttpRequest, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    body = req.get_json()
    item_id = body.get("itemId", str(uuid.uuid4()))
    item = {
        "id": item_id,
        "itemId": item_id,
        "itemName": body.get("itemName", "Unnamed Item"),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    outputDocument.set(func.Document.from_dict(item))
    return func.HttpResponse(
        json.dumps({"message": "Item stored", "item": item}),
        status_code=200,
        mimetype="application/json"
    )
