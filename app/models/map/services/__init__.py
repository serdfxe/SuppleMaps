def get_len(path, mtrx):
    #for i in range(1, len(path)): print(path[i-1], path[i], mtrx[path[i]][path[i-1]])
    return sum(mtrx[path[i]-1][path[i-1]-1] for i in range(1, len(path)))

def time_to_dist(time): return time*83

def dist_to_time(time): return time/83

def filter_ans(ans, n_of_ans):
    ans = sorted(ans, key = lambda t: (-len(t[0]), t[1]))
    ans1 = [ans[0]]
    for i in range(1, len(ans)):
        if len(ans1) == n_of_ans: break
        if all(set(ans1[j][0]).intersection(set(ans[i][0])) != set(ans[i][0]) for j in range(len(ans1))) and ans[i] not in ans1: 
            ans1.append(ans[i])
    return ans1

def get_path(mtrx, poi, time_s, time_limit = 10**5, mandatory_points = [1], dur_of_visit = False, n_of_ans = 1, temp_path = [1],temp_time=0, ans = [], depth = 0, best_time=10**5, best_path = []):
    #breaks
    if time_limit != 10**5 and (len(temp_path) < len(best_path) and temp_time > best_time):
        return ans, best_time, best_path
    
    if time_limit == 10**5 and temp_time > best_time:
        return ans, best_time, best_path

    #wins
    if len(temp_path) == len(poi)+1 and temp_time <= time_limit  and all(point in temp_path for point in mandatory_points):
        if len(temp_path) == len(best_path) and temp_time < best_time or (len(temp_path) > len(best_path)):
            best_time = temp_time
            best_path = temp_path
        full_time = int(temp_time) + (1-dur_of_visit)*sum(time_s[point-1] for point in temp_path)
        walk_time = int(temp_time) - dur_of_visit*sum(time_s[point-1] for point in temp_path)
        ans.append((tuple(temp_path), (full_time, walk_time), int(time_to_dist(temp_time - dur_of_visit*sum(time_s[point-1] for point in temp_path)))))
        # ans.append((tuple(temp_path),dist_to_time(get_len(temp_path, mtrx)), get_len(temp_path, mtrx)))
        return ans, best_time, best_path

    if time_limit != 10**5 and temp_time > time_limit and all(point in temp_path[:-1] for point in mandatory_points):
        path = temp_path[:-1]
        time = temp_time - dist_to_time(mtrx[temp_path[-2]-1][temp_path[-1]-1])
        if dur_of_visit: time -= time_s[temp_path[-1]-1]
        if time > time_limit: return ans, best_time, best_path
        if len(path) > len(best_path) or (len(path) == len(best_path) and time < best_time):
            best_path = path
            best_time = time
        full_time = int(time) + (1-dur_of_visit)*sum(time_s[point-1] for point in path)
        walk_time = int(time) - dur_of_visit*sum(time_s[point-1] for point in path)
        ans.append((tuple(path), (full_time, walk_time), int(time_to_dist(time - dur_of_visit*sum(time_s[point-1] for point in path)))))
        return ans, best_time, best_path

    
        #print(*temp_path, temp_time)
    
    for nxt_node in poi:
        if nxt_node in temp_path: continue
        #print(temp_path, nxt_node)
        nxt_path = temp_path + [nxt_node]
        nxt_time = temp_time + dist_to_time(mtrx[temp_path[-1]-1][nxt_node-1])
        if dur_of_visit: nxt_time += time_s[nxt_node-1]
        ans, best_time, best_path = get_path(mtrx,poi,time_s,time_limit,mandatory_points,dur_of_visit,n_of_ans,nxt_path,nxt_time,ans,depth+1,best_time,best_path)
    if depth == 0:
        #print(*mtrx, sep='\n')
        if time_limit == 10**5: return ans[-1:(-1)*(n_of_ans+1):-1]
        else: return filter_ans(ans, n_of_ans)
    else:
        return ans, best_time, best_path
