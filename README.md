# timesheets
Automatically fill out McGill timesheets.

### Prerequisites
1. Python 2.x
2. [pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/). macOS users, note that as of September 2017, the official Mac installer is broken and causes this script to hang. Install using this unofficial Homebrew formula instead:
```
brew install https://raw.githubusercontent.com/turforlag/homebrew-cervezas/master/pdftk.rb
```
3. pdfjinja: `pip install pdfjinja`


### Usage instructions
1. Open the original [Timesheet spreadsheet](https://docs.google.com/spreadsheets/d/1UHdaKoOdp5DbGHOrB0tZph0UFaNCRrA54Qx-YEUbgX0/edit?usp=sharing) and clone it into your own Google Drive by clicking `File -> Make a copy...`.
2. Open the cloned spreadsheet and click `Share`, then `Get shareable link`.
3. Copy the spreadsheet id that is part of the spreadsheet's URL:
`https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit` 
4. Clone this repository to your computer. Open `settings.py` and change `SPREADSHEET_ID` to your spreadsheet's ID.
5. Fill out your personal information in the spreadsheet under the `Info` sheet.
6. Fill out your work hours (`Time In`, `Time Out`, `Time Off`) as needed. Total hours and pay are calculated automatically.
7. Run the following command from the repository root directory:

```
python fill_timesheet.py
```
This will generate a `timesheet_filled_yyyy-mm-dd.pdf` file in the same directory. Print, sign, and spread the love. :) 
