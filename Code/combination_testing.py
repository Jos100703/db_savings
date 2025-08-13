
num_bs = 4
final_res = [[] for _ in range(num_bs)]

def combination_test(start,goal):
    av_trav = [i for i in range(start+1, goal+1)]
    temp_res = []

    for end in av_trav:
        if end == goal:
            final_res[start-1].append((temp_res))
        else:
            temp_res.append((start, end))
            while temp_res[-1][1] <= goal:
                temp_res.append(combination_test(end, goal))

    return (start,end)            


combination_test(1,4)



assert final_res == [[(1,2),(2,3),(3,4)],[(1,2),(2,4)],[(1,3),(2,4)],[(1,4)] ], "Combination test failed, check the logic in combination_test function."