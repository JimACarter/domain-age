def sanity_domain(domain):
    """Input url or domain name.  Return the domain name without other characters"""
    import re
    matched = re.match(r"""(?:.*[\.\/])?((?:[0-9\-A-z]+)(?:\.com|\.co_jp|\.cz|\.at|\.eu|\.ru|\.lv|\.nz|\.net|\.pl|\.be|\.fr|\.de|\.jp|\.me|\.biz|\.info|\.name|\.us|\.it|\.co|\.org|\.uk){2})(?:\/.*)?""", domain)
    if not matched:
        matched = re.match(r"""(?:.*[\.\/])?((?:[0-9\-A-z]+)(?:\.com|\.co_jp|\.cz|\.at|\.eu|\.ru|\.lv|\.nz|\.net|\.pl|\.be|\.fr|\.de|\.jp|\.me|\.biz|\.info|\.name|\.us|\.it|\.co|\.org|\.uk))(?:\/.*)?""", domain)


#    matched = re.match(r"""(?:(?:[:\/0-9\-A-z]+\/)|(?:[:\/0-9\-A-z]+\.))?((?:[0-9\-A-z]+\.)(?:com|co_jp|cz|at|eu|ru|lv|nz|net|pl|be|fr|de|jp|me|biz|info|name|us|it|co|org)(?:\/.*)?""", domain)
#    if matched == None:
#        matched = re.match(r"""(?:(?:[:\/0-9\-A-z]+\/)|(?:[:\/0-9\-A-z]+\.))?((?:[0-9\-A-z]+\.)(?:uk))(?:\/.*)?""", domain)

    try:
        san_domain = matched.group(1)
    except AttributeError:
        raise AttributeError("Domain not recongised")
    return(san_domain)

def sanity_combine_dob(day, month, year):
    """Check day month and year are numbers. Return them in the form dd-mm-yyyy"""
    import re
    d = re.match(r"""(\d\d?)""", day)
    m = re.match(r"""(\d\d?)""", month)
    y = re.match(r"""(\d\d\d\d)""", year)
    try:
        san_day = d.group(1)
        san_month = m.group(1)
        san_year = y.group(1)
    except AttributeError as e:
        raise AttributeError("Input was not in format dd-mm-yyyy{}". format(e))
    return("{}-{}-{}". format(san_year, san_month, san_day))
