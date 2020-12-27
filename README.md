# URL-Shortener
This repository holds the code for a URL shortener which accepts a url of any length and generates a **fixed length** hashed url for it. The hash is generated using a counter based approach, **which can be scaled using a zookeeper** when the application goes into production. 

> Since the hashes generated are irreversible, using incremental numbers (counter) won't pose any threat to the security of this application.

## Features
* Login
* Register
* Url Shortener
* Get hash corresponding to a saved URL
* Get URL corresponding to a saved shortened URL

## Flow of Project
User is required to sign up in order to access the functionality of the logical API. Login/ SignUp will fetch the token for the user which can be used to access the validation API. Once the user has the token, they can send the payload in the request body and get the response in json form according to the logic. Token is to be attached in the headers.

## Flow of logic
>*	make a counter: number of entries in the database
>*	use that counter to generate the hash
>*	use that hash against the url
>*	store that url and hash in the database

## Paths (local)

* Register: `http://0.0.0.0:8000/register/`

* Login: `http://0.0.0.0:8000/login/`

* URL Shortening API: `http://0.0.0.0:8000/shorten/`

* Get Hash of a saved URL: `http://0.0.0.0:8000/url2hash/`

* Get actual URL of a shortened URL: `http://0.0.0.0:8000/hash2url/`

## Staged
The django app is hosted on an EC2 server, hence you can directly check the functionality of the API through there. No auth token is required in this case, the app can be accessed [here](http://18.224.7.211:8000/shorten).

