from lightflow.models import Dag, Action
from lightflow.tasks import PythonTask


def first_call(name, data, data_store, signal):
    data_store.set('number', 5)
    data_store.set('buffer.observable', 20)
    data_store.push('sample.spectra', 7)

    return Action(data)


def second_call(name, data, data_store, signal):
    number = data_store.get('number')
    data_store.set('number', number*10)
    data_store.push('filenames', 'file_a.spec')

    signal.run_dag(name)


def third_a_call(name, data, data_store, signal):
    data_store.push('filenames', 'file_b.spec')


def third_b_call(name, data, data_store, signal):
    data_store.push('filenames', ['nested_a', 'nested_b'])
    data_store.extend('filenames', ['file_c.spec', 'file_d.spec'])


d = Dag('myDag')

first = PythonTask(name='first',
                   python_callable=first_call)

second = PythonTask(name='second',
                    python_callable=second_call)

third_a = PythonTask(name='third_a',
                     python_callable=third_a_call)

third_b = PythonTask(name='third_b',
                     python_callable=third_b_call)

d.define_workflow({first: [second], second: [third_a, third_b]})
