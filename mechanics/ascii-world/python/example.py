def render(rows, player=None):
    if any(len(row)!=len(rows[0]) for row in rows): raise ValueError("ragged map")
    tiles={0:'.',1:'#'}
    return '\n'.join(''.join('@' if player==(x,y) else tiles[tile]
        for x,tile in enumerate(row)) for y,row in enumerate(rows))
