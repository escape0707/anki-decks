from pathlib import Path

data_dir = Path("./data")

chunks_dir = data_dir / "chunks"
input_file = next((data_dir / "input").iterdir())
vocab_list_file = data_dir / "vocab_list.txt"
pronunciation_dir = data_dir / "pronunciation"
word_count_file = data_dir / "processed_word_count_cache.txt"
new_word_count_file = word_count_file.with_stem("new_" + word_count_file.stem)
new_vocab_lists_dir = data_dir / "new_vocab_lists"
lesson = "第" + input_file.stem[5:-3] + "課"
