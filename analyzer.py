import ast


def analyze_debugging(code):
    result = {
        "syntax_valid": True,
        "syntax_error": None,
        "issues": []
    }

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        result["syntax_valid"] = False
        result["syntax_error"] = {
            "line": e.lineno,
            "message": e.msg
        }
        return result

    for node in ast.walk(tree):

        # Detect empty exception handlers
        if isinstance(node, ast.ExceptHandler):
            if node.body and all(
                isinstance(x, ast.Pass)
                for x in node.body
            ):
                result["issues"].append(
                    "Empty exception handler detected."
                )

        # Detect long functions
        if isinstance(node, ast.FunctionDef):
            if len(node.body) > 20:
                result["issues"].append(
                    f"Function '{node.name}' may be too long."
                )

    return result


def analyze_complexity(code):

    try:
        tree = ast.parse(code)

    except SyntaxError:
        return {
            "complexity": "Unknown",
            "loop_count": 0,
            "max_loop_depth": 0,
            "message": "Cannot analyze complexity because syntax is invalid."
        }

    loop_count = 0
    max_loop_depth = 0

    def visit(node, depth):

        nonlocal loop_count
        nonlocal max_loop_depth

        if isinstance(node, (ast.For, ast.While)):
            loop_count += 1
            depth += 1
            max_loop_depth = max(max_loop_depth, depth)

        for child in ast.iter_child_nodes(node):
            visit(child, depth)

    visit(tree, 0)

    if max_loop_depth == 0:
        complexity = "O(1)"

    elif max_loop_depth == 1:
        complexity = "O(n)"

    elif max_loop_depth == 2:
        complexity = "O(n²)"

    elif max_loop_depth == 3:
        complexity = "O(n³)"

    else:
        complexity = f"O(n^{max_loop_depth})"

    if max_loop_depth == 0:
        message = "No loops detected."

    elif max_loop_depth == 1:
        message = "One loop level detected."

    elif max_loop_depth == 2:
        message = (
            "Nested loops detected. "
            "The code may become slow for large inputs."
        )

    else:
        message = (
            "Deeply nested loops detected. "
            "Consider a more efficient approach."
        )

    return {
        "complexity": complexity,
        "loop_count": loop_count,
        "max_loop_depth": max_loop_depth,
        "message": message
    }


def calculate_scores(debugging, complexity):

    if not debugging["syntax_valid"]:
        debugging_score = 30
    else:
        debugging_score = max(
            100 - len(debugging["issues"]) * 15,
            0
        )

    depth = complexity["max_loop_depth"]

    if depth == 0:
        complexity_score = 100

    elif depth == 1:
        complexity_score = 90

    elif depth == 2:
        complexity_score = 65

    elif depth == 3:
        complexity_score = 40

    else:
        complexity_score = 20

    return debugging_score, complexity_score


def analyze_code(code):

    debugging = analyze_debugging(code)

    complexity = analyze_complexity(code)

    debugging_score, complexity_score = calculate_scores(
        debugging,
        complexity
    )

    return {
        "debugging": debugging,
        "complexity": complexity,
        "debugging_score": debugging_score,
        "complexity_score": complexity_score
    }