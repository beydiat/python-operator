def handler(event, context):
    body = "Bonjour, ce message provient de mon TP CI"
    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {"Content-Type": "text/json; charset=utf-8"},
        "body": body
        }

    return response
