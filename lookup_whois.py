def lookup(domain_name):
    """Input domain name. Return regestered date, expiry date"""
    import re
    import subprocess
    import whois
    import datetime


    # checking the top level domain to determine which regex should be used
    try:
        whois_domain = whois.query(str(domain_name))
    except:
        pass
    else:
        if whois_domain.__dict__ != None:
            if whois_domain.creation_date != None:
                if whois_domain.expiration_date != None:
                    return("{}:{}".format(whois_domain.creation_date.date(), whois_domain.expiration_date.date()))
                else:
                    return("{}:{}".format(whois_domain.creation_date.date(), "an unknown date"))

    # since the library doesn't support the creation date of the tld or it couldn't be found at all, call a shell
    # setting variables to check when a date is found
    created = None
    expires = None
    # whois.tmp is used as I wanted to read from files in python
    subprocess.call("whois {} > ../tmp/whois.tmp".format(domain_name), shell=True)
    f = open("../tmp/whois.tmp")
    line = f.readline()
    # test for .org domains, other tld's could be added if the whois output has the same layout
    if re.match(r""".*\.org$""", domain_name):
        while len(line):
            cre = re.match(r""".*Creation Date: (\d\d\d\d-\d\d-\d\d).*""", line)
            exp = re.match(r""".*Registry Expiry Date: (\d\d\d\d-\d\d-\d\d).*""", line)
            line = f.readline()
            if cre != None:
                created = cre.group(1)
            if exp != None:
                expires = exp.group(1)
    # test for other broken tld's  could be added, the layout of the whois output would need to be observed
    # a domain without a creation date is meaning less to the app
    if created == None:
        raise AttributeError("Domain not found")
    # a domain without an expiry date is acceptable
    if expires == None:
        expires = "an unknown date"
    return("{}:{}".format(created, expires))

