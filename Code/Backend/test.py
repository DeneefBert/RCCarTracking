from repositories.DataRepository import DataRepository

test = DataRepository.request_data(1, 10)
test2 = DataRepository.request_data(2, 10)
test3 = DataRepository.request_data(3, 10)

res = []

for i in test:
    for j in test2:
        for k in test3:
            if (k['date'] == j['date']) and (k['date'] == i['date']):
                res.append({"date" : k['date'], "acc" : i["value"], "ldr" : j["value"], "temp" : k["value"]})

print(res)