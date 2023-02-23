from func import handler

def test_func():
    assert handler("","") == {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {"Content-Type": "text/json; charset=utf-8"},
        "body": "Bonjour, ce message provient de mon TP CI BBBBBBB"
        }