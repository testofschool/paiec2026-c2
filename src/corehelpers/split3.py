"""Authoritative split3 seed expression."""
import hashlib

split_seed = lambda b:int(hashlib.sha256(('split3:'+b).encode()).hexdigest()[:8],16)
