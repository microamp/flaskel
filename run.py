#-*- coding: utf-8 -*-

from flaskel import create_app

app = create_app()


if __name__ == "__main__":
    app.run("0.0.0.0", **{attr.lower(): app.config[attr]
                          for attr in ("PORT", "DEBUG",)
                          if attr in app.config})
