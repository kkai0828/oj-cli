import json
import os
from datetime import datetime

from constants import ASSIGNMENT_MAPPING_PATH
from constants import COOKIES_DIR
from util.common import get_csrf_token
from util.curl import curl
from util.colors import cyan_wrapper, green_wrapper, purple_wrapper, red_wrapper


def contests_status(assign_name):
	with open(ASSIGNMENT_MAPPING_PATH, "rt") as json_in:
		assign_to_config = json.load(json_in)
	if assign_name not in assign_to_config:
		print("Invalid Assign Number!")
		print("Available names are:")
		for hwmap in assign_to_config:
			print("- " + cyan_wrapper(hwmap))
		print("If you want to update latest homework assignment, type: [oj update] to update.")
		return
	contest_id, problem_id = (
        assign_to_config[assign_name]["contest_id"],
        assign_to_config[assign_name]["contest_problem_id"],
    )
	endpoint = "contest_submissions?myself=0&contest_id={}&limit=20".format(
        contest_id
    )
	result = json.loads(curl("get", endpoint=endpoint, use_x_csrf_token=True))
	result = result["data"]["results"]
	
	status_to_response = {
			-1: red_wrapper("WA(Wrong Answer)"),  # WA
			-2: cyan_wrapper("CE(Compilation Error)"),  # CE
			0: green_wrapper("AC(Accept)"),  # AC
			2: "TLE(Time Limit Exceeded)",  # TLE
			3: "MLE(Memory Limit Exceeded)",  # ML 
			4: purple_wrapper("RE(Runtime Error)"),  # RE
			8: cyan_wrapper("PAC(Partial Accepted)")
			}
	print('|{:12}|{:22}|{:7}|{:5}|{}'.format("User","Status","Time","Mem","When"))
	for i in result:
		timestr = i["create_time"].split("T")[0]
		timestr += " " + i["create_time"].split("T")[1].split(".")[0]
		if i["result"] != -2:
			print('|{:12}|{:33}|{:5}ms|{:3}MB|{}|'.format(i["username"], status_to_response[i["result"]], i["statistic_info"]["time_cost"], (i["statistic_info"]["memory_cost"]/1048576)+1, timestr))
		else:
			print('|{:12}|{:33}|{:5}--|{:3}--|{}|'.format(i["username"], status_to_response[i["result"]], "-----", "---", timestr))


def my_contests_status(assign_name):
	with open(ASSIGNMENT_MAPPING_PATH, "rt") as json_in:
		assign_to_config = json.load(json_in)
	if assign_name not in assign_to_config:
		print("Invalid Assign Number!")
		print("Available names are:")
		for hwmap in assign_to_config:
			print("- " + cyan_wrapper(hwmap))
		print("If you want to update latest homework assignment, type: [oj update] to update.")
		return
	contest_id, problem_id = (
        assign_to_config[assign_name]["contest_id"],
        assign_to_config[assign_name]["contest_problem_id"],
    )
	endpoint = "contest_submissions?myself=1&contest_id={}&limit=20".format(
        contest_id
    )
	result = json.loads(curl("get", endpoint=endpoint, use_x_csrf_token=True))
	result = result["data"]["results"]
	
	status_to_response = {
			-1: red_wrapper("WA(Wrong Answer)"),  # WA
			-2: cyan_wrapper("CE(Compilation Error)"),  # CE
			0: green_wrapper("AC(Accept)"),  # AC
			2: "TLE(Time Limit Exceeded)",  # TLE
			3: "MLE(Memory Limit Exceeded)",  # ML 
			4: purple_wrapper("RE(Runtime Error)"),  # RE
			8: cyan_wrapper("PAC(Partial Accepted)")
			}
	print('|{:12}|{:22}|{:7}|{:5}|{}'.format("User","Status","Time","Mem","When"))
	for i in result:
		timestr = i["create_time"].split("T")[0]
		timestr += " " + i["create_time"].split("T")[1].split(".")[0]
		if i["result"] != -2:
			print('|{:12}|{:33}|{:5}ms|{:3}MB|{}|'.format(i["username"], status_to_response[i["result"]], i["statistic_info"]["time_cost"], (i["statistic_info"]["memory_cost"]/1048576)+1, timestr))
		else:
			print('|{:12}|{:33}|{:5}--|{:3}--|{}|'.format(i["username"], status_to_response[i["result"]], "-----", "---", timestr))



