num_hs = 5

# def all_combs(start,goal):
start = 1
goal = 4

all_poss = [[[1]] for _ in range(start,goal) ]
min_start = list(range(start,goal+1))
av_routes = [list(range(min_start_ind+1,goal+1)) for min_start_ind in min_start]


for index,interm_goals in enumerate(av_routes):
    
    for poss in all_poss:
        while interm_goals:
            interm_goal = interm_goals.pop(0)

            if all_poss == [[[1], [1, 2]], [[1], [1, 3]], [[1], [1, 4]]]:
                pass

            if interm_goal > poss[-1][-1]:
                poss.append([poss[-1][-1] ,interm_goal])
                
                if len(interm_goals) > 0:
                    interm_goals.append(interm_goals[0])
                else:
                    break



    # return all_poss

# all_combs(1,num_hs)






assert all_poss == [[(1,2),(2,3),(3,4)],[(1,2),(2,4)],[(1,3),(2,4)],[(1,4)] ], "Combination test failed, check the logic in combination_test function."