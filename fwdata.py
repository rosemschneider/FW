import csv
import sys
import io

FIRSTROW = "Assignment ID,Date Test,Time,number_kids,guardian_ed,birth_order,gender,first_word,word_validation,word_type,addressee,word_meaning,word_age,current_age,word_lang,home_lang,notes\n"

#first 8 columns are not useful.  The 9th is what we want.
#9th column begins and ends with a quotation mark.  Remove that, and we have a CSV.

#todo: add a cmd line arg to specify file
if __name__ == "__main__":
    
    #quick and dirty - first arg after the script name is the file name.
    src = open(sys.argv[1], 'r')

    #see http://stackoverflow.com/questions/1170214/pythons-csv-writer-produces-wrong-line-terminator/1170297#1170297
    filename = 'out.csv'
    if sys.version_info >= (3,0,0):
        outfile = open(filename, 'w', newline='')
    else:
        outfile = open(filename, 'wb')
    
    wtr = csv.writer(outfile)

    rdr = csv.reader(src)

    firstpass = False
    for row in rdr:
        #skip the first row
        if(firstpass == False):
            outfile.write(FIRSTROW)
            firstpass = True
            continue
            
        #keep only the 9th
        d = row[8]
        #remove the quotation marks (first and last)
        d = d[1:-1]
        
        #if there was more than one child, there will be more than one response in this line
        #we could either check number_kids, or look for a \n.  
        #Going by # kids should be okay, assuming the JS didn't allow the person to finish without reponding for all kids
        cols = d.split(',')

        #number_kids is the 4th column
        nkids = int(cols[3])
        

        if(nkids > 1):

            #make a new vble for more rows from this one
            new_rows = [['']*17 for i in range(nkids)] 
            #note, you cannot do [['']*17]*nkids because that would make all the subarrays change together...weird.
            #see http://stackoverflow.com/questions/6667201/how-to-define-two-dimensional-array-in-python

            #copy the first 16 entries into new_rows
            #python list indexing requires that you write the index one past the last one you write.
            new_rows[0][0:16] = cols[0:16]
            
            #the 17th is combined with the 1st of the next row
            for i in range(nkids-1): #do it once for 2 kids, twice for 3, etc.
                #the 17th column will have a "\n" in it, which actually should start the next row.
                split17 = cols[i*16+16].split("\\n")
                
                #new_rows[i][16] = split17[0]+"\n"
                new_rows[i+1][0] = split17[1]
                
                new_rows[i+1][1:-1] = cols[(16*(i+1))+1:(16*(i+1)+15)+1]
                
                wtr.writerow(new_rows[i])
            
            wtr.writerow(new_rows[-1])    
                
        else:
            #get rid of that last "\n".  writerow() takes care of adding one
            cols[16] = cols[16][0:-2]
            cols[16] = cols[16]

            wtr.writerow(cols)
             
            
        
        
        
        