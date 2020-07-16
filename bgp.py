import sys
import os

from aggregate_prefixes import aggregate_prefixes


def main():

   if len(sys.argv)<3:
       print("Usage: "+sys.argv[0]+" Source_File AS_Number")
       sys.exit()

   filepath = sys.argv[1]
   SourceAS = sys.argv[2]
   ASPrefixesFile = "Aggregated.txt"

   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

   ASPrefixesList = []

   print("Reading input prefixes...\n")

   with open(filepath) as fp:
       cnt = 0
       for line in fp:
           words = line.strip().split()
           #print(line)
           if len(words)>2 and words[-2]==SourceAS:
              #print("prefix: "+words[1]+", Source AS: "+words[-2])
              ASPrefixesList.append(words[1])
              cnt += 1
              print("\rtotal found "+str(cnt)+", adding "+words[1]+"     ", end="")
              
  
   #print("Source prefix list:\n")
   #print(ASPrefixesList)
   print("\nAggregating...")

   AggrPList = aggregate_prefixes(ASPrefixesList)

   with open(ASPrefixesFile, 'w') as fASPrefixes:
    for prefix in AggrPList:
        fASPrefixes.write("%s\n" % prefix)

   print("Done.\n")

if __name__ == '__main__':
    main()