start = 1
goal = 10

start = 1
goal = 4

all_paths = [[start]]
final_paths = []

while all_paths:
    cand = all_paths.pop(0)

    interm_stop = cand[-1]

    bigger_nums = list(range(interm_stop+1,goal+1))

    new_paths = [cand + [num] for num in bigger_nums]

    interm_paths = [path for path in new_paths if path[-1] < goal ]
    fin_paths= [path for path in new_paths if path[-1] == goal ]

    all_paths.extend(interm_paths)
    final_paths.extend(fin_paths)

print(final_paths)


def all_combs(start:int,goal:int):
    paths = [[start]]
    next_stops = range(2,goal+1)

    while paths:
        cand = paths.pop(0)
        cand_new =[cand + [num] for num in next_stops if num > cand[-1]]
        if not cand_new:
            cand_new = [cand]

        paths.extend(cand_new)


        if set([path[-1] for path in paths]) == {goal}:
            break
  
    return paths

final_res_opt= all_combs([[start]],goal)
print(final_res_opt)




                

