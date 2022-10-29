#define PY_SSIZE_T_CLEAN
#include <Python.h>
static PyObject *ShmQueueError;

static PyObject *
shmqueue_create_queue(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = 0;
    if (sts < 0) {
        PyErr_SetString(SpamError, "System command failed");
        return NULL;
    }
    return PyLong_FromLong(sts);
}
static PyObject *
shmqueue_destroy_queue(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = 0;
    if (sts < 0) {
        PyErr_SetString(SpamError, "System command failed");
        return NULL;
    }
    return PyLong_FromLong(sts);
}
static PyObject *
shmqueue_enqueue(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = 0;
    if (sts < 0) {
        PyErr_SetString(SpamError, "System command failed");
        return NULL;
    }
    return PyLong_FromLong(sts);
}

static PyMethodDef SpamMethods[] = {
    {"create_queue",  shmqueue_create_queue, METH_VARARGS,
     "creare a shared memory queue."},
     {"destroy_queue",  shmqueue_destroy_queue, METH_VARARGS,
     "destroy a shared memory queue."},
     {"enqueue_queue",  shmqueue_enqueue, METH_VARARGS,
     "destroy a shared memory queue."},
     {"dequeue_queue",  shmqueue_enqueue, METH_VARARGS,
     "destroy a shared memory queue."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef shmqueuemodule = {
    PyModuleDef_HEAD_INIT,
    "spam",   /* name of module */
    spam_doc, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    SpamMethods
};
PyMODINIT_FUNC
PyInit_spam(void)
{
    PyObject *m;

    m = PyModule_Create(&shmqueuemodule);
    if (m == NULL)
        return NULL;

    ShmQueueError = PyErr_NewException("", NULL, NULL);
    Py_XINCREF(SpamError);
    if (PyModule_AddObject(m, "error", SpamError) < 0) {
        Py_XDECREF(SpamError);
        Py_CLEAR(SpamError);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
