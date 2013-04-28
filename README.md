owarunner
===========

Simple WebKit-powered OpenWebApp launcher

Usage
=
```
usage: owa [-h] [--width WIDTH] [--height HEIGHT] [--fullscreen] [--custom] url [murl]

positional arguments:
  url              URL for the App without protocol
  murl             Relative route for the manifest file (usually something like '/appname.webapp')

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    Default window width
  --height HEIGHT  Default window width
  --fullscreen     Start fullscreened
  --custom         Set custom decoration
```

Some test apps
=
```./owa.py mobile.twitter.com /cache/twitter.webapp --width 500```

```./owa.py app.loqui.im /loqui.webapp --width 300```
