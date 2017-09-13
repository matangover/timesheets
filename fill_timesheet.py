import csv
import urllib2
import datetime
from pdfjinja import PdfJinja

import settings

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"
EMPTY_TIMESHEET = "timesheet.pdf"

def get_timesheet_data(week_start_date):
    assert week_start_date.weekday() == 6, "week_start_date must be a Sunday"
    info_sheet = read_google_sheet(settings.SPREADSHEET_ID, settings.INFO_SHEET_ID)
    assert len(info_sheet) == 1, "Info sheet must have exactly one row."
    info = info_sheet[0]
    
    hours_sheet = read_google_sheet(settings.SPREADSHEET_ID, settings.HOURS_SHEET_ID)
    week_end_date = week_start_date + datetime.timedelta(days=6)
    days = [
        day for day in hours_sheet
        if week_start_date <= parse_date(day["Date"]) <= week_end_date
    ]
    total_hours = sum([float(day["Total Hours"]) for day in days if day["Total Hours"] != ""])
    data = {}
    data["hourlyRate"] = info["Hourly Rate"]
    data["totalHours"] = total_hours
    data["total"] = total_hours * float(info["Hourly Rate"])
    data["name"] = info["Name (Last & First)"]
    data["id"] = info["McGill ID #"]
    data["department"] = info["Department / Unit"]
    data["sin"] = info["SIN # (optional)"]
    data["startDate"] = format_date(week_start_date)
    data["endDate"] = format_date(week_end_date)
    data["date"] = format_date(datetime.datetime.now())
    for day in days:
        date = parse_date(day["Date"])
        # Convert from [Monday=0 to Sunday=6] to [Sunday=1 to Saturday=7].
        day_index = str((date.weekday() + 1) % 7 + 1)
        data["timeIn_" + day_index] = day["Time In"]
        data["timeOut_" + day_index] = day["Time Out"]
        data["timeOff_" + day_index] = day["Time Off"]
        data["totalHours_" + day_index] = day["Total Hours"]
        data["project_" + day_index] = day["Project / Task"]
        data["comment_" + day_index] = day["Comments"]
        
    return data

def fill_timesheet(week_start_date):    
    pdfjinja = PdfJinja(EMPTY_TIMESHEET)
    pdf_output = pdfjinja(get_timesheet_data(week_start_date))
    formatted_date = week_start_date.strftime("%Y-%m-%d")
    with open("timesheet_filled_%s.pdf" % formatted_date, "wb") as output_file:
        pdf_output.write(output_file)

def read_google_sheet(spreadsheet_id, sheet_id):
    sheet_url = SHEET_CSV_URL.format(spreadsheet_id=spreadsheet_id, sheet_id=sheet_id)
    return list(csv.DictReader(urllib2.urlopen(sheet_url)))

def format_date(date):
    return date.strftime("%d %b %Y")
    
def parse_date(date_string):
    return datetime.datetime.strptime(date_string, "%Y-%m-%d")


fill_timesheet(datetime.datetime(2017, 8, 13))
