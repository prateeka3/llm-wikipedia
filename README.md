# Getting started
This project is set up using [uv](https://docs.astral.sh/uv/guides/projects/#next-steps)
```
uv venv
source .venv/bin/activate
uv pip install -e .
```

# Dev Roadmap
- set up prompt, rubric, and Task for iteratively improving the fit node generator and evaluator (same as rubric but with feedback)
    - follow the template files in `prompts/node_creation`
    - at first, we will focus on improving the generator via the rubric. If the generator itself is able to get to a good spot, then this can just be a single prompt. otherwise, we'll need to loop between generating, evaluating, and generating again based on the feedback. I want to be able to fix the number of these loops and test how much improvement we get per loop on average.
- set up prompt, rubric, and Task for iteratively improving the expand node generator and evaluator (same as rubric but with feedback)
    - same as above, more likely to need multiple generator-evaluator loops


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
        - for add node: list of historical event names `historical_events.txt`
        - for fit node: historical event title, description, current graph state
            - use the prompt in node_creation to generate title and descriptions. might need some some prompts to generate the graph state part of this dataset
        - for expansion: historical event title, description, current graph state
            - use the prompt in node_creation to generate title and descriptions. might need some some prompts to generate the graph state part of this dataset
    - rubric for each prompt
    - few shot examples in the prompt if necessary
    - chain of thought in the prompt if necessary
    - create and run a task for grading the outputs based on a rubric
- see simple_viz for a simple visualization of the graph object

# Future Features
- Graph Verification: use the internet to find sources that verify each node/link
- Async Expansion: recursively run the expansion on nodes to generate a large graph
- Disputing System Roles: allow the user to change the system role from "accurate to historian" to "stubborn conspiracy theorist" or similar. compare graphs of the same event for each