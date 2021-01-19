import shutil

from common import chunks_dir, pronunciation_dir, simplified_vocab_lists_dir

lesson = "01"


def rename_mp3() -> None:
    if pronunciation_dir.exists():
        shutil.rmtree(pronunciation_dir)
    if not pronunciation_dir.exists():
        pronunciation_dir.mkdir()
    simplified_vocab_list = simplified_vocab_lists_dir / (lesson + ".txt")
    with open(simplified_vocab_list) as f:
        for mp3_path, expression in zip(chunks_dir.iterdir(), f):
            new_mp3_name = "MNN_" + expression.rstrip("\n") + ".mp3"
            new_mp3_path = pronunciation_dir / new_mp3_name
            mp3_path.link_to(new_mp3_path)
            # argument order of Path.link_to is shit
            # maybe change to Path.rename later


if __name__ == "__main__":
    rename_mp3()
