# name=ParameterRandomizer

"""
    Randomize the parameters of the focused effect or generator plugin.
    version:0.1
    author:dustractor
"""

import midi,plugins,ui

RANDOMIZER_PAD = 20
PARAMINFO_PAD = 21
_SEED = 0
_LOCK_D = dict()

channelrack_is_selected = lambda:ui.getFocused(0)
mixer_is_selected = lambda:ui.getFocused(1)
effect_is_selected = lambda:ui.getFocused(6)
generator_is_selected = lambda:ui.getFocused(7)

def setrandomizerpad(n):
    global RANDOMIZER_PAD
    RANDOMIZER_PAD = n

def setrandomizerpad_hex(n):
    global RANDOMIZER_PAD
    RANDOMIZER_PAD = int(f"0x{n}",base=16)

def setparaminfopad(n):
    global PARAMINFO_PAD
    PARAMINFO_PAD = n

def setparaminfopad_hex(n):
    global PARAMINFO_PAD
    PARAMINFO_PAD = int(f"0x{n}",base=16)

def lock(plugname,*paramindex):
    if plugname not in _LOCK_D:
        _LOCK_D[plugname] = set()
    for p in paramindex:
        _LOCK_D[plugname].add(p)
    print(_LOCK_D)

def unlock(plugname,*paramindex):
    if plugname not in _LOCK_D:
        return
    for p in paramindex:
        if p in _LOCK_D[plugname]:
            _LOCK_D[plugname].remove(p)
    print(_LOCK_D)

def OnMidiMsg(event):
    global _SEED
    _M = 2**32
    _A = 1664525
    _C = 1013904223
    event.handled = False
    if event.midiId == midi.MIDI_CONTROLCHANGE:
        if event.data2 > 0:
            if event.data1 == RANDOMIZER_PAD:
                f_id = ui.getFocusedFormID()
                if effect_is_selected():
                    t = f_id // 4194304
                    s = (f_id - 4194304 * t) // 65536
                    if plugins.isValid(t,s):
                        name = plugins.getPluginName(t,s,1)
                        L = plugins.getParamCount(t,s)
                        params = set(list(range(L)))
                        if name in _LOCK_D:
                            for p in _LOCK_D[name]:
                                if p in params:
                                    params.remove(p)
                        for i in params:
                            _SEED = (_A * _SEED + _C) % _M
                            r = _SEED / _M
                            plugins.setParamValue(r,i,t,s)
                elif generator_is_selected():
                    if plugins.isValid(f_id):
                        name = plugins.getPluginName(f_id,-1,1)
                        L = plugins.getParamCount(f_id)
                        params = set(list(range(L)))
                        if name in _LOCK_D:
                            for p in _LOCK_D[name]:
                                if p in params:
                                    params.remove(p)
                        for i in params:
                            _SEED = (_A * _SEED + _C) % _M
                            r = _SEED / _M
                            plugins.setParamValue(r,i,f_id)
                event.handled = True
            elif event.data1 == PARAMINFO_PAD:
                f_id = ui.getFocusedFormID()
                if effect_is_selected():
                    t = f_id // 4194304
                    s = (f_id - 4194304 * t) // 65536
                    if plugins.isValid(t,s):
                        name = plugins.getPluginName(t,s,1)
                        print("name:",name)
                        L = plugins.getParamCount(t,s)
                        for i in range(L):
                            paramname = plugins.getParamName(i,t,s)
                            print(i,paramname)
                elif generator_is_selected():
                    if plugins.isValid(f_id):
                        name = plugins.getPluginName(f_id,-1,1)
                        print("name:",name)
                        L = plugins.getParamCount(f_id)
                        for i in range(L):
                            paramname = plugins.getParamName(i,f_id)
                            print(i,paramname)
                event.handled = True

