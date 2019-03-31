import ujson

def sum_values_in_data(data):
    s = 0
    for k, v in data.iteritems():
        s += int(v)
    return s

def sort_by_value(data, top_value=None):
    if top_value:
        return sorted(data, key=lambda x: x[1], reverse=True)[:top_value]
    return sorted(data, key=lambda x: x[1], reverse=True)

with open('green_pickup_dropoff_data.json', "r") as data:
    green_loaded_data = ujson.load(data)
    green_loaded_data_list = green_loaded_data.items()

with open('yellow_pickup_dropoff_data.json', "r") as data:
    yellow_loaded_data = ujson.load(data)
    yellow_loaded_data_list = green_loaded_data.items()

print "________Green Taxi________"
print "There are {} dropoffs in the morning".format(sum_values_in_data(green_loaded_data['morning']['dropoff']))
print "There are {} pickups in the morning".format(sum_values_in_data(green_loaded_data['morning']['pickup']))
print "There are {} dropoffs in the evening".format(sum_values_in_data(green_loaded_data['evening']['dropoff']))
print "There are {} pickups in the evening".format(sum_values_in_data(green_loaded_data['evening']['pickup']))
print "Top 5 Pickup ID for morning is:"
print sort_by_value(green_loaded_data['morning']['pickup'].items(), 5)
print "Top 5 Dropoff ID for morning is:"
print sort_by_value(green_loaded_data['morning']['dropoff'].items(), 5)
print "Top 5 Pickup ID for evening is:"
print sort_by_value(green_loaded_data['evening']['pickup'].items(), 5)
print "Top 5 Dropoff ID for evening is:"
print sort_by_value(green_loaded_data['evening']['dropoff'].items(), 5)


print "________Yellow Taxi________"
print "There are {} dropoffs in the morning".format(sum_values_in_data(yellow_loaded_data['morning']['dropoff']))
print "There are {} pickups in the morning".format(sum_values_in_data(yellow_loaded_data['morning']['pickup']))
print "There are {} dropoffs in the evening".format(sum_values_in_data(yellow_loaded_data['evening']['dropoff']))
print "There are {} pickups in the evening".format(sum_values_in_data(yellow_loaded_data['evening']['pickup']))
print "Top 5 Pickup ID for morning is:"
print sort_by_value(yellow_loaded_data['morning']['pickup'].items(), 5)
print "Top 5 Dropoff ID for morning is:"
print sort_by_value(yellow_loaded_data['morning']['dropoff'].items(), 5)
print "Top 5 Pickup ID for evening is:"
print sort_by_value(yellow_loaded_data['evening']['pickup'].items(), 5)
print "Top 5 Dropoff ID for evening is:"
print sort_by_value(yellow_loaded_data['evening']['dropoff'].items(), 5)

