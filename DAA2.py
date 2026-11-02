
# Job Sequencing with Deadlines using Greedy Method

def job_sequencing(jobs):

    # Sort jobs by profit in descending order
    jobs.sort(key=lambda x: x[2], reverse=True)

    # Find maximum deadline
    max_deadline = max(job[1] for job in jobs)

    # Create time slots
    slots = [None] * max_deadline

    total_profit = 0

    # Schedule jobs
    for job in jobs:
        job_id, deadline, profit = job

        for j in range(min(deadline, max_deadline) - 1, -1, -1):
            if slots[j] is None:
                slots[j] = job_id
                total_profit += profit
                break

    # Display result
    print("\nScheduled Jobs:", [job for job in slots if job is not None])
    print("Maximum Profit:", total_profit)


# Accept input from user
n = int(input("Enter number of jobs: "))

jobs = []

for i in range(n):
    print("\nEnter details for Job", i + 1)

    job_id = input("Enter Job ID: ")
    deadline = int(input("Enter Deadline: "))
    profit = int(input("Enter Profit: "))

    jobs.append((job_id, deadline, profit))

# Call function
job_sequencing(jobs)
