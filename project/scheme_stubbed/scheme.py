"""A Scheme interpreter and its read-eval-print loop."""
from __future__ import print_function
from ast import expr  # Python 2 compatibility

import sys
import os

from scheme_builtins import *
from scheme_reader import *
from ucb import main, trace
import re


##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in environment ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # PROBLEM 2
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr
    if not scheme_listp(expr):
        raise SchemeError("syntax error", repr(expr))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in SPECIAL_FORMS:
        return SPECIAL_FORMS[first](rest, env)
    else:
        res = expr.map(lambda s: scheme_eval(s, env))
        return scheme_apply(res.first, res.rest, env)


def self_evaluating(expr):

    return (scheme_atomp(expr)) and not scheme_symbolp(expr) or expr is None


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    environment ENV."""
    # PROBLEM 2
    validate_procedure(procedure)
    if isinstance(procedure, BuiltinProcedure):
        return procedure.apply(args, env)

    if isinstance(procedure, LambdaProcedure):
        return procedure.apply(args, env)


################
# Environments #
################


class Frame(object):
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None)."""
        "Your Code Here"
        # Note: you should define instance variables self.parent and self.bindings
        self.parent = parent
        self.bindings = {}

    def __repr__(self):
        if self.parent is None:
            return "<Global Frame>"
        s = sorted(["{0}: {1}".format(k, v) for k, v in self.bindings.items()])
        return "<{{{0}}} -> {1}>".format(", ".join(s), repr(self.parent))

    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE."""
        self.bindings[symbol] = value

    def lookup(self, symbol):
        if self.bindings and symbol in self.bindings:
            return self.bindings[symbol]
        elif self.parent:
            return self.parent.lookup(symbol)
        else:
            raise SchemeError("{} is not defined".format(symbol))

    # BEGIN PROBLEM 2/3
    "*** YOUR CODE HERE ***"

    def make_child_frame(self, formals, vals):
        if len(formals) != len(vals):
            raise TypeError("incorrect number of arguments")
        child_env = Frame(self)
        current_param = vals
        current_formally_param = formals
        while current_param is not nil:
            child_env.define(current_formally_param.first, current_param.first)
            current_param = current_param.rest
            current_formally_param = current_formally_param.rest
        return child_env

    # END PROBLEM 2/3


##############
# Procedures #
##############


class Procedure(object):
    """The supertype of all Scheme procedures."""


def scheme_procedurep(x):
    return isinstance(x, Procedure)


class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, fn, use_env=False, name="builtin"):
        self.name = name
        self.fn = fn
        self.use_env = use_env

    def __str__(self):
        return "#[{0}]".format(self.name)

    def read_operands(self, args):
        if args is nil:
            return []
        if args.rest is nil:
            return [args.first]
        return [args.first] + self.read_operands(args.rest)

    def apply(self, args, env):
        """Apply SELF to ARGS in ENV, where ARGS is a Scheme list.

        >>> env = create_global_frame()
        >>> plus = env.bindings['+']
        >>> twos = Pair(2, Pair(2, nil))
        >>> plus.apply(twos, env)
        4
        """
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        if not scheme_listp(args):
            raise SchemeError("arguments are not a list {0}".format(args))
        operands = self.read_operands(args)
        try:
            if self.use_env:
                return self.fn(*operands, env)
            return self.fn(*operands)
        except TypeError as err:
            raise SchemeError("incorrect number of arguments")


class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        self.formals = formals
        self.body = body
        self.env = env
        if not body or body is nil:
            raise SchemeError("the body of funciton is None")

    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"

    def apply(self, argv, env):
        child_env = self.env.make_child_frame(self.formals, argv)
        return do_begin_form(self.body, child_env)

    # END PROBLEM 3
    def __str__(self):
        return str(Pair("lambda", Pair(self.formals, self.body)))

    def __repr__(self):
        return "LambdaProcedure({0}, {1}, {2})".format(
            repr(self.formals), repr(self.body), repr(self.env)
        )


def add_builtins(frame, funcs_and_names):
    """Enter bindings in FUNCS_AND_NAMES into FRAME, an environment frame,
    as built-in procedures. Each item in FUNCS_AND_NAMES has the form
    (NAME, PYTHON-FUNCTION, INTERNAL-NAME)."""
    for name, fn, proc_name in funcs_and_names:
        frame.define(name, BuiltinProcedure(fn, name=proc_name))


#################
# Special Forms #
#################

"""
How you implement special forms is up to you. We recommend you encapsulate the
logic for each special form separately somehow, which you can do here.
"""


def eval_predicate(expr, env):
    """evaluate the expr and get the value which is whether True or False and return the Boolean value and the expr's value"""
    res = scheme_eval(expr, env)
    return not res is False, res


