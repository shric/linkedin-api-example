# linkedin-api-example
Simple example usage of LinkedIn API with "3-legged OAuth" authorization

## Requirements

- [bottle](https://bottlepy.org/docs/dev/).
- Tested on Python 3.x but should be trivial to make work on 2.7

## Usage

```bash
CLIENT_ID="your client_id" CLIENT_SECRET="your client_secret" REDIRECT_URI="your redirect_uri" python3 main.py
```

See [Authorization Code Flow (3-legged OAuth)](https://docs.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow?context=linkedin/context) step 1 and 2 for information about these parameters.

In this example code, it expects the `redirect_uri` to be something that hits the server with `/callback` but of course this can be changed. 
