# Getting started
This project is set up using [uv](https://docs.astral.sh/uv/guides/projects/#next-steps)
```
uv venv
source .venv/bin/activate
uv pip install -e .
```

# Dev Roadmap
- set up prompt, rubric, and Task for iteratively improving the fit node generator and evaluator (same as rubric but with feedback)
    - maybe need a way to judge the feedback itself?
    - follow the template files in `prompts/node_creation`
- set up prompt, rubric, and Task for iteratively improving the expand node generator and evaluator (same as rubric but with feedback)
    - need a way to judge the feedback itself


# Improving the prompts
Each prompt has its own folder in `/prompts`. In that folder you'll see:
- `eval.py` - describes the evaluation Task that generates, scores, and gives feedback for a prompt
- `*.txt`   - prompt files. 
Run the appropriate Task determined in the python file to run the eval for the defined prompt. Based on the results and some manual checking, you can iterate on the prompts themselves:
- bad results and high score -> make the rubric more discerning
- bad results and low score -> tighten up the original or system prompt
- good results and low score -> make the rubric more permissive

```
inspect eval prompts/node_creation/eval.py --model openai/gpt-4
```

# Design
- llm_workflow:
    - create node
        - enter historical event
        - add node [step 1 in a prompt chain]
            - format title to standard Wikipedia type title
            - add a short 1 paragraph description
        - fit node [step 2 in prompt chain - generator-evaluator]
            - read entire graph
            - generator: given existing nodes, where does this plug in, if at all?
            - evaluator: check if the new causal flow makes sense
    - expand node
        - assume graph is in good form before
        - given node with title and description
        - read entire graph
        - generator: how would you break down this node into separate parallel steps, sequence, or both?
        - evaluator: new causal flow makes sense, not "too granular", no information overlap between nodes
- process for writing and improving prompts
    - evaluation datasets:
        - for add node: historical event name
        - for fit node: historical event title, description, current graph state
        - for expansion: historical event title, description, current graph state
    - rubric for each prompt
    - few shot examples in the prompt?
    - create and run a task for grading the outputs based on a rubric
