Title: Querying JIRA for the current sprint's items
Category: Code
Date: 2019-08-05
Authors: Jeff Esp
Summary: How to query JIRA for relevant items in the current sprint

Depending on what you are trying to measure, it can be difficult to get the exact number of points
in a sprint. There are two limits in JIRA relating to "Story" and "Sub-task" issues that makes this
difficult.

1. If you use stories and sub-tasks, the sub-tasks are **not** included in the points total in the
   sprint.
2. Also if you use stories and sub-tasks, when a story is moved to another sprint because it is not
   complete, all the subtasks move with it.

There are a few solutions that you could implement that don't involve using the code I have later in
this post. This was not going to work for my team as I'm not going to set policy on how the team
organizes the work. First off, that makes people hate the work tracking, making them less likely to
use it. Secondly, I don't want to have to fight with JIRA.

So I use the following JQL query in JIRA to find issues in a sprint.

```
Project = 'PROJ' AND Sprint = 1234 AND (statusCategory != Done OR statusCategoryChangeDate >= '2019-08-07')
```

To break the clauses of that down, an issue is included in this list if:

1. It is in `PROJ`
2. And part of sprint `1234`
3. And either: a) is not `Done`, or b) last status change is past the sprint `startDate`.

Unfortunately there are a few things you have to manually fill in and you cannot just have a
saved query that automatically grabs the right information.
