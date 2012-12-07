
bandwidth = 0.25    # use MBPS as the unit

class Application (object):
       def __init__(self, id, type, size, TI):
             self. id = id
             self. type = type
             self. size = size
             self. TI = TI
             self. max_wait_slot = round( 24 - TI / 0.125 ) # round() add by Weichao
             if      self.type == 1:
                       self.basic = 0.05
             elif   self.type == 2:
                       self.basic = 0.1
             else:  
                       self.basic = 0.15        
       
       def getTI (self):
             return self. TI
       
       def slot_need2 (self, slotleft):
             slotneed = self.size / self.basic * 300
             if slotneed <= slotleft:
                return self.size / 75                # In such case it is useless to use basic bandwidth rather than full bandwidth, since cost will not change.
             else:
                return (self.size - slotleft * self.basic * 300) / 75 + slotleft
             
       def price2 (self, curprice, newprice, slotleft):
             if self.slot_need2( slotleft ) > slotleft:
                return slotleft * self.basic * 300 * curprice + (self.size - slotleft * self.basic * 300) * newprice
             else: 
                return curprice * self.size

       def slot_need3 (self):                                              # case 1 is just the special case here with max_wait_slot = 0.
             slotneed = self.size / 75
             return self. max_wait_slot + slotneed

       def price3 (self, curprice, newprice, slotleft):      
             if self.slot_need3() <= slotleft:
                return curprice * self.size
             else:
                if self.max_wait_slot >= slotleft:
                   return newprice * self.size
                else:
                   return (self.slot_need3() - slotleft) * 75 * newprice + (slotleft - self.max_wait_slot) * 75 * curprice

       def next5mins (self, curprice, newprice, slotleft):                                            # return the amount of data consumption in next 5 mins
             if self.slot_need2 (slotleft) - self.size / 75 > self.max_wait_slot:       # method 2 cannot be used, method 3 is the only choice
                if self.max_wait_slot == 0:
                   return 75
                else:
                   return 0
             else:                                                          # method 2 is also OK, compare the cost of both method 2 & 3, then choose the cheaper one 
                if self.price2 (curprice, newprice, slotleft) <= self. price3 (curprice, newprice, slotleft):
                   return self.basic * 300
                else:
                   if self.max_wait_slot == 0:
                      return 75
                   else:
                      return 0

       def generateTraffic( self, curStation, prediction ):
            nextStation = prediction[0]
            handOverSlot = prediction[1]

            curprice = curStation.getPrice( 0 )
            newprice = self.predictNewPrice( curStation, nextStation, handOverSlot )
            slotleft = self.calculateSlotLeft()

            return [self.next5mins( curprice, newprice, slotleft ), self.TI, self.type]

       def predictNewPrice( self, curStation, nextStation, handOverSlot ):
            #may need to modify
            if nextStation is None:
                   return curStation.getPrice( 0 )
            return nextStation.getPrice( 0 )

       def calculateSlotLeft( self ):
            #TODO
            return 10
                 
             
                
                
             
             





