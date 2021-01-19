import shutil

from common import (
    chunks_dir,
    pronunciation_dir,
    revised_lesson_count,
    simplified_vocab_lists_dir,
)


def rename_mp3() -> None:
    lesson = str(revised_lesson_count).zfill(2)
    lesson_mp3_dir = pronunciation_dir / lesson
    lesson_chunks_dir = chunks_dir / lesson
    if lesson_mp3_dir.exists():
        shutil.rmtree(lesson_mp3_dir)
    if not lesson_mp3_dir.exists():
        lesson_mp3_dir.mkdir()
    simplified_vocab_list = simplified_vocab_lists_dir / (lesson + ".txt")
    with open(simplified_vocab_list) as f:
        for mp3_path, expression in zip(lesson_chunks_dir.iterdir(), f):
            if expression == "\n":
                # manually add empty lines in simp.txt to skip the corresponding mp3
                # use against "lenshuu C" & "kaiwa", etc
                continue
            new_mp3_name = "MNN_" + expression.rstrip("\n") + ".mp3"
            new_mp3_path = lesson_mp3_dir / new_mp3_name
            mp3_path.link_to(new_mp3_path)
            # argument order of Path.link_to is shit
            # maybe change to Path.rename later


if __name__ == "__main__":
    rename_mp3()
