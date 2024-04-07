class Const:
    """
    A partial constant expression, like "7", "7.", "7.8", or "". The
    latter case means a number has not yet been input.
    """

    def __init__(self, value, closed=False):
        self.value = value
        # Closed means this expression can no longer be added
        # to. Further calculator input will start off a new
        # expression. Expressions are closed when clicking "=" in the
        # calculator.
        self.closed = closed


class Node:
    """
    A binary expression.

    7 + 8 is represented as Node("+", left=Const("7"), right=Const("8"))

    7 + 8 * 5 is represented as:

    Node(
        "+",
        left=Const("7"),
        right=Node(
            "*",
            left=Const("8"),
            right=Const("5")
        )
    )
    """

    def __init__(self, op, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right


def to_number(v):
    """
    Returns an int if a given float is whole. to_number(7.0) will return 7.
    """
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return v


def eval_expr(expr):
    """
    Evaluates an expression to a number.

    We take some liberties here:

    - If the expression is partial (current nuber not yet input, like
      "7 + _", we treat the "_" as zero.
    - Division by zero is evaluated to zero.
    """
    if isinstance(expr, Const):
        if expr.value == "":
            expr.value = 0
        return to_number(float(expr.value))
    if expr.op == "/":
        try:
            return to_number(eval_expr(expr.left) / eval_expr(expr.right))
        except ZeroDivisionError:
            return 0
    if expr.op == "*":
        return to_number(eval_expr(expr.left) * eval_expr(expr.right))
    if expr.op == "-":
        return to_number(eval_expr(expr.left) - eval_expr(expr.right))
    if expr.op == "+":
        return to_number(eval_expr(expr.left) + eval_expr(expr.right))


def process_numeric_input(expr, x):
    """
    Generates an updated expression given a number input or "."
    """
    if isinstance(expr, Const):
        if expr.closed:
            value = "0"
        else:
            value = expr.value
        if x == "." and "." in value:
            return Const(value)
        if value == "0" and x != ".":
            return Const(x)
        return Const(value + x)
    else:
        return Node(expr.op, expr.left, process_numeric_input(expr.right, x))


def process_operator(expr, op):
    """Expr can be either:

    - a const like "15"
    - an expression like "8 + 5" or "8 + _" (right hand side not yet input)
    - an expression like "8 + 7 * 9" with a not yet evaluated
      multiplication or division on the right side, or "8 - 7 / _"
      (right hand side of the inner division/multiplication not yet
      input)

    """
    if op == "=":
        return Const(str(eval_expr(expr)), closed=True)

    if isinstance(expr, Const):
        return Node(op, left=expr, right=Const(""))

    # If the user clicks an operator button and there is a dangling
    # expression on the right hand side (right hand side has not yet
    # been input), the click is ignored, because clicking multiple
    # operators in a row doesn't make sense. Other behaviors are
    # possible here.
    if (
        isinstance(expr.right, Node)
        and expr.right.right.value == ""
        or isinstance(expr.right, Const)
        and expr.right.value == ""
    ):
        return expr

    if expr.op in ("+", "-") and op in ("/", "*"):
        # The top-level expression is a +/- and we are inputting a
        # division/multiplication with a higher precedence.

        # In this case we create a sub-node on the right for the new
        # operator, and place the expression currently on the right in
        # the left child of the new node.
        return Node(
            expr.op,
            left=expr.left,
            right=Node(
                op,
                left=Const(str(eval_expr(expr.right))),
                right=Const(""),
            ),
        )

    # In this case there is no operator precedence (the top-level node
    # matches the precedence of the new operator), so we evaluate the
    # top-level node and put the result in the left child of the new
    # node.
    return Node(op, left=Const(str(eval_expr(expr))), right=Const(""))


def render_output(expr):
    """
    Renders the "current number" to be displayed in the calculator's
    main display.

    This is the rightmost node in the tree, unless that node is blank
    (not yet input) in which case we render its left sibling.
    """
    while True:
        if isinstance(expr, Node):
            if isinstance(expr.right, Const):
                if expr.right.value == "":
                    return expr.left.value
                else:
                    return expr.right.value
            else:
                expr = expr.right
        elif isinstance(expr, Const):
            return expr.value


def render_expr(expr):
    """
    Inorder string rendering of the expression, to print in the
    secondary display of the calculator.
    """
    if not expr:
        return ""
    if isinstance(expr, Const):
        return expr.value
    else:
        return render_expr(expr.left) + " " + expr.op + " " + render_expr(expr.right)
