import json
import os
import requests
import urllib

from bottle import route, run, redirect, request

REDIRECT_URI=os.environ['REDIRECT_URI']
CLIENT_ID=os.environ['CLIENT_ID']
CLIENT_SECRET=os.environ['CLIENT_SECRET']
SCOPES="r_liteprofile%20r_emailaddress%20w_member_social"


@route('/')
def login():
    redirect(f'https://www.linkedin.com/oauth/v2/authorization?'
             f'response_type=code&'
             f'client_id={CLIENT_ID}&'
             f'redirect_uri={urllib.parse.quote(REDIRECT_URI, safe="")}&'
             f'scope={SCOPES}')


def get_headers(code):
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET 
    }
    r = requests.post("https://www.linkedin.com/oauth/v2/accessToken", data=payload)
    if r.status_code != 200:
        redirect("/")
    token = r.json()['access_token']
    return {"Authorization": f"Bearer {token}"}


def get_name(headers):
    r = requests.get("https://api.linkedin.com/v2/me", headers=headers)
    if r.status_code != 200:
        redirect("/")
    rj = r.json()
    return f'{rj["localizedFirstName"]} {rj["localizedLastName"]}'


def get_profile_pic_url(headers):
    r = requests.get("https://api.linkedin.com/v2/me?projection=(id,profilePicture(displayImage~:playableStreams))", headers=headers)
    elems = r.json()['profilePicture']['displayImage~']['elements']
    max_height = 0
    url = ''

    for elem in elems:
        height = elem['data']["com.linkedin.digitalmedia.mediaartifact.StillImage"]['storageSize']['height']
        if height > max_height:
            max_height = height
        url = elem['identifiers'][0]['identifier']
    return url


@route('/callback')
def callback():
    code = request.params.get('code')
    if code is None:
        redirect("/")

    headers = get_headers(code)
    name = get_name(headers)
    profile_pic_url = get_profile_pic_url(headers)

    return f'Your token: <code>{headers["Authorization"]}</code><p>Hello {name}</p><p><img src="{profile_pic_url}"></img></p>'


if __name__ == "__main__":
    run(host='0.0.0.0', port=8082, debug=True)
