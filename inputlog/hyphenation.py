
import logging
import xmlrpc.client

logger = logging.getLogger(__name__)


class Hyphenator:
    def __init__(self) -> None:
        # TODO: add check 
        self.rpc = None
        self.delimiter = None
        
    def load(self, settings):
        endpoint = f"http://127.0.0.1:{settings.hyphenate_rpc_port}"
        logger.info("Setting up the Hyphenation RPC Server at: {}".format(endpoint))
        self.delimiter = settings.delimiter
        self.rpc = xmlrpc.client.ServerProxy(endpoint)

    def hyphenate(self, token, lang):
        return self.rpc.hyphenate(
            {"word": token, "lang": lang, "delimiter": self.delimiter}
        ).split(self.delimiter)


MODEL = Hyphenator()