"""
    An email address is sometimes in the form 
        john@example.com
    And at other times
        John Smith <john@example.com>
    This will normalize it to 
        john@example.com
"""
def simplifyEmail(e):
    if "<" in e:
        left, right = e.split("<")
        e = right.replace(">", "")
    return e