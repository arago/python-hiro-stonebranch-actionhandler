from arago.hiro.actionhandler.plugin.stonebranch import Task, TaskInstanceState


class TaskInstance:
    status_desc = {
        'CANCEL_PENDING': 'A process running on the Agent needs to be terminated. When the Cancel command is issued,'
                          ' the task instance will go into a Cancel Pending status until the Agent reports back that'
                          ' the process has been cancelled. At that point, the task instance will transition'
                          ' into the Cancelled status.',
        'EXECUTION_WAIT': 'The task must wait to be completed; either the Agent/Agent Cluster running the task'
                          ' has reached its Task Execution Limit, or the ability of the Agent/Agent Cluster'
                          ' to run tasks has been suspended.',
        'IN_DOUBT': 'The Agent is "in doubt" about the current status of the task instance. This may occur if an Agent'
                    ' or Agent connection goes down. In this case, the Agent restarts and reviews its data about tasks'
                    ' in progress. If the Agent finds a task still running, it resumes normal monitoring.'
                    ' If the Agent cannot find the task, this usually indicates that the task completed,'
                    ' but the Agent considers the task status to be "in doubt."',
        'QUEUED': 'The task has been queued on a resource.',
        'UNDELIVERABLE': 'The Agent is unavailable.',
        'STARTED': 'The task has started. For Agent-based tasks, this means the Agent has received the task.',
        'CANCELLED': 'The task was cancelled by a user.',
        'DEFINED': 'The new task instance has been created (the task has been launched).',
        'EXCLUSIVE_REQUESTED': 'All tasks with a mutually exclusive task defined go immediately to a status of'
                               ' Exclusive Requested. If the task is available to run exclusively, the task then moves'
                               ' to the next appropriate processing status.',
        'EXCLUSIVE_WAIT': 'The task is mutually exclusive with one or more other tasks, and it is waiting for those'
                          ' tasks to finish before it will run.',
        'FINISHED': 'The task was forced by the user to finish. The user may do this in cases where the task had a'
                    ' Cancelled or Failed status, and the user needed to release other task instances depending on the'
                    ' successful completion of this task instance in a workflow. For more information,'
                    ' see Force Finishing a Task.',
        'HELD': 'The task has been put on hold by a user.',
        'RESOURCE_REQUESTED': 'All tasks with a virtual resource defined go immediately to a status'
                              ' of Resource Requested. If the resource is available, the task then moves'
                              ' to the next appropriate processing status.',
        'RESOURCE_WAIT': 'All tasks with a virtual resource defined go immediately to a status'
                         ' of Resource Requested. If the resource is not available, the task goes to a status'
                         ' of Resource Wait. When the resource becomes available, the task moves'
                         ' to the next appropriate processing status',
        'RUNNING': 'The task is running. For Agent-based tasks, the Agent has started running the program.',
        'SKIPPED': 'The task was skipped by a user.',
        'START Failure': 'The task was unable to start.',
        'SUCCESS': 'The task has completed successfully. Workflows will transition to Success status when all of its'
                   ' tasks have transitioned to Success, Finished, or Skipped status.',
        'WAITING': 'The task has been loaded by a workflow and is waiting on a predecessor.',
        'TIME_WAIT': 'The task is waiting to start based on a Wait To Start and/or Delay On Start specification.',
        'FAILED': 'The task ran to a failure status.',
        'ACTION_REQUIRED': 'When a manual task launches, it goes into Action Required status, meaning a user'
                           ' must perform some manual activity. For details, see Manual task.',
        'RUNNING/Problems': 'One or more tasks within the workflow has one of the following statuses:\n  • Cancelled\n'
                            '  • Confirmation Required\n  • Failure\n  • In Doubt\n'
                            '  • Running/Problems (for sub-workflows)\n  • Start Failure\n  • Undeliverable',
        'CONFIRMATION_REQUIRED': 'If you make JCL changes and restart a z/OS task, Universal Controller will put'
                                 ' the task into Confirmation Required status and prompt you for a confirmation.'
                                 ' For detailed processing steps, see Rerunning a z/OS Task.',
        'SUBMITTED': 'The task has been submitted to the z/OS Job Entry subsystem and scheduled'
                     ' by the z/OS Job Scheduler.',
    }

    def __init__(self, task: Task):
        self.task: Task = task
        self.id: str = None
        self.stdOut: str = None
        self.stdErr: str = None
        self.exitCode: int = None
        self.message: str = None
        self.state: TaskInstanceState = None
        self.status: str = None
        pass

    @property
    def success(self):
        if self.status == 'SUCCESS':
            self.message = ''
        else:
            self.message = TaskInstance.status_desc[self.status]
        return self.status == 'SUCCESS'

    pass
