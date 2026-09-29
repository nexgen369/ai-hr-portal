from scripts.ingest import chunks

def test_chunks_cover_text():
    text = "abcdefghijklmnopqrstuvwxyz"
    result = list(chunks(text, size=10, overlap=2))
    assert "".join(result).replace(" ", "")  # basic non-empty chunk check
    assert result[0] == "abcdefghij"
    assert result[1].startswith("ij")

def test_overlap_must_be_smaller_than_size():
    try:
        list(chunks("hello", size=5, overlap=5))
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError"
