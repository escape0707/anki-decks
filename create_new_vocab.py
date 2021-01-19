from common import new_vocab_list_file, vocab_list_file
from utils import extract_expressions


def create_new_vocab() -> None:
    with open(vocab_list_file) as in_f, open(new_vocab_list_file, "w") as out_f:
        for index, note in enumerate(in_f, 1):
            field_collection = note.split("\t")
            tag_field = field_collection.pop()  # end with an redundant "\n"
            expression_collection = extract_expressions(field_collection[0])
            index_field = str(index)
            audio_field = "".join(
                map(lambda x: f"[sound:MNN_{x}.mp3]", expression_collection)
            )
            new_note = "\t".join(
                [index_field] + field_collection + [audio_field, tag_field]
            )
            out_f.write(new_note)


if __name__ == "__main__":
    create_new_vocab()
