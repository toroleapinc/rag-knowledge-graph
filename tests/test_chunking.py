from ragkg.ingest import chunk_text

def test_chunk_basic():
    text = " ".join(["word"] * 1000)
    chunks = chunk_text(text, chunk_size=100, overlap=10)
    assert len(chunks) > 1
    assert len(chunks[0].split()) == 100

def test_chunk_short_text():
    chunks = chunk_text("short text", chunk_size=100)
    assert len(chunks) == 1
