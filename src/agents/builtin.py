def planner(task):
    return {"agent": "planner", "plan": [f"Understand: {task}", "Validate prerequisites", "Execute safe steps", "Verify result"]}

def researcher(task):
    return {"agent": "researcher", "status": "ready", "task": task}

def architect(task):
    return {"agent": "architect", "status": "ready", "task": task}

def trainer(task):
    return {"agent": "trainer", "status": "ready", "task": task}

def evaluator(task):
    return {"agent": "evaluator", "status": "ready", "task": task}

def optimizer(task):
    return {"agent": "optimizer", "status": "ready", "task": task}

def diagnostics(task):
    return {"agent": "diagnostics", "status": "ready", "task": task}
