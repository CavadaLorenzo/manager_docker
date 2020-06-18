##
# @mainpage
# The manager is a python script running in a Docker. This Docker will have a volume, the file storage area, where is supposed to be all the media present in the whole system. 
# The manager represent for us the muscle of our system, it will be triggered through a GET request done from copycat where is specified what file move where. 
#The workflow of this script is quite easy, it get the request from copycat, it will search the file in its file storage area, will create a scp connection with the sidecar specified in the request, and than will copy the media.