def do_if_form(expr, env):
    validate_form(expr, 2)
    predicate, clauses = expr.first, expr.rest
    consequent, alternative = clauses.first, clauses.rest
    is_true, val = eval_predicate(predicate, env)
    if is_true:
        return scheme_eval(consequent, env)
    elif not alternative is nil:
        if len(alternative) == 1:
            return scheme_eval(alternative.first, env)
        return scheme_eval(alternative, env)
    else:
        return None


def eval_and_expr(expr, env):
    first, rest = expr.first, expr.rest
    is_true, val = eval_predicate(first, env)
    if is_true:
        if rest is nil:
            return val
        return eval_and_expr(rest, env)
    else:
        return val


def do_and_form(expr, env):
    if expr is nil:
        return True
    else:
        return eval_and_expr(expr, env)


def eval_and_expr(expr, env):
    first, rest = expr.first, expr.rest
    is_true, val = eval_predicate(first, env)
    if is_true:
        if rest is nil:
            return val
        return eval_and_expr(rest, env)
    else:
        return val


def do_or_form(expr, env):
    print("DEBUG:OR", repr(expr))
    if expr is nil:
        return False
    first, rest = expr.first, expr.rest
    is_true, val = eval_predicate(first, env)
    print("DEBUG:RES", is_true)
    if is_true:
        return val
    return do_or_form(rest, env)


def do_define_form(expr, env, store_env=None):
    validate_form(expr, 2)
    if not store_env:
        store_env = env
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first):
        validate_form(expr, 2, 2)
        if self_evaluating(rest.first):
            value = rest.first
        else:
            value = scheme_eval(rest.first, env)
        store_env.define(first, value)
    elif isinstance(first, Pair):
        symbol = first.first
        params = first.rest
        store_env.define(symbol, LambdaProcedure(params, rest, env))
        return symbol
    else:
        raise SchemeError("invalida variable".format(first))

    return first


def do_quote_form(expr, env):
    return expr.first


def do_begin_form(expr, env):
    first, rest = expr.first, expr.rest
    res = scheme_eval(first, env)
    if rest is nil:
        return res
    return do_begin_form(rest, env)


def do_lambda_form(expr, env):
    return LambdaProcedure(expr.first, expr.rest, env)


def do_cond_form(expr, env):
    clause, other_clause = expr.first, expr.rest
    condition, rest = clause.first, clause.rest
    if condition == "else":
        return do_begin_form(rest, env)
    is_true, val = eval_predicate(condition, env)
    if is_true:
        if rest is nil:
            return val
        return do_begin_form(rest, env)
    else:
        if other_clause is nil:
            return None
        return do_cond_form(other_clause, env)


def eval_let_binding(expr, env, let_frame):
    first, rest = expr.first, expr.rest
    do_define_form(first, env, let_frame)
    if not rest is nil:
        eval_let_binding(rest, env, let_frame)


def do_let_form(expr, env):
    bindings, body = expr.first, expr.rest
    let_frame = Frame(env)
    eval_let_binding(bindings, env, let_frame)
    return do_begin_form(body, let_frame)


SPECIAL_FORMS = {
    "and": do_and_form,
    "begin": do_begin_form,
    "cond": do_cond_form,
    "define": do_define_form,
    "if": do_if_form,
    "lambda": do_lambda_form,
    "let": do_let_form,
    "or": do_or_form,
    "quote": do_quote_form,
    "define-macro": do_if_form,
    "quasiquote": do_if_form,
    "unquote": do_if_form,
}
# BEGIN PROBLEM 2/3
"*** YOUR CODE HERE ***"
# END PROBLEM 2/3

