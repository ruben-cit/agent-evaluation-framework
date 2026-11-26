# Agent Evaluation Framework

The language of an open framework for evaluating tool-using agents on versioned tasks.

## Language

### Versioning

**Persistent ID**:
A stable identifier for the same entity across all its versions. For example, `dodgeball.annotate-throw` identifies the task that asks for the players, positions, and outcome of a marked throw. The task keeps that ID when its answer key changes. Retired IDs stay reserved.

**Version**:
A fixed snapshot of an entity at a particular point in its history. For tasks, the framework uses the full Git commit SHA as the version identifier. For example, `dodgeball.annotate-throw` at `8f3c2a1…` (an illustrative, abbreviated SHA) refers to the task as defined at that commit. If a later commit corrects its answer key, the task keeps its persistent ID and the new SHA identifies the updated version.

### Task

**Task**:
A versioned definition of the prompt variants, response schema, fixtures, and private answer key. The subject sees one prompt variant, the response schema, and the fixtures. It never sees the answer key.
_Avoid_: case

**Fixtures**:
The fixed inputs and setup a task version requires before a trial begins. Changing a fixture creates a new task version. For the dodgeball task, the engine places the clip, roster, and court overlay at the paths named in its prompt variants.
_Avoid_: live fixtures, fixture version

**Prompt variant**:
One named wording of what the task asks the subject to do. A task has one or more, and all of them share the task’s response schema, fixtures, and answer key. Changing a prompt variant creates a new task version.
_Avoid_: prompt template, instructions

**Response schema**:
The task field that defines the JSON object the subject must return.

**Answer key**:
The task field that holds the checks the answer grader applies to a submission. The subject never sees it.

**Draft**:
A task version that no approver has published. A job cannot include it.

**Publication**:
An approver’s recorded approval of one task version, after which a job can include that version.
_Avoid_: promotion, publish the task

**Approver**:
The person who checks that a draft makes sense, that its prompt variants ask for the same thing, and that its answer key is correct, then publishes it.
_Avoid_: reviewer

### Prompt

**Delivered prompt**:
The exact message the evaluation engine sends to the subject at the start of a trial: the selected prompt variant followed by the response schema.
_Avoid_: rendered prompt, prompt sent

### Subject

**Model**:
A language model on its own, apart from the program that runs it.

**Harness**:
The program that runs a model in a loop and exposes tools to it.

**Agent**:
A model running in a harness with tools. The framework contains more than one agent: the subject, and usually whatever drafts a task. Each is called by its role, and “agent” names only the general category.

**Subject**:
The agent being evaluated.
_Avoid_: agent, tool-using agent, model

**Subject configuration**:
The provider, model, harness, extensions, and reasoning effort that identify a subject. Two subjects with different extensions are different subjects. Permissions are a condition of a job, not part of the subject configuration.
_Avoid_: agent configuration

### Trials and jobs

**Trial**:
One execution of a subject on one task version using one of its prompt variants. Each trial starts fresh with the task’s fixtures. Repeated trials of a task in a job use the same task version, subject configuration, and tool permissions.
_Avoid_: attempt, replication

**Job**:
A collection of trials for a specified subject configuration and selection of task versions. The job setting **trials per task** specifies how many fresh trials to schedule for each selected task under each selected prompt variant.
_Avoid_: run, experiment

### Isolation

**Sandbox**:
The sealed place one trial runs in, which enforces what the subject can reach.
_Avoid_: executor, container, isolated environment, isolated trial

**Workspace**:
The directory inside the sandbox where the fixtures are placed and the subject works.

### Trial records

**Manifest**:
The conditions a trial ran under, recorded before it starts: the task version, prompt variant, subject configuration, and permissions.
_Avoid_: metadata

**Trial evidence**:
What is kept from one trial after its workspace is destroyed: the session transcript, the final response, and any files the subject produced. The answer grader reads only this.
_Avoid_: archived evidence, captured evidence, evaluation evidence

**Session transcript**:
The harness’s own record of the messages, tool calls, and tool results in a trial.
_Avoid_: trace, saved session, recorded session

**Usage**:
The resources a trial consumed: tokens, cost, and wall time. It is not trial evidence.
_Avoid_: metadata

### Response

**Final response**:
The exact text of the subject’s last message, kept as received. It can be missing.
_Avoid_: reply, raw reply

**Submission**:
The final response read as a single JSON object. There is no submission when the final response is anything other than exactly one JSON object. A submission that violates the response schema is an invalid submission.
_Avoid_: submitted JSON, final JSON object

### Grading

**Check**:
One rule in an answer key: the submitted value it covers, its private expected value, an error measure, and a tolerance. It passes when the error is at most the tolerance.

**Grade**:
The answer grader’s record for one trial: the verdict, each check’s error, tolerance, and result, and the grader version and settings.
_Avoid_: score, answer grade

**Verdict**:
The pass or fail result in a grade.

**Infrastructure failure**:
A trial that could not run properly for a reason outside the subject’s doing, such as a provider outage.

**Ungraded**:
Having no grade because the trial ended in an infrastructure failure. Ungraded trials are left out of the pass rate.
_Avoid_: unscored

**Pass rate**:
Passed trials divided by graded trials.
