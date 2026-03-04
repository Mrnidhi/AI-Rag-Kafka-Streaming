import pytest
from unittest.mock import patch, MagicMock
import numpy as np


def test_embed_returns_list():
    with patch("app.services.embedder.SentenceTransformer") as mock_st:
        mock_model = MagicMock()
        mock_model.encode.return_value = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
        mock_st.return_value = mock_model

        from app.services.embedder import EmbeddingService

        svc = EmbeddingService()
        svc._model = mock_model

        result = svc.embed(["hello", "world"])

        assert len(result) == 2
        assert len(result[0]) == 3
        assert isinstance(result[0][0], float)


def test_embed_single():
    with patch("app.services.embedder.SentenceTransformer") as mock_st:
        mock_model = MagicMock()
        mock_model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        mock_st.return_value = mock_model

        from app.services.embedder import EmbeddingService

        svc = EmbeddingService()
        svc._model = mock_model

        result = svc.embed_single("hello")

        assert len(result) == 3
