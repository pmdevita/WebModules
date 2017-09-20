# First, import the BaseModule class so we can inherit from it
from BaseModule import BaseModule


# Your class must be named Module so Web Modules can find it
class Module(BaseModule):
    # Friendly name of your module for users to see
    name = "Example Module"
    # Route that your module will mount at
    route = "example"

    def run(self, route: list, method: str, args: dict):
        return "Example Module"
