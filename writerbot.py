import os
import random
import re

from errbot import BotPlugin, botcmd, re_botcmd


class WriterBot(BotPlugin):
    """A collection of fun and useful tools for writers."""

    _data = {}

    def activate(self):
        """Triggers on plugin activation"""

        super(WriterBot, self).activate()
        self._load_data_cache()

    @botcmd(hidden=True, split_args_with=None)
    def bunny(self, msg, args):
        return self.plot_bunny(msg, args)

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

    @botcmd(hidden=True)
    def ninja(self, msg, args):
        return self.plot_ninja(msg, args)

    @botcmd
    def plot_ninja(self, msg, args):
        """
        Get a random plot ninja

        Plot ninjas are little things (originally, as the name implies,
        ninjas) that can be found and provide a new twist or hook or
        otherwise get a story moving again.
        """
        ninja = self._get_data('ninjas')

        if ninja == '<roll the writers dice>':
            return self.writers_dice(msg, args)
        else:
            return ninja

    @botcmd(hidden=True)
    def profession(self, msg, args):
        return self.random_profession(msg, args)

    @botcmd
    def random_profession(self, msg, args):
        """
        Get a random profession
        """

        return self._get_data('professions')

    @botcmd(hidden=True)
    def job(self, msg, args):
        return self.random_profession(msg, args)

    @botcmd
    def random_job(self, msg, args):
        """
        Alias of "random profession"
        """

        return self.random_profession(msg, args)

    @botcmd(hidden=True)
    def hobby(self, msg, args):
        return self.random_hobby(msg, args)

    @botcmd
    def random_hobby(self, msg, args):
        """
        Get a random hobby
        """

        return self._get_data('hobbies')

    @botcmd(hidden=True)
    def hobbies(self, msg, args):
        return self.random_hobbies(msg, args)

    @botcmd
    def random_hobbies(self, msg, args):
        """
        Get a list of random hobbies
        """
        try:
            num = int(args)
        except:
            num = 5

        return "What about {}".format(
                ', '.join(self._get_data('hobbies', num)),
                )

    _writers_dice = [
            ['Fish', 'Bird', 'Wizard', 'Robot', 'Dragon', 'Bug'],
            ['Guys', 'Ladies', 'Kids', 'Lizards', 'Ghosts', 'Plants'],
            ]
    @botcmd
    def writers_dice(self, msg, args):
        """
        Roll the famous Writer's Dice

        As seen in Penny Arcade: https://www.penny-arcade.com/comic/2016/11/09/the-cubes-win
        """

        return "{} {}".format(
                random.choice(self._writers_dice[0]),
                random.choice(self._writers_dice[1]),
                )

    @botcmd(hidden=True)
    def writer_dice(self, msg, args):
        return self.writers_dice(msg, args)

    _name_responses = (
            "Here's a good {gender} name: {first} {surname}",
            "I once met a {gender} named {first} {surname}",
            "Species {num} was fond of {first} {surname} for their {gender} children",
            "How about {first} {surname}?",
            )
    @re_botcmd(pattern=r'\bname\b', flags=re.IGNORECASE)
    def random_name(self, msg, match):
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

        body = msg.body.lower().split(None)
        if 'female' in body or 'woman' in body:
            gender = 'female'
        elif 'male' in body or 'man' in body:
            gender = 'male'
        else:
            gender = random.choice(('male', 'female'))

        if gender == 'male':
            first = self._get_data('names_boys')
        else:
            first = self._get_data('names_girls')

        surname = self._get_surname()

        return random.choice(self._name_responses).format(gender=gender, first=first, surname=surname, num=random.randrange(2378,7890))

    @botcmd
    def surname(self, msg, args):
        surname = self._get_surname()

        return "How about {surname}?".format(surname=surname)

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
        fails, fails2 = self._get_data('techno_fails', 2)

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
        adj, adj2 = self._get_data('arcano_babble_adj', 2)
        noun = self._get_data('arcano_babble_nouns')
        mancy = self._get_data('mancies')

        return pattern.format(adj=adj, adj2=adj2, noun=noun, mancy=mancy)

    @botcmd
    def not_said(self, msg, args):
        """
        Get some suggestions for words to use instead of "said".

        From the list by Steven P. Wickstrom (http://www.spwickstrom.com/said/)
        """
        words = self._get_data('said', 5)

        return "Try {}".format(', '.join(words))


    @botcmd(admin_only=True)
    def reload_data(self, msg, args):
        """Reload the cached data files afresh from disk"""

        self._load_data_cache()
        return "Data cache reloaded"

    def _get_surname(self):
        if random.randrange(5):
            surname = self._get_data('names_surnames')
        else:
            #Hyphenate
            surname = '-'.join(self._get_data('names_surnames', 2))

        return surname

    def _make_babble(self):
        """Helper method to make babble"""

        pattern = self._get_data('techno_babble_patterns')
        location = self._get_data('techno_babble_locations')
        prefix = self._get_data('techno_babble_prefix')
        adj, adj2 = self._get_data('techno_babble_adj', 2)
        noun = self._get_data('techno_babble_nouns')

        return pattern.format(location=location, prefix=prefix, adj=adj, adj2=adj2, noun=noun)

    def _get_data(self, src, count=1):
        """Helper method to fetch a random line of data"""

        try:
            if count == 1:
                return random.choice(self._data[src])
            else:
                return random.sample(self._data[src], count)
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

