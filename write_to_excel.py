# Import xlrd for reading xls file
import xlrd

# Import xlwt for writing to xls file
import xlwt

#Import xlutils.copy to copy the workbook and edit it
from xlutils.copy import copy

def writeSheet(gameDataList):

	# Open the existing spreadsheet
	rb = xlrd.open_workbook("scraped_data.xls")

	# Get the first sheet (only for counting number of rows)
	rb_sheet = rb.sheet_by_index(0)
	num_rows = rb_sheet.nrows-1
	
	# Make a copy and edit the copy
	wb = copy(rb)

	# Get the first sheet (for editing)
	wb_sheet = wb.get_sheet(0)

	for gameData in gameDataList:

		# Keep track of the row number you are writing to
		num_rows += 1

		# At each row, start at the first column
		num_cols = 0

		# Iterate values of winner data and write to spreadsheet
		for value in gameData[0].itervalues():
			wb_sheet.write(num_rows, num_cols, value)
			num_cols +=1

		# Iterate values of loser data and write to spreadsheet
		for value in gameData[1].itervalues():
			wb_sheet.write(num_rows, num_cols, value)
			num_cols +=1

	# Save file
	wb.save('Scraped_data.xls')