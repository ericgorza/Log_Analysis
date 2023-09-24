import operator
import re
import csv

filename = "syslog.log"

errors = {}
users = {}


## Abrir o file e contar quantos erros e quantos INFO

with open(filename, "r") as logfile:

    for line in logfile:

        #Separar os erros e info de cada linha, contar e criar um dicionario.
        error = re.search(r'ERROR: ', line)
        info = re.search(r'INFO: ', line)

        padrao = r'\((.*?)\)'
        username = re.search(padrao, line)
        new_username = str(username[1])

        padrao_error_message = r'(ERROR: .*)\('
        error_message = re.search(padrao_error_message,line)

        # Criar o dicionario com os erros e contagens:

        if error_message:
            error_text = str(error_message[0].strip(" ("))
            if error_text not in errors:
                errors[error_text] = 1
            elif error_text in errors:
                errors[error_text]+= 1
        else:
            pass


        # Criar o dicionario com os usernames e contagens:


        if new_username not in users:
            users[new_username] = [0,0]
            if error:
                users[new_username][1]+=1
            if info:
                users[new_username][0]+=1

        elif new_username in users:

            if error:
                users[new_username][1]+=1
            if info:
                users[new_username][0]+=1


## Criar o dicionario per user com o Tuple ao inves de lista:

per_user={}

for key in users.keys():
    per_user[key]=users[key][0],users[key][1]

print(per_user)

## Criar o dicionario sorted para users

sorted_user = sorted(per_user.items(), key=operator.itemgetter(0))
print(sorted_user)


## Criar o dicionario sorted para erros:

sorted_errors = sorted(errors.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_errors)

#Criar o CSV para erros error_message.csv

header_errors = ("Error","Count")

with open("error_message.csv", "w") as error_csv:
    writer = csv.writer(error_csv)
    writer.writerow(header_errors)
    writer.writerows(sorted_errors)

#Criar o CSV para erros error_message.csv

header_users=("Username","INFO","ERROR")
user_list=[]

for user in sorted_user:
    # print(user)
    csv_username=str(user[0])
    # print(csv_username)
    csv_info=str(user[1][0])
    # print(csv_info)
    csv_error=str(user[1][1])
    # print(csv_error)
    tuple_user_csv=(csv_username,csv_info,csv_error)
    # print(tuple_user_csv)
    user_list.append(tuple_user_csv)

# print(user_list)

with open("user_statistics.csv", "w") as user_csv:
    writer_user = csv.writer(user_csv)
    writer_user.writerow(header_users)
    writer_user.writerows(user_list)