import inspect
import torch
from lintorch.core.editable_module import EditableModule

def wrap_fcn(fcn, params):
    nparams = len(params)

    if not inspect.ismethod(fcn) and not inspect.isfunction(fcn):
        if hasattr(fcn, "__call__"):
            fcn = fcn.__call__
        else:
            raise RuntimeError("The function must be callable")

    if inspect.ismethod(fcn) and isinstance(fcn.__self__, EditableModule):
        obj = fcn.__self__
        method_name = fcn.__name__
        def wrapped_fcn(*all_params):
            params = all_params[:nparams]
            obj_params = all_params[nparams:]
            with obj.useparams(method_name, *obj_params) as model:
                res = getattr(model, method_name)(*params)
            return res

        # get all the parameters
        obj_params = obj.getparams(method_name)
        all_params = [*params, *obj_params]
    else:
        wrapped_fcn = fcn
        all_params = params
    return wrapped_fcn, all_params
