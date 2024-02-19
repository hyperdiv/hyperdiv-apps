# Login Example

This is an example app with a login screen. `login_app/users_db.py` implements a mock users table that includes hashed passwords, salts, and auth tokens. When a user logs in successfully, the auth token is stored in local storage. Upon subsequent visits, the user is automatically logged in based on the already existing auth token. When a user logs out, the auth token is deleted from local storage, so they will be sent back to the login screen on subsequent visits.

The mock users and passwords are:

* Username: `bob`, password: `1234`
* Username: `lydia`, password: `5678`

![login](https://github.com/hyperdiv/hyperdiv-apps/assets/5980501/ac18cff4-cff0-44fe-9c8f-d70fcec64f15)
