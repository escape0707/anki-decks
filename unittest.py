from create_new_vocab import extract_expressions
from utils import furigana_to_kanji

if __name__ == "__main__":
    print(*extract_expressions("あの人（あの方）"))
    print(furigana_to_kanji("「どうぞ」よろしく「お 願[ねが]いします」。"))
    print(furigana_to_kanji(" 研[けん] 究[きゅう] 者[しゃ]"))
