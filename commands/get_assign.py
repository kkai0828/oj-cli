import json
import os
#from BeautifulSoup import BeautifulSoup as bs

from constants import ASSIGNMENT_MAPPING_PATH
from util.curl import curl
from util.colors import cyan_wrapper, red_wrapper


def get_assign(assign_name):
    try:
        with open(ASSIGNMENT_MAPPING_PATH, "rt") as json_in:
            assign_to_config = json.load(json_in)
    except:
        print(red_wrapper("Can not find assign mapping, did you already run ") + cyan_wrapper("oj update ") + red_wrapper("?"))
        return
    if assign_name not in assign_to_config:
        print("Invalid Assign Number!")
        print("Available names are:")
        for hwmap in assign_to_config:
            print("- " + cyan_wrapper(hwmap + " [" + assign_to_config[hwmap]['contest_name'] + "]"))
        print("If you want to update latest homework assignment, type: [oj update] to update.")
        return
    contest_id, problem_id = (
        assign_to_config[assign_name]["contest_id"],
        assign_to_config[assign_name]["contest_problem_id"],
    )
    endpoint = "contest/problem?contest_id={}&problem_id={}".format(
        contest_id, problem_id
    )
    result = json.loads(curl("get", endpoint=endpoint, use_x_csrf_token=True))
    data = result["data"]
    if not data:
        print("Unexpected Error with Server")
        return
    try:
        samples = data["samples"]
    except:
        print("Unexpected Error in Parsing Response")
        print(data)
        return
    template = None
    if "C" in data["template"]:
        template = data["template"]["C"]
    else:
        template = "#include <stdio.h>\n\nint main() {\n    \n    return 0;\n}\n"
    dir_name = data["_id"]
    print("Made a [{}] folder in your current directory.".format(dir_name))
    template_path = dir_name + "/main.c"
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    with open(template_path, "wt") as fout:
        fout.write(template)
    for idx, sample in enumerate(samples):
        sample_num = idx + 1
        input_sample_path = dir_name + "/" + "{}.in".format(sample_num)
        input_ = sample["input"]
        with open(input_sample_path, "wt") as fout:
            try:
                fout.write(input_)
            except:
                print("ERROR: None-ascii character in input file")
        output_sample_path = dir_name + "/" + "{}.out".format(sample_num)
        output = sample["output"]
        with open(output_sample_path, "wt") as fout:
            try:
                fout.write(output)
            except:
                print("ERROR: None-ascii character in input file")
