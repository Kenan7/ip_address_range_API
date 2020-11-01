import csv
from typing import Any, Dict

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:4200",
# ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# seperate IP address by dots
def tear_ip(ip: str):
    splitted_ip_by_dots = ip.split(".")
    return {
        "1st_part_of_ip": int(splitted_ip_by_dots[0]),
        "2nd_part_of_ip": int(splitted_ip_by_dots[1]),
        "3rd_part_of_ip": int(splitted_ip_by_dots[2]),
        "4th_part_of_ip": int(splitted_ip_by_dots[3]),
    }


# we use the get_item function here to check for collisions notice how there is not any duplicate code [DRY]
def check_collisions(ip: str):
    result = get_item(ip)
    if len(result) > 0:
        return False
    else:
        return True


file_location = "assets/New.csv"


@app.post("/add")
def add_entry(request: Dict[Any, Any]):
    # check for collision when adding. we don't want any duplicates
    if check_collisions(request["ip1"]):
        # if the defined function returns true then we can append the new address range
        with open(file_location, "a+", newline="") as csv_file:
            # we opened and passed the file to the csv writer function (append mode)
            csv_writer = csv.writer(csv_file)
            # add
            csv_writer.writerow([f"{request['ip1']} {request['ip2']}"])

        return JSONResponse(status_code=201, content={"message": "Added!"})

    # if there is any duplicates
    else:
        return JSONResponse(status_code=409, content={"message": "This entry already exists!"})


@app.get("/get/{ip}")
def get_item(ip: str):

    # initalize emtpy array for storing ranges
    ip_ranges_list = []

    # seperate input for comparing later
    teared_up_input = tear_ip(ip)

    # open csv file
    with open(file_location, "r") as csv_file:
        # pass file object to reader function
        csv_reader = csv.reader(csv_file, delimiter=",")

        # pass on one line because first line is the header and we need numbers
        next(csv_reader)

        # loop through csv lines
        for ip_range in csv_reader:
            # split ip addresses by space which is formatted like 34.43.23.0 34.43.23.255
            splitted_by_space = str(ip_range[0]).split(" ")
            # split ip addresses which is seperated by space
            teared_up_start = tear_ip(ip=splitted_by_space[0])
            teared_up_last = tear_ip(ip=splitted_by_space[1])

            # compare
            if (
                teared_up_start["1st_part_of_ip"]
                <= teared_up_input["1st_part_of_ip"]
                <= teared_up_last["1st_part_of_ip"]
            ):

                if (
                    teared_up_start["2nd_part_of_ip"]
                    <= teared_up_input["2nd_part_of_ip"]
                    <= teared_up_last["2nd_part_of_ip"]
                ):
                    if (
                        teared_up_start["3rd_part_of_ip"]
                        <= teared_up_input["3rd_part_of_ip"]
                        <= teared_up_last["3rd_part_of_ip"]
                    ):
                        if (
                            teared_up_start["4th_part_of_ip"]
                            <= teared_up_input["4th_part_of_ip"]
                            <= teared_up_last["4th_part_of_ip"]
                        ):
                            # add matched addresses to the list
                            ip_ranges_list.append(ip_range[0])

    # return the matched addresses
    return ip_ranges_list
