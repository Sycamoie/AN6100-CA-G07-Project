from Utils import UndefinedVariable

# get global variablies for the function that
def exposeGlobalVar(global_variable={}):
    def _exposeGlobalVar(function):
        def __exposeGlobalVar(*args, **kw):
            global PCno 
            Pcno = global_variable.get('PCno')
            global gateID 
            gateID = global_variable.get('gateID')

            if PCno is None:
                raise UndefinedVariable('PCno')
                PCno = -1
            if gateID is None:
                raise UndefinedVariable('gateID')
                gateID = '.'
            
            return function(*args, **kw)
        return __exposeGlobalVar
    return _exposeGlobalVar