def contests_result(assign_name):
	with open(ASSIGNMENT_MAPPING_PATH, "rt") as json_in:
		assign_to_config = json.load(json_in)
	if assign_name not in assign_to_config:
		print("Invalid Assign Number!")
		print("Available names are:")
		for hwmap in assign_to_config:
			print("- " + cyan_wrapper(hwmap))
		print("If you want to update latest homework assignment, type: [oj update] to update.")
		return

	contest_id, problem_id = (
        assign_to_config[assign_name]["contest_id"],
        assign_to_config[assign_name]["contest_problem_id"],
    )
	endpoint = "contest_rank?myself=0&contest_id={}&limit=100".format(
        contest_id
    )
	result = json.loads(curl("get", endpoint=endpoint, use_x_csrf_token=True))
	endpoint = "contest/problem?contest_id={}".format(
        contest_id
    )
	result2 = json.loads(curl("get", endpoint=endpoint, use_x_csrf_token=True))
	result = result["data"]["results"]
	result2 = result2["data"][0]
	status_to_response = {
			-1: red_wrapper("WA(Wrong Answer)"),  # WA
			-2: cyan_wrapper("CE(Compilation Error)"),  # CE
			0: green_wrapper("AC(Accept)"),  # AC
			2: "TLE(Time Limit Exceeded)",  # TLE
			3: "MLE(Memory Limit Exceeded)",  # ML 
			4: purple_wrapper("RE(Runtime Error)"),  # RE
			8: cyan_wrapper("PAC(Partial Accepted)")
			}
	if result2["my_status"] == "null":
		print("\nYour status of " + assign_name + " : No rrecord")
	else:
		print("\nYour status of " + assign_name + " : " + status_to_response[result2["my_status"]])
	print("================================================")
	blockstatus=[0,0,0,0,0,0,0,0,0,0]
	for usr in result:
		blocks = usr["total_score"]/10
		blocks -= 1
		blockstatus[blocks] += 1
	ic = 0
	for i in blockstatus:
		stastr = ''
		if ic == 0:
			print(' {:3}~{:3} :{:3}  |  {:33} : {}'.format(ic+1,ic+10,i,status_to_response[0],result2["statistic_info"]["0"]))
		elif ic == 10:
			print(' {:3}~{:3} :{:3}  |  {:33} : {}'.format(ic+1,ic+10,i,status_to_response[4],result2["statistic_info"]["4"]))
		elif ic == 20:
			print(' {:3}~{:3} :{:3}  |  {:33} : {}'.format(ic+1,ic+10,i,status_to_response[8],result2["statistic_info"]["8"]))
		elif ic == 30:
			print(' {:3}~{:3} :{:3}  |  {:33} : {}'.format(ic+1,ic+10,i,status_to_response[-1],result2["statistic_info"]["-1"]))	
		elif ic == 40:
			print(' {:3}~{:3} :{:3}  |  {:33} : {}'.format(ic+1,ic+10,i,status_to_response[-2],result2["statistic_info"]["-2"]))
		elif ic == 50:
			print(' {:3}~{:3} :{:3}  |--------------------------------'.format(ic+1,ic+10,i))
		elif ic == 60:
			print(' {:3}~{:3} :{:3}  |  {:22} : {}'.format(ic+1,ic+10,i,"Total submissions",result2["submission_number"]))
		else:
			print(' {:3}~{:3} :{:3}  |'.format(ic+1,ic+10,i))
		ic += 10
	print("")
