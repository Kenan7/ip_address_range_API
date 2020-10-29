from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Form
from typing import Dict, Any
from xlrd import open_workbook
from xlutils.copy import copy
from openpyxl import Workbook, load_workbook


app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:4200",
# ]

file_location = "assets/Section_4.xlsx"

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


# convert tabs to spaces because it causes error the next time we open it
#  (tabs are deleted so I could not seperate ip addresses, this is the solution I came up with)
def convert_tabs_to_spaces():
    wb = open_workbook(file_location)
    write_mode = copy(wb)
    sheet = wb.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        if "\t" in sheet.cell_value(i, 0):
            val_modified = sheet.cell_value(i, 0).replace("\t", " ")
            write_mode.get_sheet(0).write(i, 0, val_modified)

    write_mode.get_sheet(0).write(0, 1, "CONVERTED")
    write_mode.save(file_location)


@app.get("/get/{ip}")
def get_all(ip: str):
    wb = open_workbook(file_location)
    sheet = wb.sheet_by_index(0)

    # if the tabs (\t) you put in between addresses still not converted to space then do it (:
    try:
        # try to see if it's already converted. if yes then pass
        if str(sheet.cell_value(0, 1)) == "CONVERTED":
            pass
        # if it's not converted then do it
        else:
            convert_tabs_to_spaces()
            # after converting the file, open it again
            wb = open_workbook(file_location)
            sheet = wb.sheet_by_index(0)
    # if in any way it throws indexerror that's because it can't read the 'converted' string which is not there
    # this is extra step that is because xlrd API does not return anything about cell is empty or does not exists
    # it's basically raises IndexError if there is not a cell
    except IndexError:
        convert_tabs_to_spaces()
        wb = open_workbook(file_location)
        sheet = wb.sheet_by_index(0)

    # initalize emtpy array for storing ranges
    ip_ranges = []

    teared_up_input = tear_ip(ip)

    # read all addresses and add those to the list which is in range
    for i in range(1, sheet.nrows):

        splitted_by_space = str(sheet.cell_value(i, 0)).split(" ")

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


@app.post("/create")
def new_entry(request: Dict[Any, Any]):
    # open the workbook in read mode
    read = open_workbook(file_location)
    # this function copies xlrd.Book objects into xlwt.Workbook objects so they can be manipulated
    write = copy(read)
    # read the first page
    sheet = read.sheet_by_index(0)
    # convert dict objects to string like 34.45.34.0 34.45.34.255
    new_value = f"{request['ip1']} {request['ip2']}"
    # write the new value to last row
    write.get_sheet(0).write(sheet.nrows, 0, new_value)
    write.save(file_location)
