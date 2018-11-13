id = 69
end_index = "KONIEC"


def import_connections(dir="local", start_index="id=", end_index="id="):
    if dir == "local":
        data_file = open("test.txt")
    else:
        data_file = open(dir)
    block = []
    found = False
    find = start_index + str(id)
    for line in data_file:
        if found:
            if line.strip().startswith(end_index): break
            block.append(line)
        else:
            if line.strip() == find:
                found = True

    data_file.close()
    print(block[1])
import_connections()
#why wont you push it??
#argghhh
#git updated
#whyyy
#dlaczego