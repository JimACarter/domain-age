def day(days_in_month):
    """Input number of days in month. Returns html for dropdown choice of days"""
    list_message = []
    for date in range(1, days_in_month+1):
        list_message.append("<option value={}>{}</option>". format(date,date))
    return("\n                 ".join(list_message))

def month():
    """Returns html for dropdown choice of months"""
    list_month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    list_message = []
    for num_month, word_month in enumerate(list_month, start=1):
        list_message.append("<option value={}>{}</option>". format(num_month,word_month))
    return("\n                 ".join(list_message))

def year(start, end):
    """Input year to count from and until.  Returns html for dropdown choice of years"""
    list_message = []
    for the_year in range(start, end+1):
        list_message.append("<option value={}>{}</option>". format(the_year,the_year))
    list_message.reverse()
    return("\n                 ".join(list_message))
