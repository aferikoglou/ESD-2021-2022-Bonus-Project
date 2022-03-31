f1 = open('DSE_GENETIC_300/solution1/solution1_data.json','r')
f2 = open('DSE_GENETIC_299/solution1/solution1_data.json','r')

f1.close()
f2.close()

killed = 0

for i in range (1,401):

    try:
        f = open(f'DSE_GENETIC_{i}/solution1/solution1_data.json','r')
        f.close()
    except Exception as e:
        killed+=1
        print(i)
        #print(e)

print(killed)
