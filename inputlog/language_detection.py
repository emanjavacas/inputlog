
import logging
from lingua import Language, LanguageDetectorBuilder, IsoCode639_1

logger = logging.getLogger(__name__)


def get_language_from_code(code):
    return Language.from_iso_code_639_1(getattr(IsoCode639_1, code.upper()))


class LanguageDetector:
    def __init__(self) -> None:
        self.detector = None

    def detect_language(self, sentence):
        detected = self.detector.detect_language_of(sentence)
        if detected is not None:
            return detected.iso_code_639_1.name.lower()

    def load(self, settings):
        logger.info("Loading language detection systems ...")
        self.detector = LanguageDetectorBuilder.from_languages(
            *[get_language_from_code(language.language) for language in settings.languages]
        ).build()
        logger.info("...language detection system loaded")


MODEL = LanguageDetector()