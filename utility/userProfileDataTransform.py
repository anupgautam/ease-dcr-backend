import uuid

def user_profile_data_transmission(request, data):
    final_data = {}
    if len(data['initial_data']) !=0:
        for i in data['initial_data']:
            final_data[i] = request.data.get(i) 
    foreignData = {}
    if len(data['foreign_key']) != 0:
        for i in data['foreign_key']:
            if not foreignData.get(i['key_name']):
                foreignData[i['key_name']] = {}
            for j in i['key_value']:
                foreignData[i['key_name']][j] = request.data.get(j)
            if len(i['extra_value']) != 0:
                for j in i['extra_value']:
                    foreignData[i['key_name']][j['name']] = j['value']
    final_data.update(foreignData)
    return final_data