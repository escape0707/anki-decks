from pathlib import Path

data_dir = Path("./data")
revised_lesson_count = 44

chunks_dir = data_dir / "chunks"
input_dir = data_dir / "input"
vocab_list_file = data_dir / "vocab_list.txt"
new_vocab_list_file = vocab_list_file.with_stem("new_" + vocab_list_file.stem)
pronunciation_dir = data_dir / "pronunciation"
simplified_vocab_lists_dir = data_dir / "simplified_vocab_lists"
