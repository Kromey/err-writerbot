from errbot import BotPlugin, botcmd
import os
import random

class WriterBot(BotPlugin):
    """A collection of fun and useful tools for writers."""

    _data = {}
    def activate(self):
        """Triggers on plugin activation"""
        super(WriterBot, self).activate()
        data_dir = os.path.join(
                os.path.realpath(os.path.dirname(__file__)),
                'data'
                )
        #Load our data files into memory
        for root, _, files in os.walk(data_dir):
            for filename in files:
                datafile = os.path.join(root, filename)
                basename, _ = os.path.splitext(filename)
                with open(datafile) as f:
                    WriterBot._data[basename] = [l.strip() for l in f.readlines()]

    @botcmd(split_args_with=None)
    def plot_bunny(self, msg, args):
        """
        Get a random plot bunny

        Plot bunnies are short story ideas or hooks that can either spawn
        entire stories themselves, or rescue a story that's hit a wall.

        Optionally may provide the MC's name as an argument, in which case
        the MC will be included in the bunny (if it references the MC), e.g.:
        plot bunny bob
        Bob risks his/her life to rescue someone.
        """
        if args:
            mc = args[0].capitalize()
        else:
            mc = '____'
        return random.choice(self._data['bunnies']).format(mc=mc)

    @botcmd
    def plot_ninja(self, msg, args):
        """
        Get a random plot ninja

        Plot ninjas are little things (originally, as the name implies,
        ninjas) that can be found and provide a new twist or hook or
        otherwise get a story moving again.
        """
        return random.choice(self._data['ninjas'])

    @botcmd
    def random_profession(self, msg, args):
        """
        Get a random profession
        """
        #return random.choice(self._data['professions'])
        return random.choice(self._data['professions'])

    @botcmd
    def random_job(self, msg, args):
        """
        Alias of "random profession"
        """
        return self.random_profession(msg, args)

    @botcmd
    def random_name(self, msg, args):
        """
        Get a random name

        Optionally may provide the desired gender (male/female, man/woman)
        as an argument after the command, e.g. 'random name female'. If no
        gender is requested, one will be selected at random.

        Note that despite the ethnic origins of some names, all names this
        command generates follow the Western (European/North American)
        standard of "First Last". Keep this in mind when using this tool
        to generate names that will be used in other cultures.
        """
        if args:
            gender = 'male' if args[0].lower() == 'm' else 'female'
        else:
            gender = random.choice(('male', 'female'))

        if gender == 'male':
            first = random.choice(self._data['names_boys'])
        else:
            first = random.choice(self._data['names_girls'])

        if random.randrange(5):
            surname = random.choice(self._data['names_surnames'])
        else:
            surname = "{}-{}".format(
                    random.choice(self._data['names_surnames']),
                    random.choice(self._data['names_surnames'])
                    )

        yield "I've picked this {} name just for you:".format(gender)
        yield "{} {}".format(first, surname)

