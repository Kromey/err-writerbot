import os
import random

from errbot import BotPlugin, botcmd


class WriterBot(BotPlugin):
    """A collection of fun and useful tools for writers."""

    _data = {}

    def activate(self):
        """Triggers on plugin activation"""

        super(WriterBot, self).activate()
        self._load_data_cache()

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

        try:
            mc = args[0].capitalize()
        except IndexError:
            mc = '____'

        return self._get_data('bunnies').format(mc=mc)

    @botcmd
    def plot_ninja(self, msg, args):
        """
        Get a random plot ninja

        Plot ninjas are little things (originally, as the name implies,
        ninjas) that can be found and provide a new twist or hook or
        otherwise get a story moving again.
        """

        return self._get_data('ninjas')

    @botcmd
    def random_profession(self, msg, args):
        """
        Get a random profession
        """

        return self._get_data('professions')

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

        try:
            gender = 'male' if args[0].lower() == 'm' else 'female'
        except IndexError:
            gender = random.choice(('male', 'female'))

        if gender == 'male':
            first = self._get_data('names_boys')
        else:
            first = self._get_data('names_girls')

        if random.randrange(5):
            surname = self._get_data('names_surnames')
        else:
            name1 = self._get_data('names_surnames')
            name2 = self._get_data('names_surnames')

            if name1 == name2:
                #Retry for a different name, but only once
                name2 = self._get_data('names_surnames')

            surname = '-'.join((name1, name2))

        yield "I've picked this {} name just for you:".format(gender)
        yield ' '.join((first, surname))

    @botcmd
    def technobabble(self, msg, args):
        """
        Random technobabble generator

        Now you too can sound just like Geordi LaForge! Now with 100%
        more trans-plasmic shells!
        """

        pattern = self._get_data('techno_patterns')
        fix = self._get_data('techno_fix')
        babble = self._make_babble()
        thing = self._make_babble()
        fails = self._get_data('techno_fails')
        fails2 = self._get_data('techno_fails')

        if fails == fails2:
            #Only retry this once, don't want an infinite loop
            fails2 = self._get_data('techno_fails')

        return pattern.format(fix=fix, babble=babble, thing=thing, fails=fails, fails2=fails2)

    @botcmd
    def divination(self, msg, args):
        """Get a random kind of divination"""

        return "{}mancy".format(self._get_data('mancies'))

    @botcmd
    def diviner(self, msg, args):
        """Get a random kind of divination"""

        return "{}mancer".format(self._get_data('mancies'))

    @botcmd
    def arcanobabble(self, msg, args):
        """
        Random arcanobabble

        Prepare the necromantic psychic mana field!
        """

        pattern = self._get_data('arcano_patterns')
        adj = self._get_data('arcano_babble_adj')
        adj2 = self._get_data('arcano_babble_adj')
        noun = self._get_data('arcano_babble_nouns')
        mancy = self._get_data('mancies')

        if adj == adj2:
            adj2 = self._get_data('arcano_babble_adj')

        return pattern.format(adj=adj, adj2=adj2, noun=noun, mancy=mancy)

    @botcmd(admin_only=True)
    def reload_data(self, msg, args):
        """Reload the cached data files afresh from disk"""

        self._load_data_cache()
        return "Data cache reloaded"

    def _make_babble(self):
        """Helper method to make babble"""

        pattern = self._get_data('techno_babble_patterns')
        location = self._get_data('techno_babble_locations')
        prefix = self._get_data('techno_babble_prefix')
        adj = self._get_data('techno_babble_adj')
        adj2 = self._get_data('techno_babble_adj')
        noun = self._get_data('techno_babble_nouns')

        if adj == adj2:
            #Retry for a different adjective, but only once
            #Don't want an infinite loop
            adj2 = self._get_data('techno_babble_adj')

        return pattern.format(location=location, prefix=prefix, adj=adj, adj2=adj2, noun=noun)

    def _get_data(self, src):
        """Helper method to fetch a random line of data"""

        try:
            return random.choice(self._data[src])
        except KeyError:
            return "Sorry, {} is not one of my data files".format(src)

    def _load_data_cache(self):
        """
        Load the data files into memory.

        The data files are stored in a dictionary in a class member
        to avoid data duplication while improving performance.
        """

        data_dir = os.path.join(
                os.path.realpath(os.path.dirname(__file__)),
                'data'
                )

        #Start with a clean slate
        WriterBot._data = {}

        #Load our data files into memory
        for root, _, files in os.walk(data_dir):
            for filename in files:
                datafile = os.path.join(root, filename)
                basename, _ = os.path.splitext(filename)
                with open(datafile, encoding='utf-8') as fh:
                    WriterBot._data[basename] = [line.strip() for line in fh.readlines()]

