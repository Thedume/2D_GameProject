hurdle_distance = [13.72, 8.5, 8.5, 8.5, 8.5, 8.5, 8.5, 8.5, 8.5, 8.5, 14.02]
h_pix_distance = []
dis = 0
for distance in hurdle_distance:
    dis += distance * 33
    h_pix_distance.append(dis)

print(h_pix_distance)