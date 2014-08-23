#include <Python.h>

/* int dot({str: float} weights, (str) features)
 *
 * Compute the dot product of a feature vector against a sparse weight
 * dictionary. About three times faster than the equivalent Python:
 *
 * >>> sum(weights.get(f, 0) for f in features)
 *
 * Weights should be a dictionary mapping strings (features) to floats
 * (weights). Features should be a tuple containing a sequence of strings
 * (features).
 */
static PyObject *
dot(PyObject *self, PyObject *args)
{
    PyObject *map, *tup, *keys, *value;
    Py_ssize_t i = 0;
    double acc = 0.0;

    if (!PyArg_ParseTuple(args, "OO", &map, &tup))
        return NULL;
    keys = PySequence_Fast(tup, "features must be a tuple of strings");
    for (i = 0; i < PySequence_Fast_GET_SIZE(keys); ++i) {
        value = PyDict_GetItemString(map,
            PyString_AsString(PySequence_Fast_GET_ITEM(keys, i)));
        if (value != NULL)
            acc += PyFloat_AS_DOUBLE(value);
    }
    Py_DECREF(keys);
    return (PyObject *) PyFloat_FromDouble(acc);
}

static PyMethodDef SparseMethods[] = {
    {"dot", dot, METH_VARARGS,
     "Sum a feature vector against a sparse weight dictionary."},
    {NULL, NULL, 0, NULL} /* sentinel */
};

PyMODINIT_FUNC
init_sparse(void)
{
    (void) Py_InitModule("_sparse", SparseMethods);
}
