import firebase_admin
from firebase_admin import credentials,firestore
import os

def initialize_firebase():
    cred = credentials.Certificate({
            "type": "service_account",
            "project_id": "turnosya-c5672",
            "private_key_id": "1d2d96510c4b26b9c2e71c58b6658f9a39993609",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDcxS0VjRRwOAE7\nYgtqy2h4OfT6NOvVHIiz1gG8o1EPPaNydsu8FW1RMCo4KyKjHspS5ZhEeiH1sf2p\nAazgsa3/MZH2CUbzt3tAaCWdkkDo+FLT2QslveEvCvZ18ePu69ruWKIML83X2exx\n2py0PaY0RFTo1SFSN3pkiNnaCnnpX6naUjhrMiLgBAGNOABPJvMk29d4xxdHcis/\nzcsU9nsP6sjsOycSFxdfkf9uNxi5NKHy27d0bPzMwsfSUZW4HrqMHZuoUBHj+BTb\nAukZY1UzHJqy4fJ5BDv6EtVndgMCPqgtfDK8mScpFwvVXW5tlHW15ueHzRI5zWcY\noY782UBzAgMBAAECggEADQAs3X4HXBcQNi0EkG9rYYPC4hEdFNmvUIJ5FmC6X0lj\n8f5TlRSLRs1X+c110WFOIio/GJk7SBAJPgXz5kTQWEd/rvDGQDKSjC0V5KeThvnz\nTA0V/kz7kRz2J+VCD58ir10s0xw65PaCWVoPAauNDrrkvSlVOFWSsY+Vifo1SlbU\nfAX8QryxCwqnheoGkf3Hb3KQgUxuqJAM7ZRVmyJn/yY3dZ0rI15I/+yhuWRm+JCn\n4XjXZe0XQnzfoN4LcHYEOs0Uupwaf4EfSgQV7qoQ6nOU19NXqrUkTSK1oi+CBJRX\n4PLqNyfKl7Irm/JUVirv/lG/bKEzdmfLQMlJe+teIQKBgQD29BpT9RoSUJS7E+nP\n+eOpcbyK9TbBIi/jFa12UQQsArGOuOjaEdDXafwrQt1PeIefR6BwrRCA1B9/JU5Y\ntpNJNdGEHTRRHEe4mhC+rO4AmQ6K9wknJyamNTyLcQmn1yJvLGGZgAq3Gd1xoQpD\n29MccGdpU5IMMhL4HHpvTr5cmQKBgQDk24ebAVRahE+TNIa3YqONdF8dNKd3pNYE\nOF7TilMfrOTxxsJxDOp3FwqY/71Ze/Ux7vnFPxTaz4wD+Os/73Mp0ggFhXsy2qQa\nPlWJGNXDCJOR1FVbQihME7S3wAsN/t1PEt9llLCjTWT8XnjptQxWlDrgtIVPYEPx\nF1uNiRRA6wKBgF6tu6JQqAw5hKwsuEmaPqRqDKUh2jo1hzKCzxw7d2QALF7RmcRx\nbCYKZjmXyw164lQ4u9Q3JcqeiOzQOrdcWB+LWKZUJAis1Pp7ZswTtLPZ+m9gwsuW\nAQVcB7hWQCNvIa6Jz2lwY6tLaVD1MuBNWSTgG2WQOsAeOpORJ4ehIu6RAoGBAMn+\nSW4yejV6WpHe5pit4xVTBTBN7RHY11zaNDgZ+swWWexcNfp6H+gE2kG4V3PHyN7N\nwn6p8so+LaLD7T99JPRggNv+uIJmIDlZkz1yQhnmU/l+o+fsOI0NR5B3XEp6DPNi\nAPMzjcRU5zEoYShFuCIiquTx8Efi+5SrvQ7rUokJAoGAdVW5bR7QVz3OS3oXt9eD\nK9y9Vc41En7DDV6B9wbd/Tg4+aT52jRqbjYQyV0qCktzmnl62w1G10tWD0eYlbHg\nET8gcnsLP4g9eJxww/oA33+oCjatRkuJ84ga9IT1cgJ3LIHuDZ+xj7jRBjCTE6cb\niaCxfMUEuAeso/UWiDsqJVM=\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-fbsvc@turnosya-c5672.iam.gserviceaccount.com",
            "client_id": "110209063338957749643",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40turnosya-c5672.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
    })
    firebase_admin.initialize_app(cred,{
        "storageBucket": "turnosya-c5672.firebasestorage.app"
    })
    print("Firebase SDK inicializado correctamente.")
    return firestore.client()

db = initialize_firebase()
    