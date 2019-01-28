import logging
from esipysi import EsiPysi, EsiAuth
from esipysi.cache import RedisCache
import redis
import config

log = logging.getLogger(__name__)

class ESI:
    def __init__(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=1)
        self.cache = RedisCache(r)
        self.esi = EsiPysi(
            'https://esi.evetech.net/_latest/swagger.json?datasource=tranquility',
            user_agent=config.email,
            cache=self.cache
        )

        #self.auth_esi = EsiAuth(config.client_id, config.secret_key)

    def search(self, scope, entity):
        entity_search = self.esi.get_operation("get_search")
        result = entity_search.json(
            categories=scope,
            search=entity,
            strict=True
        )
        return result

    def loose_search(self, scope, entity):
        entity_search = self.esi.get_operation("get_search")
        result = entity_search.json(
            categories=scope,
            search=entity,
            strict=False
        )
        return result

    def kill_lookup(self, kill_id, kill_hash):
                    kill_call = self.esi.get_operation("get_killmails_killmail_id_killmail_hash")
                    result = kill_call.json(
                            killmail_id=kill_id, 
                            killmail_hash=kill_hash
                            )
                    return result
