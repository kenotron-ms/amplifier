"""
Simple workflow orchestrator for AmpBox POC.

Zero dependencies beyond Python stdlib - proves the concept before adding complexity.
If this becomes too complex, THEN we add LangGraph. Not before.
"""

import json
from collections.abc import Awaitable
from collections.abc import Callable
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class WorkflowState:
    """
    State container that passes between workflow steps.

    Simple dict wrapper with convenience methods.
    """

    data: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from state"""
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set value in state"""
        self.data[key] = value

    def to_dict(self) -> dict[str, Any]:
        """Export state as dict"""
        return self.data.copy()


class SimpleWorkflow:
    """
    Minimal workflow orchestrator.

    Runs Python functions (deterministic or agentic) in sequence.
    Saves state after each step for resumability.

    No external dependencies. No complex graph logic. Just sequential execution
    with state passing. If we need branching/parallelism later, add it then.
    """

    def __init__(self, name: str, state_dir: Path | None = None):
        """
        Initialize workflow.

        Args:
            name: Workflow identifier
            state_dir: Where to save state (default: .ampbox_state)
        """
        self.name = name
        self.state_dir = state_dir or Path(".ampbox_state")
        self.state_dir.mkdir(exist_ok=True, parents=True)
        self.steps: list[tuple[str, Callable[[WorkflowState], Awaitable[None]]]] = []

    def add_step(self, name: str, func: Callable[[WorkflowState], Awaitable[None]]) -> None:
        """
        Add a workflow step.

        Step can be deterministic (simple transformation) or agentic (calls AI).

        Args:
            name: Step identifier
            func: Async function that takes WorkflowState and modifies it
        """
        self.steps.append((name, func))

    async def run(self, initial_state: dict[str, Any] | None = None) -> WorkflowState:
        """
        Execute workflow steps in sequence.

        State is saved after each step for resumability.

        Args:
            initial_state: Starting state dict (optional)

        Returns:
            Final workflow state
        """
        state = WorkflowState(data=initial_state or {})

        # Add metadata
        state.set("_workflow_name", self.name)
        state.set("_started_at", datetime.now().isoformat())

        print(f"\n🚀 Starting workflow: {self.name}")
        print(f"   Steps: {len(self.steps)}")
        print()

        for i, (step_name, step_func) in enumerate(self.steps, 1):
            print(f"→ Step {i}/{len(self.steps)}: {step_name}")

            try:
                # Execute step
                await step_func(state)

                # Save state after each step
                self._save_state(state, step_name)

                print("  ✓ Complete\n")

            except Exception as e:
                print(f"  ✗ Error: {e}\n")
                state.set(f"_error_{step_name}", str(e))
                self._save_state(state, f"{step_name}_ERROR")
                raise

        # Mark workflow complete
        state.set("_completed_at", datetime.now().isoformat())
        self._save_state(state, "COMPLETE")

        print(f"✅ Workflow complete: {self.name}\n")
        return state

    def _save_state(self, state: WorkflowState, checkpoint: str) -> None:
        """
        Save workflow state to JSON file.

        Creates checkpoint for resumability and debugging.

        Args:
            state: Current state
            checkpoint: Checkpoint name (step name or status)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.name}_{timestamp}_{checkpoint}.json"
        state_file = self.state_dir / filename

        # Save state
        with open(state_file, "w") as f:
            json.dump(state.to_dict(), f, indent=2, default=str)

        # Also save as "latest" for easy access
        latest_file = self.state_dir / f"{self.name}_latest.json"
        with open(latest_file, "w") as f:
            json.dump(state.to_dict(), f, indent=2, default=str)
