import patreon

client_id = "hrGEn5uURNyJgs18LizOBhFi5HevvZqXBSwvLSf7oU9j5j0eOcybj7gaDMFjzGjh"
client_secret = "r0dam9X9vpQ2o4nqAJm3VbPizcelQg0mIQZacBq0OStUV4P8_T8w3AWZfCpKBEGs"
# Here we go boys. We're gonna need CLOUD COMPUTING for this token retrieval (FUCK 3-LEGGED OAUTH)
# https://epsagon.com/blog/aws-lambda-and-python-flask-getting-started/
def oauth():
    oauth_client = patreon.OAuth(client_id, client_secret)
    tokens = oauth_client.get_tokens('abc123', 'oauth/redirect')
    access_token = tokens['access_token']

    api_client = patreon.API(access_token)
    user_response = api_client.get_identity()
    user = user_response.data()

oauth()