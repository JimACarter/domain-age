def age_function(input_date):
    """Input date of birth dd-mm-yyyy.  Return age in years"""
    from datetime import date, datetime
    list_date = str(input_date).split("-")
    list_today = str(date.today()).split("-")
    try:
        datetime(int(list_date[0]), int(list_date[1]), int(list_date[2]))
    except ValueError as e:
        raise ValueError("DOB does not exist", e)
    the_age = int(list_today[0]) - int(list_date[0])
    if int(list_today[1]) < int(list_date[1]):
        the_age -= 1
    elif int(list_today[1]) == int(list_date[1]) and int(list_today[2]) < int(list_date[2]):
        the_age -= 1
    return(the_age)
