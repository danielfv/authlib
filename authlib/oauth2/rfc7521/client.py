from authlib.common.encoding import to_native


class AssertionClient(object):
    """Constructs a new Assertion Framework for OAuth 2.0 Authorization Grants
    per RFC7521_.

    .. _RFC7521: https://tools.ietf.org/html/rfc7521
    """
    DEFAULT_GRANT_TYPE = None
    ASSERTION_METHODS = {}
    token_auth_class = None

    def __init__(self, session, token_url, issuer, subject, audience,
                 grant_type=None, claims=None, token_placement='header',
                 scope=None, **kwargs):

        self.session = session
        self.token_url = token_url

        if grant_type is None:
            grant_type = self.DEFAULT_GRANT_TYPE
        self.grant_type = grant_type

        # https://tools.ietf.org/html/rfc7521#section-5.1
        self.issuer = issuer
        self.subject = subject
        self.audience = audience
        self.claims = claims
        self.scope = scope
        if self.token_auth_class is not None:
            self.token_auth = self.token_auth_class(None, token_placement, self)
        self._kwargs = kwargs

    @property
    def token(self):
        return self.token_auth.token

    @token.setter
    def token(self, token):
        self.token_auth.set_token(token)

    def refresh_token(self):
        """Using Assertions as Authorization Grants to refresh token as
        described in `Section 4.1`_.

        .. _`Section 4.1`: https://tools.ietf.org/html/rfc7521#section-4.1
        """
        generate_assertion = self.ASSERTION_METHODS[self.grant_type]
        assertion = generate_assertion(
            issuer=self.issuer,
            subject=self.subject,
            audience=self.audience,
            claims=self.claims,
            **self._kwargs
        )
        data = {
            'assertion': to_native(assertion),
            'grant_type': self.grant_type,
        }
        if self.scope:
            data['scope'] = self.scope

        return self._refresh_token(data)

    def _refresh_token(self, data):
        resp = self.session.post(
            self.token_url, data=data, withhold_token=True)
        self.token = resp.json()
        return self.token
