from . import config


class GamePlayer():
    def __init__(self, user: config.UserType, **options) -> None:
        self.user = user
        for k, v in options.items():
            assert(getattr(self, k, None) == None)
            setattr(self, k, v)

    @property
    def name(self):
        return self.user.display_name

    @property
    def mention(self):
        return "<@!{}>".format(self.user.id)

    def __str__(self) -> str:
        return "{}#{} (ID{})".format(self.user.name, self.user.discriminator, str(self.user.id))
