from pyevolve import G1DList, GAllele
from pyevolve import GSimpleGA
from pyevolve import Mutators
from pyevolve import Crossovers
from pyevolve import Consts


import sys, random,os,time
startingtime = 0
random.seed(1024)
from math import sqrt

PIL_SUPPORT = None

try:
   from PIL import Image, ImageFont, ImageDraw
   PIL_SUPPORT = True
except:
   PIL_SUPPORT = False


cm     = []
coords = []
CITIES = 0
WIDTH   = 1024
HEIGHT  = 768
LAST_SCORE = -1

def cartesian_matrix(coords):
   """ A distance matrix """
   matrix={}
   for i,(x1,y1) in enumerate(coords):
      for j,(x2,y2) in enumerate(coords):
         dx, dy = x1-x2, y1-y2
         dist=sqrt(dx*dx + dy*dy)
         matrix[i,j] = dist
   return matrix

def tour_length(matrix, tour):
   """ Returns the total length of the tour """
   total = 0
   t = tour.getInternalList()
   for i in range(CITIES):
      j      = (i+1)%CITIES
      total += matrix[t[i], t[j]]
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
   with open ("tsp_result_for_ga.txt" , 'a') as f:
      f.write (filename + "&"+str(round(tourcost,2)) +"&" +str(round((time.time() - startingtime),6))+"\\\\"+"\n")
      f.write ("\hline\n")
   f.close()


def G1DListTSPInitializator(genome, **args):
   """ The initializator for the TSP """
   lst = [i for i in xrange(genome.getListSize())]
   random.shuffle(lst)
   genome.setInternalList(lst)

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
   global startingtime, cm, coords, WIDTH, HEIGHT
   if os.path.isfile("att48_tsp_result_for_Ga.txt"):
      os.remove("att48_tsp_result_for_Ga.txt")
   if os.path.isfile("tsp_result_for_ga.txt"):
      os.remove("tsp_result_for_ga.txt")
   
   for filename in os.listdir(folder):
      startingtime = time.time()
      if filename.endswith(".tsp"):
         with open (folder+ filename , 'r') as f:
            if (f.readlines()[4].replace('\n','') == "EDGE_WEIGHT_TYPE : EUC_2D") or (filename == "att48.tsp"):

               f.close()
               coords = readCords(folder + filename)
               cm     = cartesian_matrix(coords)
               genome = G1DList.G1DList(len(coords))

               genome.evaluator.set(lambda chromosome: tour_length(cm, chromosome))
               genome.crossover.set(Crossovers.G1DListCrossoverEdge)
               genome.initializator.set(G1DListTSPInitializator)

               ga = GSimpleGA.GSimpleGA(genome)
               ga.setGenerations(1000)
               ga.setMinimax(Consts.minimaxType["minimize"])
               ga.setCrossoverRate(1.0)
               ga.setMutationRate(0.02)
               ga.setPopulationSize(80)

               ga.evolve(freq_stats=0)
               best = ga.bestIndividual()

               if PIL_SUPPORT:
                  if filename == "att48.tsp":
                     write_tour_to_txt(best,"att48_tsp_result_for_Ga.txt")
                  write_data_for_table(filename , tour_length(cm,best))
               else:
                  print "No PIL detected, cannot plot the graph !"

if __name__ == "__main__":
   main_run()
