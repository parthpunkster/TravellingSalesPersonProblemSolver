import sys, random,os,time
startingtime = 0
random.seed(1024)
from math import sqrt

cm     = []
coords = []
CITIES = 0


def cartesian_matrix(coords):
   """ A distance matrix """
   matrix={}
   for i,(x1,y1) in enumerate(coords):
      for j,(x2,y2) in enumerate(coords):
         dx, dy = x1-x2, y1-y2
         dist=sqrt(dx*dx + dy*dy)
         matrix[i+1,j+1] = dist
   return matrix

def g_Of_N(tempVisited,matrix):
   sum = 0
   for i in range(0,len(tempVisited)-1):
      sum += matrix[tempVisited[i],tempVisited[i+1]]
   return sum

def h1_Of_N(tempVisited,matrix,currentCity):
   tmp=[]
   for i in range(1,CITIES+1):
      if i not in tempVisited:
         tmp.append(matrix[currentCity,i])
   if tmp == []:
      return 0
   else:
      return min(tmp)

def h3_Of_N(tempVisited,matrix):
   sum = 0
   subGraph = []
   for i,j in sorted(matrix,key=matrix.get):
      if i != j:
         if (i not in tempVisited) and (j not in tempVisited):
            iFlag = 'NOVALUE'
            jFlag = 'NOVALUE'
            for ct,sub in enumerate(subGraph):
               if i in sub:
                  iFlag = ct
               if j in sub:
                  jFlag = ct
            if (iFlag == 'NOVALUE') and (jFlag == 'NOVALUE'):
               sum += matrix[i,j]
               subGraph.append([i,j])
            elif (iFlag == 'NOVALUE'):
               sum += matrix[i,j]
               subGraph[jFlag].append(i)
            elif (jFlag == 'NOVALUE'):
               sum += matrix[i,j]
               subGraph[iFlag].append(j)
            elif iFlag != jFlag:
               sum += matrix[i,j]
               subGraph[iFlag] = subGraph[iFlag]+subGraph[jFlag]
               subGraph.pop(jFlag)
   return sum



      

def tour_length(matrix, tour):
   """ Returns the total length of the tour """
   total = 0
   for i in range(len(tour)-1):
      total += matrix[tour[i],tour[i+1]]
   return total

def write_tour_to_txt(tour,txt_file):
   """ THe function to write to output file """
   num_cities = len(tour)
   with open (txt_file , 'w') as f:
      f.write("TOUR_SECTION\n")
      for i in range(num_cities):
         f.write(str(tour[i])+'\n')
   f.close()

def write_data_for_table(filename,tourcost):
   global startingtime
   with open ("tsp_result_for_astar.txt" , 'a') as f:
      f.write (filename + "&"+str(round(tourcost,2)) +"&" +str(round((time.time() - startingtime),6))+"\\\\"+"\n")
      f.write ("\hline\n")
   f.close()

def readCords(filename):
   global CITIES
   with open (filename , 'r') as f:
      lines = f.readlines()
      for elem in lines:
         elem1 = elem.strip().replace('\n','')
         elem1 = ' '.join(elem1.split())
         lines[lines.index(elem)] = elem1
      stval = lines.index('NODE_COORD_SECTION') + 1
      finallist = []
      for i in range (stval,len(lines)):
         elem = lines[i].split(' ')
         if elem != ['EOF']:
            finallist.append((float(elem[1]),float(elem[2])))
      f.close()
      CITIES = len(finallist)
      return finallist


def main_run():
   folder = raw_input('Please Enter the name of folder (e.g benchmarks) : ')
   folder = folder+'/'
   global startingtime, cm, coords,CITIES
   if os.path.isfile("att48_tsp_result_for_astar.txt"):
      os.remove("att48_tsp_result_for_astar.txt")
   if os.path.isfile("tsp_result_for_astar.txt"):
      os.remove("tsp_result_for_astar.txt")
   ctr = 1
   
   for filename in os.listdir(folder):
      startingtime = time.time()
      if filename.endswith(".tsp"):
         with open (folder + filename , 'r') as f:
            if (f.readlines()[4].replace('\n','') == "EDGE_WEIGHT_TYPE : EUC_2D") or (filename == "att48.tsp"):
               coords = readCords(folder + filename)
               cm = cartesian_matrix(coords)
               visited = []
               startCity = 'NONE'
               tempStartCity = 'NONE'
               visited1 = []
               select ={}
               while len(visited) != CITIES:
                  for i in range(1,CITIES+1):
                     if i not in visited:
                        if startCity == 'NONE':
                           tempStartCity = i
                        else :tempStartCity = startCity
                        tempVisited = visited+[i]
                        # print tempVisited
                        gOfN = g_Of_N(tempVisited,cm)
                        h1OfN = h1_Of_N(tempVisited,cm,i)
                        h2OfN = h1_Of_N(tempVisited,cm,tempStartCity)
                        h3OfN = h3_Of_N(tempVisited,cm)
                        if len(tempVisited) == 1:
                           select[(i)] = gOfN+h1OfN+h2OfN+h3OfN
                        else : 
                           select[tuple(tempVisited)] = gOfN+h1OfN+h2OfN+h3OfN
                  minimum = min(select,key = select.get)
                  if type(minimum) == int:
                     minimum = [minimum]
                  elif type(minimum) == tuple:
                     minimum = list(minimum)
                  if len(minimum) == 1:
                     del select[minimum[0]]
                  else :
                     del select[tuple(minimum)]
                  visited = minimum
                  startCity = minimum[0]               
               visited.append(visited[0])
               write_data_for_table(filename,tour_length(cm,visited))
               if filename == "att48.tsp":
                  write_tour_to_txt(visited,"att48_tsp_result_for_astar.txt")



if __name__ == "__main__":
   main_run()
