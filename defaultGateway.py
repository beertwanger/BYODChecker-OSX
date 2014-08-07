from subprocess import check_output

words = (check_output(["netstat", "-rn"])).split()

for index in range(len(words)):
    if (words[index] == 'default'):
        gateway = words[index+1]


print "Default gateway: ", gateway
