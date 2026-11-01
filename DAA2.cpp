
#include <iostream>
#include <algorithm>
using namespace std;

struct Job
{
    char id;
    int deadline;
    int profit;
};

bool compare(Job a, Job b)
{
    return a.profit > b.profit;
}

int main()
{
    int n;
    cout << "Enter number of jobs: ";
    cin >> n;

    Job jobs[n];

    for (int i = 0; i < n; i++)
    {
        cout << "Enter job ID, deadline and profit: ";
        cin >> jobs[i].id >> jobs[i].deadline >> jobs[i].profit;
    }

    sort(jobs, jobs + n, compare);

    int maxDeadline = 0;

    for (int i = 0; i < n; i++)
    {
        maxDeadline = max(maxDeadline, jobs[i].deadline);
    }

    char result[100];
    bool slot[100] = {false};

    int totalProfit = 0;

    for (int i = 0; i < n; i++)
    {
        for (int j = min(maxDeadline, jobs[i].deadline) - 1;
             j >= 0; j--)
        {
            if (!slot[j])
            {
                slot[j] = true;
                result[j] = jobs[i].id;
                totalProfit += jobs[i].profit;
                break;
            }
        }
    }

    cout << "\nSelected Jobs: ";

    for (int i = 0; i < maxDeadline; i++)
    {
        if (slot[i])
            cout << result[i] << " ";
    }

    cout << "\nMaximum Profit: " << totalProfit;

    return 0;
}
