"""Match-three detection and gravity. Original MIT-licensed educational implementation."""

def matches(board, minimum=3):
    if type(minimum) is not int or minimum < 2: raise ValueError("invalid run length")
    width=len(board[0]) if board else 0
    if any(len(row)!=width for row in board): raise ValueError("ragged board")
    result=set()
    lines=[[(x,y) for x in range(width)] for y in range(len(board))]
    lines += [[(x,y) for y in range(len(board))] for x in range(width)]
    for line in lines:
        start=0
        while start < len(line):
            x,y=line[start]; value=board[y][x]; end=start+1
            while end<len(line) and board[line[end][1]][line[end][0]] == value: end+=1
            if value is not None and end-start >= minimum: result.update(line[start:end])
            start=end
    return result

def clear_and_fall(board, cells):
    width=len(board[0]) if board else 0
    if any(len(row)!=width for row in board): raise ValueError("ragged board")
    cells=set(cells)
    if any(not (0<=x<width and 0<=y<len(board)) for x,y in cells):
        raise ValueError("cell outside board")
    result=[[None]*width for _ in board]
    for x in range(width):
        survivors=[board[y][x] for y in range(len(board)) if (x,y) not in cells and board[y][x] is not None]
        # Write survivors at the bottom without reversing their order.
        for y,value in enumerate(survivors,len(board)-len(survivors)): result[y][x]=value
    return result
