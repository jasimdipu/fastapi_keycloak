from keycloak import KeycloakOpenID

# Keycloak auth

keycloak_openId = KeycloakOpenID(
    server_url="http://localhost:8080/auth/",
    client_id="myclient",
    realm_name="myrealm",
    client_secret_key="ePLbGH6LZOWzzDB7CNNVJDoIl2LFirbR"
)

config_well_known = keycloak_openId.well_known()

print(config_well_known)
