# Internal packages
from davaiops.configurations import ProductionConfig
from davaiops.routes import create_app

app = create_app(config_class=ProductionConfig)

if __name__ == "__main__":
    app.run()
