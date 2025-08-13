start = 1
goal = 10


def all_combs(start,goal):
    path_list = [[start]]
    final_list = []
    while path_list:
        cand = path_list.pop(0)
        pot_ends = list( range(start+1,goal+1))

        while pot_ends:
            end = pot_ends.pop(0)
            if cand[-1] < end:
                interm = cand + [end]

                if end == goal:
                    final_list.append(interm)
                else:
                    path_list.append(interm)

    return final_list

final_list = all_combs(start,goal)
print(final_list)
                

