#!/usr/bin/python2.7

import argparse

from commands import auth, get_assign, get_problem, status, submit, update_map, contests

parser = argparse.ArgumentParser(
    prog="oj",
    description="CLI tool that helping you access CP Online Judge",
)
subparsers = parser.add_subparsers(dest="subcmd")
parser_login = subparsers.add_parser(
    "login", description="Login your account to CP Online Judge"
)
parser_login.set_defaults(func=auth)

parser_update = subparsers.add_parser(
    "update", description="Update your Assign and Exercise Homework"
)
parser_login.set_defaults(func=update_map)

parser_get_assign = subparsers.add_parser(
    "get_assign", description="Get assignment/exercise from contest"
)
parser_get_assign.add_argument("assign_no", type=str, help="assignment number")
parser_get_assign.set_defaults(func=get_assign)


parser_contest = subparsers.add_parser(
    "contest", description="View specific contest statics."
)
parser_contest.add_argument("option", type=str, help="[status|s`]: Show the latest 20 submissions of this contest. [update|u]: Update the latest contest. [rank|r]: Show the rank of this contest.")
parser_contest.add_argument("assign_no", type=str, help="assignment number. NOTICE that the [update] method requires this argument.")
parser_contest.set_defaults(func=contests)


parser_get_problem = subparsers.add_parser(
    "get_problem", description="Get problem from public problem"
)
parser_get_problem.add_argument("problem_id", type=str, help="problem display ID")

parser_submit = subparsers.add_parser(
    "submit", description="Submit and grade your code"
)
parser_submit.add_argument("assign_no", type=str, help="assignment number")
parser_submit.add_argument("code_file", type=str, help="file of your codes")

parser_status = subparsers.add_parser("status", description="Get submission status")
parser_status.add_argument("submission_id", type=str, help="the submission id")

args = parser.parse_args()
cmd_to_func = {
    "login": auth,
	"update": update_map,
    "get_assign": lambda: get_assign(args.assign_no),
    "get_problem": lambda: get_problem(args.problem_id),
    "submit": lambda: submit(args.assign_no, args.code_file),
    "status": lambda: status(args.submission_id),
	"contest": lambda: contests(args.option, args.assign_no),
}


cmd_to_func[args.subcmd]()
