from . import config


class GamePlayer():
    def __init__(self, user: config.UserType, **options) -> None:
        self.user = user
        self.winner = False
        for k, v in options.items():
            assert(getattr(self, k, None) == None)
            setattr(self, k, v)

    @property
    def name(self):
        return self.user.display_name

    @property
    def full_name(self):
        return f"{self.user.name}#{self.user.discriminator}"

    @property
    def mention(self):
        return "<@!{}>".format(self.user.id)

    def __str__(self) -> str:
        return "{} (ID{})".format(self.full_name, str(self.user.id))

    def __eq__(self, other) -> bool:
        if isinstance(other, GamePlayer):
            return self.user == other.user
        return self.user == other