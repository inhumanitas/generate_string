# coding: utf-8

import random
import string


def string_generator(max_value=10):
    return random.randint(0, max_value)


def int_generator(max_value=10):
    return ''.join(
        random.choice(string.ascii_letters) for _ in range(max_value))


generator_modes = {
    's': string_generator,
    'i': int_generator,
}


class Generator:

    def __init__(self) -> None:
        super().__init__()
        self._generators = []

    @property
    def generators(self):
        return self._generators

    def add_mode(self, mode):
        assert mode in generator_modes
        self._generators.append(generator_modes[mode])

    def generate(self):
        return ''.join([str(cur_g()) for cur_g in self.generators])


def random_value(modes='si'):
    generator = Generator()
    for _mode in generator_modes:
        if _mode in modes:
            generator.add_mode(_mode)

    return generator.generate()