# Utility methods for checking the structure of Scheme programs


def validate_form(expr, min, max=float("inf")):
    """Check EXPR is a proper list whose length is at least MIN and no more
    than MAX (default: no maximum). Raises a SchemeError if this is not the
    case.

    >>> validate_form(read_line('(a b)'), 2)
    """
    if not scheme_listp(expr):
        raise SchemeError("badly formed expression: " + repl_str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError("too few operands in form")
    elif length > max:
        raise SchemeError("too many operands in form")


def validate_formals(formals):
    """Check that FORMALS is a valid parameter list, a Scheme list of symbols
    in which each symbol is distinct. Raise a SchemeError if the list of
    formals is not a list of symbols or if any symbol is repeated.

    >>> validate_formals(read_line('(a b c)'))
    """
    symbols = set()

    def validate_and_add(symbol, is_last):
        if not scheme_symbolp(symbol):
            raise SchemeError("non-symbol: {0}".format(symbol))
        if symbol in symbols:
            raise SchemeError("duplicate symbol: {0}".format(symbol))
        symbols.add(symbol)

    while isinstance(formals, Pair):
        validate_and_add(formals.first, formals.rest is nil)
        formals = formals.rest

    # here for compatibility with DOTS_ARE_CONS
    if formals != nil:
        validate_and_add(formals, True)


def validate_procedure(procedure):
    """Check that PROCEDURE is a valid Scheme procedure."""
    if not scheme_procedurep(procedure):
        raise SchemeError(
            "{0} is not callable: {1}".format(
                type(procedure).__name__.lower(), repl_str(procedure)
            )
        )


#################
# Dynamic Scope #
#################


class MuProcedure(Procedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and
        Scheme list BODY as its definition."""
        self.formals = formals
        self.body = body

    def __str__(self):
        return str(Pair("mu", Pair(self.formals, self.body)))

    def __repr__(self):
        return "MuProcedure({0}, {1})".format(repr(self.formals), repr(self.body))


##################
# Tail Recursion #
##################


# Make classes/functions for creating tail recursive programs here?


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not a Thunk.
    Right now it just calls scheme_apply, but you will need to change this
    if you attempt the optional questions."""
    val = scheme_apply(procedure, args, env)
    # Add stuff here?
    return val


# BEGIN PROBLEM 8
"*** YOUR CODE HERE ***"
# END PROBLEM 8


####################
# Extra Procedures #
####################


def scheme_map(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, "map")
    validate_type(s, scheme_listp, 1, "map")
    return s.map(lambda x: complete_apply(fn, Pair(x, nil), env))


def scheme_filter(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, "filter")
    validate_type(s, scheme_listp, 1, "filter")
    head, current = nil, nil
    while s is not nil:
        item, s = s.first, s.rest
        if complete_apply(fn, Pair(item, nil), env):
            if head is nil:
                head = Pair(item, nil)
                current = head
            else:
                current.rest = Pair(item, nil)
                current = current.rest
    return head


def scheme_reduce(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, "reduce")
    validate_type(s, lambda x: x is not nil, 1, "reduce")
    validate_type(s, scheme_listp, 1, "reduce")
    value, s = s.first, s.rest
    while s is not nil:
        value = complete_apply(fn, scheme_list(value, s.first), env)
        s = s.rest
    return value


################
# Input/Output #
################


def read_eval_print_loop(
    next_line,
    env,
    interactive=False,
    quiet=False,
    startup=False,
    load_files=(),
    show_read=False,
):
    """Read and evaluate input until an end of file or keyboard interrupt."""
    if startup:
        for filename in load_files:
            scheme_load(filename, True, env)
    while True:
        try:
            src = next_line()
            while src.more_on_line:
                expression = scheme_read(src)
                if show_read:
                    print("str", expression)
                    print("repr", repr(expression))
                result = scheme_eval(expression, env)
                if not quiet and result is not None:
                    print(repl_str(result))
        except (SchemeError, SyntaxError, ValueError, RuntimeError) as err:
            if (
                isinstance(err, RuntimeError)
                and "maximum recursion depth exceeded" not in getattr(err, "args")[0]
            ):
                raise
            elif isinstance(err, RuntimeError):
                print("Error: maximum recursion depth exceeded")
            else:
                print("Error:", err)
        except KeyboardInterrupt:  # <Control>-C
            if not startup:
                raise
            print()
            print("KeyboardInterrupt")
            if not interactive:
                return
        except EOFError:  # <Control>-D, etc.
            print()
            return


def scheme_load(*args):
    """Load a Scheme source file. ARGS should be of the form (SYM, ENV) or
    (SYM, QUIET, ENV). The file named SYM is loaded into environment ENV,
    with verbosity determined by QUIET (default true)."""
    if not (2 <= len(args) <= 3):
        expressions = args[:-1]
        raise SchemeError(
            '"load" given incorrect number of arguments: '
            "{0}".format(len(expressions))
        )
    sym = args[0]
    quiet = args[1] if len(args) > 2 else True
    env = args[-1]
    if scheme_stringp(sym):
        sym = eval(sym)
    validate_type(sym, scheme_symbolp, 0, "load")
    with scheme_open(sym) as infile:
        lines = infile.readlines()
    args = (lines, None) if quiet else (lines,)

    def next_line():
        return buffer_lines(*args)

    read_eval_print_loop(next_line, env, quiet=quiet)


def scheme_open(filename):
    """If either FILENAME or FILENAME.scm is the name of a valid file,
    return a Python file opened to it. Otherwise, raise an error."""
    try:
        return open(filename)
    except IOError as exc:
        if filename.endswith(".scm"):
            raise SchemeError(str(exc))
    try:
        return open(filename + ".scm")
    except IOError as exc:
        raise SchemeError(str(exc))


def create_global_frame():
    """Initialize and return a single-frame environment with built-in names."""
    env = Frame(None)
    env.define("eval", BuiltinProcedure(scheme_eval, True, "eval"))
    env.define("apply", BuiltinProcedure(complete_apply, True, "apply"))
    env.define("load", BuiltinProcedure(scheme_load, True, "load"))
    env.define("procedure?", BuiltinProcedure(scheme_procedurep, False, "procedure?"))
    env.define("map", BuiltinProcedure(scheme_map, True, "map"))
    env.define("filter", BuiltinProcedure(scheme_filter, True, "filter"))
    env.define("reduce", BuiltinProcedure(scheme_reduce, True, "reduce"))
    env.define("undefined", None)
    add_builtins(env, BUILTINS)
    return env


@main
def run(*argv):
    import argparse

    parser = argparse.ArgumentParser(description="CS 61A Scheme Interpreter")
    parser.add_argument(
        "--pillow-turtle",
        action="store_true",
        help="run with pillow-based turtle. This is much faster for rendering but there is no GUI",
    )
    parser.add_argument(
        "--show-read",
        default=False,
        help="run with pillow-based turtle. This is much faster for rendering but there is no GUI",
    )
    parser.add_argument(
        "--turtle-save-path",
        default=None,
        help="save the image to this location when g",
    )
    parser.add_argument(
        "-load", "-i", action="store_true", help="run file interactively"
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=argparse.FileType("r"),
        default=None,
        help="Scheme file to run",
    )
    args = parser.parse_args()

    import scheme

    scheme.TK_TURTLE = not args.pillow_turtle
    scheme.TURTLE_SAVE_PATH = args.turtle_save_path
    sys.path.insert(0, "")
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(scheme.__file__))))

    next_line = buffer_input
    interactive = True
    load_files = []

    if args.file is not None:
        if args.load:
            load_files.append(getattr(args.file, "name"))
        else:
            lines = args.file.readlines()

            def next_line():
                return buffer_lines(lines)

            interactive = False
    show_read = args.show_read
    read_eval_print_loop(
        next_line,
        create_global_frame(),
        startup=True,
        interactive=interactive,
        load_files=load_files,
        show_read=show_read,
    )
    tscheme_exitonclick()
