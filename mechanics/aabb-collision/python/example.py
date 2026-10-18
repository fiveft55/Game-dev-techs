def overlaps(a, b):
    if a[2] < 0 or a[3] < 0 or b[2] < 0 or b[3] < 0:
        raise ValueError("negative dimensions")
    # A separating interval on either axis rules out contact.
    return (a[0] <= b[0]+b[2] and b[0] <= a[0]+a[2]
            and a[1] <= b[1]+b[3] and b[1] <= a[1]+a[3])
