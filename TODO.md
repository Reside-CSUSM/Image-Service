#When Adding areas it's launching bot two times even though it prolly shudn't DONE
#Need to repair search filter DONE
#Need to test if data can be recieved from provider DONE

#Add Count feature to keep track of all the cities, states and countries.


#In order to deploy on vercel don't use relative imports within a folder
#Specify parent package as well. For example:  Don't -> from utility import object.   Do->  from MongoDB.utility import object


#FIX update mechanism shudnt launch bot 3 times and it shudn't create new documents in db instead on update delete previous collection and repopulate documents. Or we can use collection.replace() in case of update  DONE


#issue fixed bot now launches only two times for single area on update, it was adding mamy areas causing bots to launch many times
#still it has extra for DONE


#Fix address parsing issue in database. Modify string filter or not use it because sometimes it parses out important symbpols like # in some addresses


$Fix City, State resolution problem cuz otherwise bots are not going to launch. DONE

#