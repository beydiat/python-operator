from messages import bonjour

def test_message():
    assert bonjour("Dubois") == "Bonjour M/Mme Dubois"