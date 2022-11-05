intersections = [[-1632, 99],[-1632, 99], [-1519, 100], [-1194, 981],[-1194, 981], [-1125, 980], [391, 99], [391, 100], [403, 477], [403, 479], [409, 671], [409, 672], [418, 956], [418, 957], [419, 980], [419, 981], [893, 99], [893, 100], [899, 468], [899, 470], [902, 654], [902, 655], [902, 656], [907, 939], [907, 940], [908, 980], [908, 981], [1158, 99], [1158, 100], [1159, 99], [1159, 100], [1171, 463], [1171, 465], [1171, 466], [1177, 645], [1177, 646], [1177, 647], [1178, 645], [1178, 646], [1178, 647], [1187, 929], [1187, 930], [1188, 929], [1188, 930], [1189, 980], [1189, 981], [1710, 99], [1710, 100], [1713, 99], [1713, 100], [1746, 452], [1747, 99], [1747, 100], [1747, 454], [1747, 456], [1750, 452], [1750, 454], [1750, 456], [1764, 625], [1764, 627], [1765, 627], [1767, 624], [1768, 626], [1768, 627], [1784, 451], [1784, 453], [1784, 455], [1794, 908], [1794, 909], [1797, 908], [1797, 909], [1801, 980], [1801, 981], [1802, 623], [1802, 625], [1802, 626], [1804, 980], [1804, 981], [1820, 450], [1820, 453], [1820, 454], [1820, 623], [1820, 625], [1820, 626], [1820, 907], [1820, 908], [1831, 1100], [1839, 980], [2000, 981]]



print(len(intersections))
def cleanInput():

    intersections.sort(key=lambda intersections:intersections[0])

    threshold = 100
    delete = []
    for i in range(1 , len(intersections)):

        if intersections[i - 1][0] - threshold < intersections[i][0] < intersections[i - 1][0] + threshold:
            if intersections[i - 1][1] - threshold < intersections[i][1] < intersections[i - 1][1] + threshold:
                delete.append(intersections[i])

    for element in delete:
        intersections.remove(element)


cleanInput()
print(len(intersections))
print(intersections)