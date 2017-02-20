from flask import Flask, request, render_template
from sanity_check import sanity_domain, sanity_combine_dob
from lookup_whois import lookup
from age_calc import age_function
from html_generation import day, month, year
from form import RegistrationForm

application = Flask(__name__)

@application.route('/')
def home():
    return render_template('index.html')

@application.route('/form')
def form():
    return render_template('form.html', day_list = day(31),
                                        month_list = month(),
                                        year_list = year(1900,2017))

@application.route('/results', methods=['POST'])
def results():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # required inputs
        name = request.form['username']
        domain = request.form['domain_name']
        Day = request.form['day']
        Month = request.form['month']
        Year = request.form['year']
    else:
        return render_template('error.html', error_message = 'unrecognised input format',
                                             further_explanation = "Input is required in the form,<br>'username=&day=&month=&year=&domain_name='")

    # this section handles the domain's age and expiry date
    try:
        checked_domain = sanity_domain(domain)
    except AttributeError as e:
        return render_template('error.html', error_message = e,
                                             further_explanation = "Accepted top level domains are:<br>com|org|uk|net|co_jp|it|cz|at|eu|ru|lv|nz|pl|be|fr|de|jp|me|biz|info|name|us|co")
    # for testing purposes nolookup.com will not bother the whois database with a request
    if checked_domain == "nolookup.com":
        start = "2017-02-09"
        exp = "2038-01-19"
    else:
        # catching errors, they should probably all be one type and pass the error e to the error_message and then give further_explanation using if statements to determine which problem occured
        try:
            start_exp  = lookup(checked_domain)
        except AttributeError as e:
            return render_template('error.html', error_message = e,
                                                 further_explanation = "The application can not lookup your chosen domain in its current state try another domain" )
        start = start_exp.split(':')[0]
        exp = start_exp.split(':')[1]

    domain_age = age_function(start)


    # this section handles the user's age
    try:
        checked_dob = sanity_combine_dob(Day,Month,Year)
    except AttributeError:
        return render_template('error.html', error_message = "Please enter a your DOB in a compatable format.",
                                             further_explanation = "Did you miss a field? 'username=&day=dd&month=mm&year=yyyy&domain_name=' is currently the only accepted format.")
    try:
        age = age_function(checked_dob)
    except ValueError:
        return render_template('error.html', error_message = "Please enter an existing DOB",
                                             further_explanation = "The DOB you entered does not exist,<br> it is likely that you entered a DOB such as 30 Feb, 31 Apr.")

    # calculate the age difference between the user and the domain they entered to be returned to them
    age_difference = int(age) - int(domain_age)

    # determining what phrase to use to describe the age difference
    if int(age_difference) > 1:
        older_younger = "years older than"
    elif int(age_difference) < -1:
        older_younger = "years younger than"
        age_difference = -int(age_difference)
    elif int(age_difference) == 0:
        older_younger = "the same age as"
        age_difference = ""
    elif int(age_difference) == 1:
        older_younger = "year older than"
    elif int(age_difference) == -1:
        older_younger = "year younger than"
        age_difference = -int(age_difference)

    # passing variables to the results template to give the dynamic output
    return render_template('results.html', username = name,
                                           your_age = age,
                                           domain_name = checked_domain,
                                           regestered = start,
                                           expires = exp,
                                           domain_age = domain_age,
                                           age_difference = age_difference,
                                           older_younger = older_younger)

if __name__ == '__main__':
    application.run()
