from mpi4py import MPI

def enum(*sequential, **named):
    """Handy way to fake an enumerated type in Python
    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# Define MPI message tags
tags = enum('READY', 'DONE', 'EXIT', 'START')

# Initializations and preliminaries
comm = MPI.COMM_WORLD   # get MPI communicator object
size = comm.Get_size()  # total number of processes
rank = comm.Get_rank()  # rank of this process
name = MPI.Get_processor_name()
status = MPI.Status()   # get MPI status object

if rank == 0:
    # Master process executes code below
    tasks = range(2*size)
    task_index = 0
    num_workers = size - 1
    closed_workers = 0
    print("Master starting with {} workers".format(num_workers))
    while closed_workers < num_workers:
        data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        source = status.Get_source()
        tag = status.Get_tag()
        if tag == tags.READY:
            # Worker is ready, so send it a task
            if task_index < len(tasks):
                comm.send(tasks[task_index], dest=source, tag=tags.START)
                print("Sending task {} to worker {}".format(task_index, source))
                task_index += 1
            else:
                comm.send(None, dest=source, tag=tags.EXIT)
        elif tag == tags.DONE:
            results = data
            print("Got data from worker {}".format(source))
        elif tag == tags.EXIT:
            print("Worker {} exited.".format(source))
            closed_workers += 1

    print("Master finishing")
else:
    # Worker processes execute code below
    print("I am a worker with rank {} on {}.".format(rank, name))
    while True:
        comm.send(None, dest=0, tag=tags.READY)
        task = comm.recv(source=0, tag=MPI.ANY_SOURCE, status=status)
        tag = status.Get_tag()

        if tag == tags.START:
            # Do the work here
            result = task**2
            comm.send(result, dest=0, tag=tags.DONE)
        elif tag == tags.EXIT:
            break

    comm.send(None, dest=0, tag=tags.EXIT)
