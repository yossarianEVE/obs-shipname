#!venv/bin/python
# -*- coding: utf-8 -*-


from esipy import App, EsiClient, EsiSecurity
from esipy.exceptions import APIException
from server import fetch_auth_code
from typeids import get_name_by_typeid
import webbrowser
import time
from secret import secret


def authenticate():
    app = App.create(url="https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility")
    security = EsiSecurity(
        app=app,
        redirect_uri='http://localhost:51350',
        client_id=secret['client_id'],
        secret_key=secret['secret_key'],
    )
    client = EsiClient(
        retry_requests=True,
        header={'User-Agent': 'shipLocation'},
        security=security
    )
    eve_sso_auth_url = security.get_auth_uri(scopes=['esi-location.read_ship_type.v1'])
    webbrowser.open(eve_sso_auth_url, new=2)  # open in a new browser tab
    auth_code = fetch_auth_code()  # fetch authentication code using a temporary web server
    security.auth(auth_code)

    return (app, client, security)


authenticated = False
while(True):
    if not authenticated:
        app, client, security = authenticate()
        api_info = security.verify()
        authenticated = True  # we're authed now


    try:
        op = app.op['get_characters_character_id_ship'](
            character_id=api_info['CharacterID']
        )
        ship = client.request(op)
    except APIException:
        pass


    # and to see the data behind, let's print it
    ship_type_id = ship.data['ship_type_id']
    ship_name = get_name_by_typeid(ship_type_id)
    with open('shipname.txt', 'w') as f:
        f.write(ship_name)
    time.sleep(5)
