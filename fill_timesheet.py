import csv
import urllib2
import datetime
import sys
from pdfjinja import PdfJinja

import settings

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"
EMPTY_TIMESHEET = "timesheet.pdf"

def fill_timesheets(week_start_dates):
    info_sheet = read_google_sheet(settings.SPREADSHEET_ID, settings.INFO_SHEET_ID)
    hours_sheet = read_google_sheet(settings.SPREADSHEET_ID, settings.HOURS_SHEET_ID)
    for week_start_date in week_start_dates:
        fill_timesheet(week_start_date, info_sheet, hours_sheet)
    
def fill_timesheet(week_start_date, info_sheet, hours_sheet):
    pdfjinja = PdfJinja(EMPTY_TIMESHEET)
    pdf_output = pdfjinja(get_timesheet_data(week_start_date, info_sheet, hours_sheet))
    formatted_date = week_start_date.strftime("%Y-%m-%d")
    with open("timesheet_filled_%s.pdf" % formatted_date, "wb") as output_file:
        pdf_output.write(output_file)

def get_timesheet_data(week_start_date, info_sheet, hours_sheet):
    assert week_start_date.weekday() == 6, "week_start_date must be a Sunday"
    assert len(info_sheet) == 1, "Info sheet must have exactly one row."
    info = info_sheet[0]
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

def read_google_sheet(spreadsheet_id, sheet_id):
    sheet_url = SHEET_CSV_URL.format(spreadsheet_id=spreadsheet_id, sheet_id=sheet_id)
    return list(csv.DictReader(urllib2.urlopen(sheet_url)))

def format_date(date):
    return date.strftime("%d %b %Y")
    
def parse_date(date_string):
    return datetime.datetime.strptime(date_string, "%Y-%m-%d")

def main(args):
    if len(args) > 0:
        week_start_dates = [parse_date(date_string) for date_string in args]
    else:
        today = datetime.datetime.today()
        # Weeks start on Sunday at McGill.
        week_start_date = today - datetime.timedelta(days=(today.weekday() + 1))
        last_week_start_date = week_start_date - datetime.timedelta(weeks=1)
        week_start_dates = [last_week_start_date, week_start_date]

    fill_timesheets(week_start_dates)

if __name__ == "__main__":
    main(sys.argv[1:])
    
