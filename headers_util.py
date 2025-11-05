def add_vensec_auth_to_headers(session_id, client_id, auth):
    return {
        'accept': '*/*',
        'access-control-allow-origin': '*',
        'content-type': 'application/json; charset=utf-8, application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'session_id': session_id,
        'x-client-id': client_id,
        'Authorization': auth,
        'Content-Type': "application/json; charset=utf-8"
    }


def add_niftytrader_auth_to_headers(auth):
    return {
        'Authorization': auth,
        'accept': '*/*',
        'access-control-allow-origin': '*',
        'content-type': 'application/json; charset=utf-8, application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    }