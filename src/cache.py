"""
cache.py — wrapper Redis para o Bodies Barber.

Uso básico:
    from cache import cache_get, cache_set, cache_delete

    # Ler do cache (retorna None se não existir/Redis off)
    data = cache_get("minha_chave")

    # Gravar no cache por 5 minutos (300 s)
    cache_set("minha_chave", data, ttl=300)

    # Invalidar manualmente
    cache_delete("minha_chave")
"""
import os
import json
import logging
import redis

logger = logging.getLogger(__name__)

#  conexão (lazy singleton) 

_client = None

def _get_client():
    global _client
    if _client is not None:
        return _client

    url = os.environ.get("REDIS_URL")
    if not url:
        return None          # cache desativado

    try:
        _client = redis.from_url(url, decode_responses=True, socket_connect_timeout=2)
        _client.ping()       # valida conexão ao iniciar
        logger.info("Redis conectado: %s", url.split("@")[-1])
    except Exception as exc:
        logger.warning("Redis indisponível — cache desativado: %s", exc)
        _client = None

    return _client


#  API pública 

def cache_get(key: str):
    """Retorna o valor (já desserializado) ou None."""
    client = _get_client()
    if client is None:
        return None
    try:
        raw = client.get(key)
        return json.loads(raw) if raw is not None else None
    except Exception as exc:
        logger.warning("cache_get(%s) falhou: %s", key, exc)
        return None


def cache_set(key: str, value, ttl: int = 300):
    """Serializa e grava no Redis com expiração em segundos (padrão 5 min)."""
    client = _get_client()
    if client is None:
        return
    try:
        client.setex(key, ttl, json.dumps(value, default=str))
    except Exception as exc:
        logger.warning("cache_set(%s) falhou: %s", key, exc)


def cache_delete(*keys: str):
    """Remove uma ou mais chaves do Redis."""
    client = _get_client()
    if client is None:
        return
    try:
        client.delete(*keys)
    except Exception as exc:
        logger.warning("cache_delete(%s) falhou: %s", keys, exc)