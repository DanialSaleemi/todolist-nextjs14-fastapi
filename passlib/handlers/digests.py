"""passlib.handlers.digests - plain hash digests
"""
#=============================================================================
# imports
#=============================================================================
# core
import hashlib
import logging; log = logging.getLogger(__name__)
# site
# pkg
from passlib.utils import to_native_str, to_bytes, render_bytes, consteq
from passlib.utils.compat import unicode, str_to_uascii
import passlib.utils.handlers as uh
from passlib.crypto.digest import lookup_hash
# local
__all__ = [
    "create_hex_hash",
    "hex_md4",
    "hex_md5",
    "hex_sha1",
    "hex_sha256",
    "hex_sha512",
]

#=============================================================================
# helpers for hexadecimal hashes
#=============================================================================
class HexDigestHash(uh.StaticHandler):
    """this provides a template for supporting passwords stored as plain hexadecimal hashes"""
    #===================================================================
    # class attrs
    #===================================================================
    _hash_func = None # hash function to use - filled in by create_hex_hash()
    checksum_size = None # filled in by create_hex_hash()
    checksum_chars = uh.HEX_CHARS

    #: special for detecting if _hash_func is just a stub method.
    supported = True

    #===================================================================
    # methods
    #===================================================================
    @classmethod
    def _norm_hash(cls, hash):
        return hash.lower()

    def _calc_checksum(self, secret):
        if isinstance(secret, unicode):
            secret = secret.encode("utf-8")
        return str_to_uascii(self._hash_func(secret).hexdigest())

    #===================================================================
    # eoc
    #===================================================================

def create_hex_hash(digest, module=__name__, django_name=None, required=True):
    """
    create hex-encoded unsalted hasher for specified digest algorithm.

    .. versionchanged:: 1.7.3
        If called with unknown/supported digest, won't throw error immediately,
        but instead return a dummy hasher that will throw error when called.

        set ``required=True`` to restore old behavior.
    """
    info = lookup_hash(digest, required=required)
    name = "hex_" + info.name
    if not info.supported:
        info.digest_size = 0
    hasher = type(name, (HexDigestHash,), dict(
        name=name,
        __module__=module, # so ABCMeta won't clobber it
        _hash_func=staticmethod(info.const), # sometimes it's a function, sometimes not. so wrap it.
        checksum_size=info.digest_size*2,
        __doc__="""This class implements a plain hexadecimal %s hash, and follows the :ref:`password-hash-api`.

It supports no optional or contextual keywords.
""" % (info.name,)
    ))
    if not info.supported:
        hasher.supported = False
    if django_name:
        hasher.django_name = django_name
    return hasher

#=============================================================================
# predefined handlers
#=============================================================================

# NOTE: some digests below are marked as "required=False", because these may not be present on
#       FIPS systems (see issue 116).  if missing, will return stub hasher that throws error
#       if an attempt is made to actually use hash/verify with them.

hex_md4     = create_hex_hash("md4", required=False)
hex_md5     = create_hex_hash("md5", django_name="unsalted_md5", required=False)
hex_sha1    = create_hex_hash("sha1", required=False)
hex_sha256  = create_hex_hash("sha256")
hex_sha512  = create_hex_hash("sha512")

#=============================================================================
# htdigest
#=============================================================================
class htdigest(uh.MinimalHandler):
    """htdigest hash function.

    .. todo::
        document this hash
    """
    name = "htdigest"
    setting_kwds = ()
    context_kwds = ("user", "realm", "encoding")
    default_encoding = "utf-8"

    @classmethod
    def hash(cls, secret, user, realm, encoding=None):
        # NOTE: this was deliberately written so that raw bytes are passed through
        # unchanged, the encoding kwd is only used to handle unicode values.
        if not encoding:
            encoding = cls.default_encoding
        uh.validate_secret(secret)
        if isinstance(secret, unicode):
            secret = secret.encode(encoding)
        user = to_bytes(user, encoding, "user")
        realm = to_bytes(realm, encoding, "realm")
        data = render_bytes("%s:%s:%s", user, realm, secret)
        return hashlib.md5(data).hexdigest()

    @classmethod
    def _norm_hash(cls, hash):
        """normalize hash to native string, and validate it"""
        hash = to_native_str(hash, param="hash")
        if len(hash) != 32:
            raise uh.exc.MalformedHashError(cls, "wrong size")
        for char in hash:
            if char not in uh.LC_HEX_CHARS:
                raise uh.exc.MalformedHashError(cls, "invalid chars in hash")
        return hash

    @classmethod
    def verify(cls, secret, hash, user, realm, encoding="utf-8"):
        hash = cls._norm_hash(hash)
        other = cls.hash(secret, user, realm, encoding)
        return consteq(hash, other)

    @classmethod
    def identify(cls, hash):
        try:
            cls._norm_hash(hash)
        except ValueError:
            return False
        return True

    @uh.deprecated_method(deprecated="1.7", removed="2.0")
    @classmethod
    def genconfig(cls):
        return cls.hash("", "", "")

    @uh.deprecated_method(deprecated="1.7", removed="2.0")
    @classmethod
    def genhash(cls, secret, config, user, realm, encoding=None):
        # NOTE: 'config' is ignored, as this hash has no salting / other configuration.
        #       just have to make sure it's valid.
        cls._norm_hash(config)
        return cls.hash(secret, user, realm, encoding)

#=============================================================================
# eof
#=============================================================================
