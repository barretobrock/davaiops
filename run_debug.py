# Internal packages
from davaiops.configurations import DevelopmentConfig
from davaiops.routes import create_app

app = create_app(config_class=DevelopmentConfig)

if __name__ == "__main__":
    app.run()
