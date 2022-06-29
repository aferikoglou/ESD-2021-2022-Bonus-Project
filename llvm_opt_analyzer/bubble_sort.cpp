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
    int A[N] = {9,8,7,6,5,4,3,2,1,0,16,17,18,19,20,15},temp,B[N][N];
    for (int i=0;i<N-1;i++)
        for (int j=0;j<N-i-1;j++)
        {
            if (A[j] > A[j + 1])
            {
                temp = A[j+1];
                A[j+1]=A[j]+1;
                A[j]=temp;
            }
        }
    addArr(A,A);
    for (int i=1;i<N;i++)
        A[i] = A[i] + 1;
    for (int i=0;i<N;i++)
        for (int j=0;j<N;j++)
            B[i][j] += i*j;
    return A[0];
}