# RAG Evaluation with RAGAS

Automated evaluation harness using RAGAS framework.

## Metrics Tracked
- **Faithfulness**: Answer grounded in retrieved context
- **Answer Relevance**: Response relevance to question
- **Context Precision**: Quality of retrieved chunks
- **Context Recall**: Coverage of necessary information
- **Hallucination Rate**: Factual accuracy

## Running Evaluation
```bash
cd eval/ragas
pip install -r requirements.txt
python run_eval.py
```

## Golden Dataset
Located in `/data/golden-dataset/`:
- `qa_pairs.json` - Ground truth Q&A
- `expected_sources.json` - Expected retrieval docs

Format:
```json
{
  "questions": [
    {
      "id": "q1",
      "question": "What is RAG?",
      "expected_answer": "Retrieval-Augmented Generation...",
      "expected_sources": ["doc1", "doc2"]
    }
  ]
}
```

## Reports
Results saved to `eval/ragas/reports/`:
- `latest_eval.json` - Latest run results
- `trends.csv` - Historical trends
- `dashboard.html` - Visual report

## Target Benchmarks
- Faithfulness: > 0.90
- Answer Relevance: > 0.85
- Context Precision: > 0.80
- Hallucination Rate: < 3%
