def correct_word(word, vocabulary):

    # exact match
    if word in vocabulary:
        return word

    # simple edit distance (1-step tolerance)
    def is_close(w1, w2):
        if abs(len(w1) - len(w2)) > 1:
            return False

        mismatches = 0
        i = j = 0

        while i < len(w1) and j < len(w2):
            if w1[i] != w2[j]:
                mismatches += 1
                if mismatches > 1:
                    return False

                # skip one char
                if len(w1) > len(w2):
                    i += 1
                elif len(w2) > len(w1):
                    j += 1
                else:
                    i += 1
                    j += 1
            else:
                i += 1
                j += 1

        return True

    # find closest match
    for v in vocabulary:
        if is_close(word, v):
            return v

    return word