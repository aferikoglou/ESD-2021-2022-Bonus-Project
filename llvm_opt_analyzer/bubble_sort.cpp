#define N 16

int r0()
{
    return 0;
}

void addArr(int *a,int *b)
{
    for(int i=0;i<N;i++)
        a[i] += b[i];
}

int main(int argc,char **argv)
{
    int A[N] = {9,8,7,6,5,4,3,2,1,0,16,17,18,19,20,15},temp;
    for (int i=0;i<N-1;i++)
        for (int j=0;j<N-i-1;j++)
            if (A[j] > A[j + 1])
            {
                temp = A[j+1];
                A[j+1]=A[j];
                A[j]=temp;
            }
    addArr(A,A);
    return A[0];
}