import urlparse

from netloc import Netloc
from ports import DEFAULT_PORTS
from query_string import QueryString


class URLObject(unicode):

    """
    A URL.

    This class contains properties and methods for accessing and modifying the
    constituent components of a URL. :class:`URLObject` instances are
    immutable, as they derive from the built-in ``unicode``, and therefore all
    methods return *new* objects; you need to consider this when using
    :class:`URLObject` in your own code.
    """

    def __repr__(self):
        return 'URLObject(%r)' % (unicode(self),)

    @property
    def scheme(self):
        return urlparse.urlsplit(self).scheme
    def with_scheme(self, scheme):
        return self.__replace(scheme=scheme)

    @property
    def netloc(self):
        return Netloc(urlparse.urlsplit(self).netloc)
    def with_netloc(self, netloc):
        return self.__replace(netloc=netloc)

    @property
    def username(self):
        return self.netloc.username
    def with_username(self, username):
        return self.with_netloc(self.netloc.with_username(username))
    def without_username(self):
        return self.with_netloc(self.netloc.without_username())

    @property
    def password(self):
        return self.netloc.password
    def with_password(self, password):
        return self.with_netloc(self.netloc.with_password(password))
    def without_password(self):
        return self.with_netloc(self.netloc.without_password())

    @property
    def hostname(self):
        return self.netloc.hostname
    def with_hostname(self, hostname):
        return self.with_netloc(self.netloc.with_hostname(hostname))
    def without_hostname(self):
        return self.with_netloc(self.netloc.without_hostname())

    @property
    def port(self):
        return self.netloc.port
    def with_port(self, port):
        return self.with_netloc(self.netloc.with_port(port))
    def without_port(self):
        return self.with_netloc(self.netloc.without_port())

    @property
    def auth(self):
        return self.netloc.auth
    def with_auth(self, *auth):
        return self.with_netloc(self.netloc.with_auth(*auth))
    def without_auth(self):
        return self.with_netloc(self.netloc.without_auth())

    @property
    def default_port(self):
        """
        The destination port number for this URL.

        If no port number is explicitly given in the URL, this will return the
        default port number for the scheme if one is known, or ``None``. The
        mapping of schemes to default ports is defined in
        :const:`urlobject.ports.DEFAULT_PORTS`.
        """
        port = urlparse.urlsplit(self).port
        if port is not None:
            return port
        return DEFAULT_PORTS.get(self.scheme)

    @property
    def path(self):
        return urlparse.urlsplit(self).path
    def with_path(self, path):
        return self.__replace(path=path)

    @property
    def query(self):
        return QueryString(urlparse.urlsplit(self).query)
    def with_query(self, query):
        return self.__replace(query=query)
    def without_query(self):
        return self.__replace(query='')

    @property
    def fragment(self):
        return urlparse.urlsplit(self).fragment
    def with_fragment(self, fragment):
        return self.__replace(fragment=fragment)
    def without_fragment(self):
        return self.__replace(fragment='')

    def __replace(self, **replace):
        """Replace a field in the ``urlparse.SplitResult`` for this URL."""
        return type(self)(urlparse.urlunsplit(
            urlparse.urlsplit(self)._replace(**replace)))
