import urllib
import sys
import re


web=r'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?'
level=r'&level=under'
subject=r'&subject='
coursenum=r'&cournum='
sess=r'sess='
ts=r'<TR>'
td=r'<TD ALIGN="center">'
pat=ts+td
tr=r'</TD>'
table=r'</TABLE>'
end = r'</HTML>'

def query(result,term,course,num):
   f = urllib.urlopen(result)
   
   resid = 1
   while 1:
      text = f.readline().strip()
      if text == end:
         break
      if pat in text:
         if resid == 0:
            break
         resid -= 1
   
   if resid == 1:
      print "no result is found for",term,str(course)+str(num)
      return
     
   print 'The following is the result of',term,str(course)+str(num)
   print 'Note: Actual - Enrol = # of students override'
   print
   print '{0:7s} {1:5s} {2:5s} {3:20s} {4:9s} {5:20s}'.format("Section","Enrol","Actual","Time","Room","Instructor")
   print
   while text != table:
      text = text.split(tr)
      section = re.sub(td,"",text[1])
      if section[0:3] != "LEC" and section[0:3] != "LAB" and section[0:3] != "TUT":
         text = f.readline().strip()
         continue
      enrol = re.sub(td,"",text[6])
      total = re.sub(td,"",text[7])
      time = re.sub(td,"",text[10])
      loc = re.sub(td,"",text[11])
      prof = re.sub(td,"",text[12])
      if prof == r'</TR>':
         prof = "Unknown"
      print '{0:7s} {1:5s} {2:5s} {3:20s} {4:9s} {5:20s}'.format(section,enrol,total,time,loc,prof)
      
      text = f.readline().strip()
   
def parsing_term(term):
   #parsing term
   digit = 0
   semester = term[0].upper()
   if semester == 'F':
      digit = 9
   elif semester == 'S':
      digit = 5
   elif semester == 'W':
      digit = 1
   else:
      print 'warning: you enter a wrong term'
      print 'please enter either W , S, or F'
      sys.exit(5)
   year = term[1::]
   
   session = '1'+year+str(digit)   
   #parsing complete
   return session
   
def calc_web(session,num,course):
    result = web + sess + session + level + subject + course + coursenum + num
    return result
    
if __name__ == '__main__':

   term = raw_input("enter the term(e.g S13)")
   session = parsing_term(term)
   course = raw_input("enter the course(e.g MATH)")
   num = raw_input("enter the course num(e.g 237)")
   print
   
   course = course.upper()
   result = calc_web(session,num,course)
   query(result,term,course,num)
   
