def get_location(values):
    before, sep, after = values.partition(':')
    if len(after) > 0:
        values = after
        remove_x = values.replace('X=', '')
        remove_y = remove_x.replace('Y=', '')
        final = remove_y.replace('Z=', '')
        return final


print(get_location("อ.เอ็มไงจะใครล่ะ: X=-902642.063 Y=-287250.375 Z=21641.670"))
