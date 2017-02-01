records = []

typechs = []

lengths = []

fields = []


def load(filename):

    global records

    global typechs

    global lengths

    global fields


    try:

        with open(filename, 'r') as file:

            fields = file.readline().rstrip().split(':')

            lengths = file.readline().rstrip().split(':')

            typechs = file.readline().rstrip().split(':')


            for line in file:

                line = line.rstrip()

                if line:

                    record = line.split(':')

                    records.append(record)

    except FileNotFoundError:

        return -1


def save(filename):

    global records

    global typechs

    global lengths

    global fields


    data = ''


    for f in fields: data += f + ':'

    data = data[:-1] + '\n'

    for l in lengths: data += l + ':'

    data = data[:-1] + '\n'

    for tc in typechs: data += tc + ':'

    data = data[:-1] + '\n'


    for record in records:

        for field in record: data += field + ':'

        data = data[:-1] + '\n'


    with open(filename, 'w') as file:

        file.write(data)


def search(id):

    global records


    i = 0

    for record in records:

        if int(record[0]) == int(id): return i 

        i += 1


    return -1 

            
def add(record):

    global records


    i = search(int(record[0]))

    if not i == -1: return -1


    records.append(record)


    return search(int(record[0])) 


def remove(id):

    global records


    i = search(id)

    if i == -1: return -1


    update = records[:i]

    update += records[i+1:]


    records = update


    return i 

