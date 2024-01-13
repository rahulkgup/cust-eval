
def modelOut(summary, n):

    return summary.tail(n).applymap(lambda x: round(x, 6))

