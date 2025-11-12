"""
AmpBox: Integrated Runtime for AI Agents

Minimal proof-of-concept - zero external dependencies beyond Amplifier@next.
Philosophy: Start simple, add complexity only when simplicity fails.
"""

from ampbox.workflow import SimpleWorkflow
from ampbox.workflow import WorkflowState

__all__ = ["SimpleWorkflow", "WorkflowState"]
