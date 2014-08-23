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

/* update({str: double} target, {str: double} source, double multiplier)
 *
 * Update a target set of sparse weights using a source set of sparse weights.
 * After this function has completed, the keys in target will be the union of
 * the keys in target and the keys in source, and the values in target will be
 * the sums of the values for the corresponding keys in target and source.
 * Source is not modified. Equivalent to the following Python:
 *
 * >>> for key, value in source.iteritems():
 * ...   target[key] = target.get(key, 0) + multiplier * value
 *
 * Both target and source should be dictionaries mapping strings (features) to
 * floats (weights). The multiplier should be a float.
 */
static PyObject *
update(PyObject *self, PyObject *args)
{
    PyObject *dst, *src, *k, *v, *x;
    Py_ssize_t i = 0;
    double mul, acc;
    char *key;

    if (!PyArg_ParseTuple(args, "OOd", &dst, &src, &mul))
        return NULL;
    while (PyDict_Next(src, &i, &k, &v)) {
        if (!PyString_Check(k)) return NULL;
        key = PyString_AsString(k);
        if (!PyFloat_Check(v)) return NULL;
        acc = mul * PyFloat_AS_DOUBLE(v);
        x = PyDict_GetItemString(dst, key);
        if (x != NULL)
            acc += PyFloat_AS_DOUBLE(x);
        PyDict_SetItemString(dst, key, PyFloat_FromDouble(acc));
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef SparseMethods[] = {
    {"dot", dot, METH_VARARGS,
     "Sum a feature vector against a sparse weight dictionary."},
    {"update", update, METH_VARARGS,
     "Update one sparse weight dictionary using the values in another."},
    {NULL, NULL, 0, NULL} /* sentinel */
};

PyMODINIT_FUNC
init_sparse(void)
{
    (void) Py_InitModule("_sparse", SparseMethods);
}
