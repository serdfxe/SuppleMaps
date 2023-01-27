from itertools import permutations


def time_to_len(time): return time*83

def dist_to_time(dist): return dist/83

def get_len(path, mtrx): return sum(mtrx[path[i]][path[i-1]] for i in range(1, len(path)))

def get_time(path, mtrx, time_s, dur_of_visit = True):
    return dist_to_time(get_len(path, mtrx)) + dur_of_visit * sum(time_s[i] for i in path)

def get_path(mtrx, poi, time_s, time_limit = 10**10, mandatory_points = [], dur_of_visit = True, n_of_ans = 1):
    mn_time = 10**10
    mn_path = list()
    ans = list()
    ans_s = set()

    for p in permutations(sorted(poi)):
        full_path = [0] + list(p)
        temp_path = full_path
        temp_time = 0

        for i in range(1, len(full_path)):
            temp_time += dist_to_time(mtrx[full_path[i]][full_path[i-1]])

            if dur_of_visit: temp_time += time_s[i]

            if temp_time > min(mn_time, time_limit):
                temp_time -= dist_to_time(mtrx[full_path[i]][full_path[i-1]])
                if dur_of_visit: temp_time -= time_s[i]
                temp_path = full_path[:i]
                break
            
        if temp_time <= time_limit and all(point in temp_path for point in mandatory_points) and tuple(temp_path) not in ans_s:
            ans.append(temp_path)
            ans_s.add(tuple(temp_path))

            if len(temp_path) >= len(mn_path) and temp_time <= mn_time:
                mn_time = temp_time
                mn_path = temp_path

    ans = sorted(ans, key = lambda x: (-len(x), get_time(x, mtrx, time_s, dur_of_visit=dur_of_visit)))

    ans1 = [ans[0]]

    for i in range(1, len(ans1)):
        if set(ans1[0]).intersection(set(ans[i])) != set(ans[i]): 
            ans1.append(ans[i])
            if len(ans1) == n_of_ans: break

    return ans1
