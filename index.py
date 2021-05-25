import re


def get_variable(variable_name, count):
    f = open("Variables/" + variable_name + ".txt", "r")
    content = f.readlines()
    return content[count].replace("\n", "")


email_list_file = open("variables/email.txt", "r")

count = 0

for email in email_list_file:
    email = email.replace("\n", "")

    body = 'A for <<email>>, b means <<name>>, and c could be <<name>>.'

    print(re.sub(r'<<([^>]*)>>',
                 lambda m: get_variable(m.group(1), count), body))
    count += 1
