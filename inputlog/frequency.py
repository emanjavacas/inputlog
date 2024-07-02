
import logging
import math

logger = logging.getLogger(__name__)


WEB1T = 1_024_908_267_229


def safe_log(freq):
    if freq < 1:
        return 0
    return math.log(freq)


def read_freqs(path):
    d = {}
    with open(path) as f:
        for line in f:
            w, freq = line.strip().split()
            d[w] = int(freq)

    result_log, result_rel = {}, {}
    total = sum(d.values())
    for w, freq in d.items():
        logfreq = safe_log(freq * WEB1T / total)
        result_log[w.lower()] = logfreq
        result_rel[w.lower()] = freq / total
    return result_log, result_rel


class Frequency:
    def __init__(self) -> None:
        self.log_freq = {}
        self.rel_freq = {}

    def load(self, settings):
        for language in settings.languages:
            logging.info(
                "Loading frequency data for language '{}' from: {}.".format(
                    language.language, language.freqs_path))
            log_freq, rel_freq = read_freqs(language.freqs_path)
            self.rel_freq[language.language] = rel_freq
            self.log_freq[language.language] = log_freq

    def get_freqs(self, token, lang):
        log_freq = self.log_freq[lang].get(token.lower(), 0)
        rel_freq = self.rel_freq[lang].get(token.lower(), 0)
        return round(log_freq, 4), round(rel_freq, 4)


MODEL = Frequency()
