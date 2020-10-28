from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
import xlrd

app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
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


def tear_ip(ip: str):
    splitted_ip_by_dots = ip.split(".")
    return {
        "1st_part_of_ip": int(splitted_ip_by_dots[0]),
        "2nd_part_of_ip": int(splitted_ip_by_dots[1]),
        "3rd_part_of_ip": int(splitted_ip_by_dots[2]),
        "4th_part_of_ip": int(splitted_ip_by_dots[3]),
    }


@app.get("/get/{ip}")
def get_all(ip: str):
    wb = xlrd.open_workbook("assets/Section_4.xlsx")
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    ip_ranges = []

    teared_up_input = tear_ip(ip)

    for i in range(1, sheet.nrows):
        splitted_by_space = str(sheet.cell_value(i, 0)).split("\t")

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

                        ip_ranges.append(sheet.cell_value(i, 0))

    return ip_ranges
