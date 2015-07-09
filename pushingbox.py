#pushingbox class
#Credit to: GuigiAbloc
#from the pushingbox python API page
#http://blog.guiguiabloc.fr/index.php/2012/02/22/pushingbox-vos-notifications-in-the-cloud/

import  urllib ,  urllib2 
class pushingbox ( ) :
  url =  "" 
  def  __init__ ( self , key ) :
    url =  'http://api.pushingbox.com/pushingbox' 
    values ​​=  { 'devid' : key } 
    try :
      data =  urllib . urlencode ( values ) 
      req =  urllib2 . Request ( url , data ) 
      sendrequest =  urllib2 . urlopen ( req ) 
    except  Exception , detail:
       print  "Error " , detail