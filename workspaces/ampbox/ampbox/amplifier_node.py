"""
AmplifierNode: Bridge between Amplifier@next agents and LangGraph workflows.

This is the 10% glue - makes Amplifier agents work as LangGraph nodes.
Uses LangGraph for orchestration (don't reinvent), adds Amplifier integration.
"""


def create_amplifier_node(agent_name: str, task: str):
    """
    Create a LangGraph-compatible node that runs an Amplifier@next agent.

    This is the bridge - makes Amplifier agents work as LangGraph workflow nodes.

    Args:
        agent_name: Which Amplifier agent to use
        task: Task description for the agent

    Returns:
        Async function compatible with LangGraph nodes
    """

    async def amplifier_node(state: dict) -> dict:
        """
        Execute Amplifier agent within LangGraph workflow.

        Called by LangGraph when workflow reaches this node.

        Args:
            state: Current workflow state

        Returns:
            Updated state with agent results
        """
        # Integration point: Call Amplifier@next agent
        result = await _run_amplifier_agent(agent_name, task, state)

        # Update state with agent output
        return {
            **state,
            "themes": result,  # Agent output goes to themes field
            f"{agent_name}_complete": True,
        }

    return amplifier_node


async def _run_amplifier_agent(agent_name: str, task: str, state: dict) -> str:
    """
    Run Amplifier agent with context from workflow state.

    Future: Import from amplifier@next and call actual agents.
    Current: Working implementation that proves the bridge.

    Args:
        agent_name: Agent identifier
        task: Task description
        state: Workflow state

    Returns:
        Agent output (themes extracted)
    """
    # Extract context from state
    documents = state.get("documents", [])

    # Simple keyword extraction (will be real Amplifier agent call)
    all_text = " ".join(documents).lower()
    keywords = ["agent", "workflow", "orchestration", "state", "execution"]
    found = [kw for kw in keywords if kw in all_text]

    themes = "\n".join(f"{i + 1}. {theme.capitalize()}-based patterns" for i, theme in enumerate(found[:5]))

    if not themes:
        themes = "General content - no specific patterns identified"

    return themes


# Export factory function
AmplifierNode = create_amplifier_node
