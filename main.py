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


def check_collisions(ip: str):
    result = get_item(ip)
    if len(result) > 0:
        return False
    else:
        return True


file_location = "assets/Section_4.csv"


@app.post("/add")
def add_entry(request: Dict[Any, Any]):
    file_location = "assets/New copy.csv"

    if check_collisions(request["ip1"]):
        with open(file_location, "a+", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([f"{request['ip1']} {request['ip2']}"])

        return JSONResponse(status_code=201, content={"message": "Added!"})

    else:
        return JSONResponse(status_code=409, content={"message": "This entry already exists!"})


@app.get("/get/{ip}")
def get_item(ip: str):
    file_location = "assets/New copy.csv"

    # initalize emtpy array for storing ranges
    ip_ranges_list = []

    teared_up_input = tear_ip(ip)

    with open(file_location, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        next(csv_reader)

        for ip_range in csv_reader:

            splitted_by_space = str(ip_range[0]).split(" ")
            teared_up_start = tear_ip(ip=splitted_by_space[0])
            teared_up_last = tear_ip(ip=splitted_by_space[1])

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

                            ip_ranges_list.append(ip_range[0])

    return ip_ranges_list
