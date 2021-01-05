from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class IrcamAuthAccount(ProviderAccount):
    pass

class IrcamAuthProvider(OAuth2Provider):
    id = 'ircamauth'
    name = 'Ircam Auth'
    account_class = IrcamAuthAccount

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        return dict(username=data['username'],
                    email=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    avatar=data['avatar'],
                    )

    def get_default_scope(self):
        scope = ['read']
        return scope

    def get_avatar_url(self):
        return self.account.extra_data.get('avatar')

        
providers.registry.register(IrcamAuthProvider)
