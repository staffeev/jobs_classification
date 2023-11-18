proccessed = [pool.apply_async(r.get_data) for r in resumes_list]
    # proccessed = [i.get() for i in proccessed]