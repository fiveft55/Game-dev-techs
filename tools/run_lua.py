"""Run a Lua file using a system Lua 5.4 shared library when lua CLI is absent.

The mechanic modules themselves are standard Lua; this is only a test launcher.
"""
import ctypes
import ctypes.util
import sys


def run(path):
    library = ctypes.util.find_library('lua5.4')
    if not library:
        raise RuntimeError('Install Lua 5.4 (CLI or shared library)')
    lua = ctypes.CDLL(library)
    lua.luaL_newstate.restype = ctypes.c_void_p
    lua.luaL_openlibs.argtypes = [ctypes.c_void_p]
    lua.luaL_loadfilex.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
    lua.luaL_loadfilex.restype = ctypes.c_int
    lua.lua_pcallk.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_ssize_t, ctypes.c_void_p]
    lua.lua_pcallk.restype = ctypes.c_int
    lua.lua_tolstring.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
    lua.lua_tolstring.restype = ctypes.c_char_p
    lua.lua_close.argtypes = [ctypes.c_void_p]
    state = lua.luaL_newstate()
    if not state:
        raise RuntimeError('Lua state allocation failed')
    try:
        lua.luaL_openlibs(state)
        status = lua.luaL_loadfilex(state, str(path).encode(), None)
        if status == 0:
            status = lua.lua_pcallk(state, 0, 0, 0, 0, None)
        if status:
            raise RuntimeError(lua.lua_tolstring(state, -1, None).decode())
    finally:
        lua.lua_close(state)


if __name__ == '__main__':
    run(sys.argv[1])
