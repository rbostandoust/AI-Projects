import random
def same_teacher(timeslot, teacher):
    for i in range (len(timeslot)):
        if (teacher == timeslot[i][0]):
            return True
    return False
def population_sort(result, population):
    for i in range (0, len(result)):
        for j in range (0, len(result)):
            if(result[i] > result[j]):
                temp = result[i]
                result[i] = result[j]
                result[j] = temp
                temp = population[i]
                population[i] = population[j]
                population[j] = temp
    for i in range (0, len(result) - 100):
        population.pop() 
        result.pop()
def fitness_function(population, timeSlotPerDay, numberOfDay, goodPhase, badPhase):
    result = []
    for i in range (0, len(population)):
        temp = 0
        submitted_class = []
        for j in range (0, numberOfDay):
            for k in range (0, timeSlotPerDay):
                submitted_teacher = []
                for w in range (0, len(population[i][j][k])):
                    temp += goodPhase[population[i][j][k][w][1] - 1]
                    if(population[i][j][k][w][1] in submitted_class or population[i][j][k][w][0] in submitted_teacher):
                        temp = -999999999999999
                        break
                    submitted_class.append(population[i][j][k][w][1])
                    submitted_teacher.append(population[i][j][k][w][0])
                    for u in range (w, len(population[i][j][k])):
                        temp -= badPhase[population[i][j][k][w][1] - 1][population[i][j][k][u][1] - 1]
        result.append(temp)
    return result
def mutation (population, timeSlotPerDay, numberOfDay, teacherClasses):
    for i in range (0, len(population)):
        randomNumber = random.randint(1, 101)
        if(randomNumber <= 5):
            submitted_class = []
            for j in range (0, numberOfDay):
                for k in range (0, timeSlotPerDay):
                    for w in range (0, len(population[i][j][k])):
                        submitted_class.append(population[i][j][k][w][1])
            c1 = random.randint(0, numberOfDay - 1)
            c2 = random.randint(0, timeSlotPerDay - 1)
            c3 = random.randint(0, len(teacherClasses) - 1)
            if(len(teacherClasses[c3]) != 0):
                c4 = random.randint(0, len(teacherClasses[c3]) - 1)
                submitted_teacher = []
                for j in population[i][c1][c2]:
                    submitted_teacher.append(j[0])   
                if(teacherClasses[c3][c4] not in submitted_class and c3 not in submitted_teacher):
                    population[i][c1][c2].append((c3, teacherClasses[c3][c4]))
def cross_over(population, timeSlotPerDay, numberOfDay):
    for i in range ((int)(len(population)/2)):
        flag = 0
        c1 = random.randint(0 , len(population)-1)
        c2 = random.randint(0 , len(population)-1)
        divider = random.randint(1 , timeSlotPerDay)
        new_chromo = population[c1][:(int)(timeSlotPerDay/divider)] + population[c2][(int)(timeSlotPerDay/divider):]
        submitted_class = []
        for j in range (0, numberOfDay):
            for k in range (0, timeSlotPerDay):
                for w in range (0, len(new_chromo[j][k])):
                    if(new_chromo[j][k][w][1] not in submitted_class):
                        submitted_class.append(new_chromo[j][k][w][1])
                    else:
                        flag = 1
                        break
        if(flag == 0):
            population.append(new_chromo)
def generate_population(teacherClasses, classNumber, timeSlotPerDay, numberOfDay, goodPhase, badPhase):
    population = []
    for r in range (1000):
        chromosome = [[[] for i in range (timeSlotPerDay) ] for j in range (numberOfDay)]
        submitted_class =[]
        for i in range (len(teacherClasses)):
            for j in range (len(teacherClasses[i])):
                for k in range (5):
                    day_rand = random.randint(0 , numberOfDay-1)
                    time_rand = random.randint(0 , timeSlotPerDay-1)
                    if(teacherClasses[i][j] in submitted_class or same_teacher(chromosome[day_rand][time_rand], i)):
                        continue
                    chromosome[day_rand][time_rand].append((i, teacherClasses[i][j]))
                    submitted_class.append(teacherClasses[i][j])
                    break
        population.append(chromosome) 
    result = fitness_function(population, timeSlotPerDay, numberOfDay, goodPhase, badPhase)
    population_sort(result, population)
    lastResult = []
    sample = -99999999999999
    lastResult.append(sample)
    for i in range (100):   
        cross_over(population, timeSlotPerDay, numberOfDay)  
        mutation(population, timeSlotPerDay, numberOfDay, teacherClasses)
        result = fitness_function(population, timeSlotPerDay, numberOfDay, goodPhase, badPhase)
        population_sort(result, population)
        if(result[0] - lastResult[0] < 50):
            break
        lastResult = result
    print(result[0])
    #   max fitness
    return population  
if __name__ == "__main__":

    numberOfDay, timeSlotPerDay = input().split(" ")
    numberOfDay = (int)(numberOfDay)
    timeSlotPerDay = (int)(timeSlotPerDay)
    classNumber = (int)(input())
    goodPhase = []
    goodPhase = input().split(" ")
    goodPhase = list(map(int, goodPhase)) 
    teacherNumber = (int)(input())
    teacherClasses = []
    for i in range (0, teacherNumber):
        temp = input().split(" ")
        temp.pop(0)
        teacherClasses.append(list(map(int, temp)))
    badPhase = []
    for i in range (0, classNumber):
        temp = input().split(" ")
        temp.pop()
        badPhase.append(list(map(int, temp)))
    ppl = generate_population(teacherClasses, classNumber, timeSlotPerDay, numberOfDay, goodPhase, badPhase)
    for i in range (numberOfDay):
        for j in range (timeSlotPerDay):
            for k in range (len(ppl[0][i][j])):
                print (i+1, j+1, ppl[0][i][j][k][1], ppl[0][i][j][k][0])
                # d   t   c   p 

    