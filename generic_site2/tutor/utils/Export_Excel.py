from django.conf import settings
from tutor.models import Event, Student
from datetime import date
from calendar import monthrange

from io import StringIO, BytesIO
# from io import StringIO
import xlsxwriter
 
def TutorExportExcel(year, month):
    output = BytesIO()
    # workbook = xlsxwriter.Workbook(output)

    named_month = date(1900, int(month), 1).strftime("%B")
        
    workbook = xlsxwriter.Workbook(output)

    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
        })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
        })

    # This is the summary worksheet
    worksheet_s = workbook.add_worksheet(str(year) + "_" + named_month)
    worksheet_s.set_column('A:Z', 20)

    title_text = "Sessions for " + str(year) + " " + named_month
    worksheet_s.merge_range('B2:F2', title_text, title)

    worksheet_s.write_string(4, 0, "Date", header)
    worksheet_s.write_string(4, 1, "From Time", header)
    worksheet_s.write_string(4, 2, "To Time", header)
    worksheet_s.write_string(4, 3, "Student", header)
    worksheet_s.write_string(4, 4, "Instructor", header)
    worksheet_s.write_string(4, 5, "Session", header)
    worksheet_s.write_string(4, 6, "Duration (Hour)", header)

    from_month = date(int(year), int(month), 1)
    to_month = date(int(year), int(month), monthrange(int(year), int(month))[1])
    events = Event.objects.filter(day_dt__gte=from_month, day_dt__lte=to_month)

    for idx, data in enumerate(events):
        row = 5 + idx
        worksheet_s.write(row, 0, data.day_dt.strftime('%Y-%m-%d')) 
        worksheet_s.write_string(row, 1, data.from_time[0:5])
        worksheet_s.write_string(row, 2, data.to_time[0:5])
        worksheet_s.write_string(row, 3, data.student.name)
        worksheet_s.write_string(row, 4, data.instructor.name)
        worksheet_s.write_string(row, 5, data.lesson_type.name)
        worksheet_s.write_number(row, 6, data.get_duration_hr())
    # now we do a sheet per Student
    for student in Student.objects.all(): 
        worksheet_s = workbook.add_worksheet(student.name + " " + student.surname)
        worksheet_s.set_column('A:Z', 20)

        title_text = named_month + " sessions for " + student.name + " " + student.surname + " " 
        worksheet_s.merge_range('B2:F2', title_text, title)

        worksheet_s.write_string(4, 0, "Date", header)
        worksheet_s.write_string(4, 1, "From Time", header)
        worksheet_s.write_string(4, 2, "To Time", header)
        worksheet_s.write_string(4, 3, "Student", header)
        worksheet_s.write_string(4, 4, "Instructor", header)
        worksheet_s.write_string(4, 5, "Session", header)
        worksheet_s.write_string(4, 6, "Duration (Hour)", header)

        from_month = date(int(year), int(month), 1)
        to_month = date(int(year), int(month), monthrange(int(year), int(month))[1])
        events = Event.objects.filter(day_dt__gte=from_month, day_dt__lte=to_month, student = student )

        for idx, data in enumerate(events):
            row = 5 + idx
            worksheet_s.write(row, 0, data.day_dt.strftime('%Y-%m-%d')) 
            worksheet_s.write_string(row, 1, data.from_time[0:5])
            worksheet_s.write_string(row, 2, data.to_time[0:5])
            worksheet_s.write_string(row, 3, data.student.name)
            worksheet_s.write_string(row, 4, data.instructor.name)
            worksheet_s.write_string(row, 5, data.lesson_type.name)
            worksheet_s.write_number(row, 6, data.get_duration_hr())
    
    workbook.close()
    # the rest of the data
    # xlsx_data contains the Excel file
    xlsx_data = output.getvalue()

    return xlsx_data



