[![AGPL](https://img.shields.io/badge/license-AGPL-blue.svg)](https://raw.githubusercontent.com/jboynyc/cmus_app/master/LICENSE)

# cmus-remote web app

This is a web app to control a server instance of
[`cmus`](https://cmus.github.io/), a powerful music player, remotely. It only
supports basic player and volume controls, not adding items to the playlist. 


## Dependencies

`cmus` is required, of course. The backend is written in Python and has been
tested with Python 3.8 (Python 3 variants should work)

All frontend dependencies are bundled:[Zepto](http://zeptojs.com/), [Kube](http://imperavi.com/kube), and [Font
Awesome](http://fortawesome.github.com/Font-Awesome/). Thanks to the creators
for making them available under permissive licenses. 

[`bottle`](http://bottlepy.org) needs to be manually installed though
## Instructions

The web app can run on the same host as the `cmus` instance you want to control
or a different one, but both hosts will have to have `cmus` installed.

### On the cmus host

Just run it without `--listen` argument

### On the web app host

- Fetch cmus_app:

        $ git clone git://github.com/jboynyc/cmus_app
        $ cd cmus_app

- Edit the configuration file. (Optional.)
- Run the app with a configuration file or command-line options:

        $ python app.py -f <config_file>
        $ python app.py --welcome "The Groovbox" -a localhost -p 8080

### Anywhere on your network

- Open your browser and navigate to `http://<host>:<port>`.

Enjoy!

## Prior Art and Alternatives

Take a look on the [cmus wiki](https://github.com/cmus/cmus/wiki/remote-control).
