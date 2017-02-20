from flask import Flask, request, render_template, session
from sanity_check import sanity_domain, sanity_combine_dob
from lookup_whois import lookup
from age_calc import age_function
from html_generation import day, month, year
from form import RegistrationForm

application = Flask(__name__)

key_file = open('.key.txt')
application.config['SECRET_KEY'] = key_file.readline()
key_file.close()

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
        session['name'] = request.form['username']
        session['domain'] = request.form['domain_name']
        session['Day'] = request.form['day']
        session['Month'] = request.form['month']
        session['Year'] = request.form['year']
    else:
        return render_template('error.html', error_message = 'unrecognised input format',
                                             further_explanation = "Input is required in the form,<br>'username=&day=&month=&year=&domain_name='")

    # this section handles the domain's age and expiry date
    try:
        session['checked_domain'] = sanity_domain(session['domain'])
    except AttributeError as e:
        return render_template('error.html', error_message = e,
                                             further_explanation = "Accepted top level domains are:<br>com|org|uk|net|co_jp|it|cz|at|eu|ru|lv|nz|pl|be|fr|de|jp|me|biz|info|name|us|co")
    # for testing purposes nolookup.com will not bother the whois database with a request
    if session['checked_domain'] == "nolookup.com":
        session['start'] = "2017-02-09"
        session['exp'] = "2038-01-19"
    else:
        # catching errors, they should probably all be one type and pass the error e to the error_message and then give further_explanation using if statements to determine which problem occured
        try:
            start_exp  = lookup(session['checked_domain'])
        except AttributeError as e:
            return render_template('error.html', error_message = e,
                                                 further_explanation = "The application can not lookup your chosen domain in its current state try another domain" )
        session['start'] = start_exp.split(':')[0]
        session['exp'] = start_exp.split(':')[1]

    session['domain_age'] = age_function(session['start'])


    # this section handles the user's age
    try:
        session['checked_dob'] = sanity_combine_dob(session['Day'],session['Month'],session['Year'])
    except AttributeError:
        return render_template('error.html', error_message = "Please enter a your DOB in a compatable format.",
                                             further_explanation = "Did you miss a field? 'username=&day=dd&month=mm&year=yyyy&domain_name=' is currently the only accepted format.")
    try:
        session['age'] = age_function(session['checked_dob'])
    except ValueError:
        return render_template('error.html', error_message = "Please enter an existing DOB",
                                             further_explanation = "The DOB you entered does not exist,<br> it is likely that you entered a DOB such as 30 Feb, 31 Apr.")

    # calculate the age difference between the user and the domain they entered to be returned to them
    session['age_difference'] = int(session['age']) - int(session['domain_age'])

    # determining what phrase to use to describe the age difference
    if int(session['age_difference']) > 1:
        session['older_younger'] = "years older than"
    elif int(session['age_difference']) < -1:
        session['older_younger'] = "years younger than"
        session['age_difference'] = -int(session['age_difference'])
    elif int(session['age_difference']) == 0:
        session['older_younger'] = "the same age as"
        session['age_difference'] = ""
    elif int(session['age_difference']) == 1:
        session['older_younger'] = "year older than"
    elif int(session['age_difference']) == -1:
        session['older_younger'] = "year younger than"
        session['age_difference'] = -int(session['age_difference'])

    # passing variables to the results template to give the dynamic output
    return render_template('results.html', username = session['name'],
                                           your_age = session['age'],
                                           domain_name = session['checked_domain'],
                                           regestered = session['start'],
                                           expires = session['exp'],
                                           domain_age = session['domain_age'],
                                           age_difference = session['age_difference'],
                                           older_younger = session['older_younger'])

if __name__ == '__main__':
    application.run()
