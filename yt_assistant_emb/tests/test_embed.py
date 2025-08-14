from unittest.mock import MagicMock, patch

from tasks.embed import process_transcript_embedding_logic


@patch("tasks.embed.execute_values")
@patch("tasks.embed.RecursiveCharacterTextSplitter")
def test_process_transcript_embedding_logic(mock_splitter_cls, mock_execute_values):
    # ---------------------- ARRANGE ----------------------

    # Mock cursor and db connection
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (
        "transcript-uuid-1234",
        "Transcript text",
    )
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # Mock text splitter
    mock_splitter = MagicMock()
    mock_splitter.split_text.return_value = ["chunk1", "chunk2"]
    mock_splitter_cls.return_value = mock_splitter

    # Mock embeddings model
    mock_embedding_model = MagicMock()
    mock_embedding_model.embed_documents.return_value = [
        [0.1] * 768,
        [0.2] * 768,
    ]

    video_id = "test-video-1234"

    # ---------------------- ACT -----------------------
    transcript_id, chunk_count = process_transcript_embedding_logic(
        video_id, mock_conn, mock_embedding_model
    )

    # --------------------- ASSERT ---------------------

    # SELECT query called
    assert len(mock_cursor.execute.call_args_list) == 1
    assert mock_cursor.execute.call_args_list[0].args == (
        "SELECT id, transcript_text FROM transcript WHERE video_id = %s",
        (video_id,),
    )

    # Chunks were passed to embeddings
    assert mock_embedding_model.embed_documents.call_count == 1
    assert mock_embedding_model.embed_documents.call_args[0][0] == ["chunk1", "chunk2"]

    # execute_values called for chunks insert and for embeddings insert
    assert len(mock_execute_values.call_args_list) == 2
    assert any(
        "INSERT INTO transcript_chunk" in call.args[1]
        for call in mock_execute_values.call_args_list
    )
    assert any(
        "INSERT INTO embedding" in call.args[1]
        for call in mock_execute_values.call_args_list
    )
    # commit called
    assert mock_conn.commit.call_count == 1

    # Function returns correct transcript_id and chunk_count
    assert transcript_id == "transcript-uuid-1234"
    assert chunk_count == 2
