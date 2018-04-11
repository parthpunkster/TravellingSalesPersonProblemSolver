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

def tour_length(matrix, tour):
   """ Returns the total length of the tour """
   total = 0
   for i in range(len(tour)-1):
   	  	 total += matrix[tour[i],tour[i+1]]
   return total

def write_data_for_table(filename,tourcost):
   global startingtime
   with open ("tsp_result_for_greedy.txt" , 'a') as f:
      f.write (filename + "&"+str(round(tourcost,2)) +"&" +str(round((time.time() - startingtime),6))+"\\\\"+"\n")
      f.write ("\hline\n")
   f.close()

def write_tour_to_txt(tour,txt_file):
   """ THe function to write to output file """
   num_cities = len(tour)
   with open (txt_file , 'w') as f:
      f.write("TOUR_SECTION\n")
      for i in range(num_cities):
         f.write(str(tour[i])+'\n')
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
   if os.path.isfile("att48_tsp_result_for_greedy.txt"):
      os.remove("att48_tsp_result_for_greedy.txt")
   if os.path.isfile("tsp_result_for_greedy.txt"):
      os.remove("tsp_result_for_greedy.txt")
   
   for filename in os.listdir(folder):
      startingtime = time.time()
      if filename.endswith(".tsp"):
         with open (folder+ filename , 'r') as f:
            if (f.readlines()[4].replace('\n','') == "EDGE_WEIGHT_TYPE : EUC_2D") or (filename == "att48.tsp"):
		
            	coords = readCords(folder + filename)
            	cm     = cartesian_matrix(coords)
            	next = 1
            	visited = [1]
            	while len(visited) != CITIES:
            		tmp = {}
            		for j in range(1,(CITIES+1)):
            			if (next != j) and (j not in visited) :
            				tmp[(next,j)] = cm[(next,j)]
            		minimum = min(tmp,key = tmp.get)[1]
            		visited.append(minimum)
            		next = minimum
            	visited.append(1)

            	write_data_for_table(filename , tour_length(cm,visited))
                if filename == "att48.tsp":
                  write_tour_to_txt(visited , "att48_tsp_result_for_greedy.txt")               
          					

if __name__ == "__main__":
   main_run()

