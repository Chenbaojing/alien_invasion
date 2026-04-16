#include <cstdio>
#include <cmath>
using namespace std;

int main()
{
    int A, C = 0;
    scanf ("%d", &A);
    for(int i = 1; i <= sqrt(A); i++)
    {
        if (A % i == 0)
        {
            if (i == A / i)
                C++;
            else
                C += 2;
        }
    }
    printf("%d", C);
}