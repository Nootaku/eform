def replaceInString(p, f, r):
    """Creates a find and replace function within any given string. Only
    replace the first occurence.

    Arguments:
            - p: the original string where a replacement should take place
            - f: what needs to be replaced
            - r: what it should be replaced with

    Output:
            - New_string: string with replaced value.
    """
    if r is not None:
        if p.find(f) != -1 and r != "":
            split = p.split(f)
            new_p = ""
            for i in split:
                new_p += i
                new_p += r
            new_p = new_p[0: -int(len(r))]

            return new_p

        else:
            return p

    else:
        print("HEEEEEEERREEEEEE")
        print(p)
        new_p = p.replace(f, "")
        if new_p != "":
            return new_p
        else:
            return None
