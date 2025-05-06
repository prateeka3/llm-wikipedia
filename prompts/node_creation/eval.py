from inspect_ai import Task, task
from inspect_ai.solver import Generate, Solver, TaskState, solver
from inspect_ai.dataset import Sample
from inspect_ai.scorer import model_graded_qa
from inspect_ai.solver import generate, system_message


# Regex to extract the grade from the model response. Defaults to looking for e.g. GRADE: 4 The regex should have a single capture group that extracts exactly the number (1-5)
GRADE_PATTERN = "GRADE: ([1-5])"


@solver
def event_prompt_template() -> Solver:
    """
    Returns a solve function which modifies the user prompt with the given template.

    Args:
        template : The template string to use to modify the user prompt. Must include {prompt} to be replaced with the original user prompt.

    Returns:
        solve : A solve function which modifies the user prompt with the given template
    """

    with open("./prompt.txt", "r") as f:
        prompt = f.read()

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        state.user_prompt.text = prompt.format(event=state.input_text)
        return state

    return solve


@task
def expand_historical_event():
    def record_to_sample(historical_event: str) -> Sample:
        return Sample(
            input=historical_event,
        )
    
    with open("./historical_events.txt", "r") as f:
        historical_events = f.readlines()
    
    dataset = [record_to_sample(event) for event in historical_events]

    with open("./rubric.txt", "r") as f:
        rubric = f.read()

    return Task(
        dataset=dataset,
        solver=[
            system_message("./system.txt"),
            event_prompt_template(),
            generate()
        ],
        scorer=model_graded_qa(template=rubric, grade_pattern=GRADE_PATTERN),
    )
