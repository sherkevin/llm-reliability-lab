from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from eval_rag import evaluate_citations, evaluate_retrieval, load_jsonl as load_rag
from eval_tool_calls import evaluate as evaluate_tools, load_jsonl as load_tools
from eval_trajectory import evaluate as evaluate_trajectory, load_jsonl as load_trajectories


def test_rag_metrics():
    samples = list(load_rag(ROOT / "data" / "rag_eval_samples.jsonl"))
    metrics = evaluate_retrieval(samples, [1, 3, 5])
    metrics.update(evaluate_citations(samples))
    assert metrics["HitRate@5"] == 1.0
    assert metrics["ClaimSupport"] == 1.0


def test_tool_metrics_detect_unsafe_argument():
    samples = list(load_tools(ROOT / "data" / "tool_call_samples.jsonl"))
    metrics = evaluate_tools(samples)
    assert metrics["ToolSelectionAccuracy"] == 1.0
    assert metrics["UnsafeActionErrors"] == 1


def test_trajectory_metrics_detect_unsafe_step():
    samples = list(load_trajectories(ROOT / "data" / "agent_trajectory_samples.jsonl"))
    metrics = evaluate_trajectory(samples)
    assert metrics["UnsafeToolSteps"] == 1
    assert metrics["ToolOrderAccuracy"] == 1.0
