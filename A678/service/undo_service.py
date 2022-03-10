class UndoService:
    def __init__(self):
        self._history = []
        self._index = -1

    def add_operation(self, operation):
        # When recording a new operation, discard all previous undos
        #self._history = self._history[0:self._index + 1]
        self._history.append(operation)
        self._index = len(self._history) - 1

    def undo(self):
        """
        If list is empty(index is -1) no undos can be done
        :return:
        """
        if self._index == -1:
            raise ValueError("\n No more undos! \n")
        try:
            self._history[self._index].undo()
            self._index -= 1
        except:
            self._index -= 1


    def redo(self):
        """
        If the list is full (index = len(list) - 1) no undos have been performed
        yet, so we cannot do any redos
        :return:
        """
        if self._index == len(self._history) - 1:
            raise ValueError("\n No more redos! \n")

        self._index += 1
        self._history[self._index].redo()

class CascadedOperation:
    def __init__(self, *operations):
        self._operations = operations

    def undo(self):
        # TODO Check order of operations in cascaded undo/redo
        for oper in self._operations:
            oper.undo()

    def redo(self):
        # TODO Check order of operations in cascaded undo/redo
        for oper in self._operations:
            oper.redo()


class Operation:
    def __init__(self, funct_call_undo, funct_call_redo):
        self._funct_call_undo = funct_call_undo
        self._funct_call_redo = funct_call_redo

    def undo(self):
        self._funct_call_undo()

    def redo(self):
        self._funct_call_redo()


class FunctionCall:
    def __init__(self, function_reference, *function_params):
        self._function_reference = function_reference
        self._function_params = function_params

    def call(self):
        return self._function_reference(*self._function_params)

    def __call__(self):
        return self.call()