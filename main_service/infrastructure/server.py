from infrastructure.api.app import create_app
from infrastructure.config import get_config
from infrastructure.providers.container import create_container

config = get_config()
container = create_container()
app = create_app(container, config)
