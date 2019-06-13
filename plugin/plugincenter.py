from plugin.base import BasePlugin


class PluginCenter:

    def __init__(self):
        self.plugins = {}

    def add_plugin(self, plugin):
        if isinstance(plugin, BasePlugin):
            self.plugins[plugin.name] = plugin
        else:
            raise ValueError("name:{0}__{1} is not Plugin".format(name, plugin.__class__))

    def get_plugin(self, name):
        return self.plugins[name]
