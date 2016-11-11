import io 
import random

import datetime
from time import gmtime, strftime, sleep

import requests

from rdflib.graph import Graph
from rdflib import Namespace, URIRef, Literal

from PIL import Image, ImageDraw, ImageFont

class HTTPOperation:
    
    def __init__(self, config, counter):
        self.config = config
        self.counter = counter
        
        self.SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
        self.nsdict = dict(skos=self.SKOS)

    def delete_request(self, uri):
        st = datetime.datetime.now()
        starttime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        
        processed = 0
        response_status_code = 0
        httperror = 1
        with requests.Session() as sess:
            try:
                r = sess.delete(uri)
                httperror = 0
                response_status_code = r.status_code
                if r.status_code == 204:
                    processed = 1
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                    print (e)
                    pass
            
        endtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        et = datetime.datetime.now()
        timedelta = et - st
        
        oline = uri+ "; " + str(processed) + "; " + str(response_status_code) + "; " + str(timedelta) + "; "
        self.counter.results.append(oline)
        print(oline)
        
        i = {
            "processed": processed,
            "httperror": httperror,
            "response_status_code": response_status_code,
            "starttime": starttime,
            "endtime": endtime,
            "timedelta": timedelta,
            
            "processed_binary": 0,
            "httperror_binary": 0,
            "response_status_code_binary": 0,
            "timedelta_binary": datetime.timedelta(0),
        }
        self.counter.update(i, 0)
        return
    
    def get_request(self, uri):
        headers={"Content-type": "application/n-triples"}

        st = datetime.datetime.now()
        starttime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        
        processed = 0
        response_status_code = 0
        httperror = 1
        with requests.Session() as sess:
            try:
                r = sess.get(uri, headers=headers)
                httperror = 0
                response_status_code = r.status_code
                if r.status_code == 200:
                    processed = 1
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                    print (e)
                    pass
            
        endtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        et = datetime.datetime.now()
        timedelta = et - st
        
        oline = uri+ "; " + str(processed) + "; " + str(response_status_code) + "; " + str(timedelta) + "; "
        self.counter.results.append(oline)
        print(oline)
        
        i = {
            "processed": processed,
            "httperror": httperror,
            "response_status_code": response_status_code,
            "starttime": starttime,
            "endtime": endtime,
            "timedelta": timedelta,
            
            "processed_binary": 0,
            "httperror_binary": 0,
            "response_status_code_binary": 0,
            "timedelta_binary": datetime.timedelta(0),
        }
        self.counter.update(i, self.config["load_binary_data"])
        return
    
    def insertRelations(self, subjects, g):
        for s in subjects:
            tempg = Graph()
            tempg += g.triples( (URIRef(s), None, None) )
            d = tempg.serialize(format="nt", initNs=self.nsdict)
            
            response = requests.put(s, data=d, headers={"Content-type": "application/n-triples"})
            
            oline = s+ "; " + str(response.status_code) + "; "
            self.counter.results.append(oline)
            print(oline)
            
    def put_request(self, s, c, resources_graph):
        new_s = s.replace(self.config['fcrepo']['base'], self.config['fcrepo']['base'] + c + "/")
        
        tempg = Graph()
        for s,p,o in resources_graph.triples( (URIRef(s), None, None) ):
            tempg.add(( URIRef(new_s), p, o))
        
        num = random.randint(1, 4)
        tempg.add( ( URIRef(new_s), self.SKOS.related, URIRef(self.config['fcrepo']['base'] + "related0" + str(num)) ) )
        d = tempg.serialize(format="nt", initNs=self.nsdict)
        headers={"Content-type": "application/n-triples"}
        
        st = datetime.datetime.now()
        starttime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        
        processed = 0
        response_status_code = 0
        httperror = 1
        with requests.Session() as sess:
            try:
                r = sess.put(new_s, data=d, headers=headers)
                httperror = 0
                response_status_code = r.status_code
                if r.status_code == 201:
                    processed = 1
            except requests.exceptions.RequestException as e:
                    print (e)
                    pass

        endtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        et = datetime.datetime.now()
        timedelta = et - st

        oline = new_s+ "; " + str(processed) + "; " + str(response_status_code) + "; " + str(timedelta) + "; "
        self.counter.results.append(oline)
        print(oline)
        
        processed_binary = 0
        httperror_binary = 0
        response_status_code_binary = 0
        timedelta_binary = datetime.timedelta(0)
        if self.config["load_binary_data"]:
            new_s_binary = new_s + "/addison.jpg"
            
            im = Image.open("source-data/sample-data/20151225_084019.jpg")
            im = im.rotate(-90, expand=True)
            # Adding text, hopefully, will result in a unique image.  
            # In a limited test of about 1,250 resources, this was certainly the case,
            # finding 1,250 resources buried in the subdirectories of the fcrepo.binary 
            # directory.
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype("source-data/sample-data/Tuffy_Bold.ttf", 56)
            draw.text((10, 4030), new_s_binary, (0,0,0), font=font)
            
            file = io.BytesIO()
            im.save(file, format="jpeg")
            file.name = 'addison.jpg'
            file.seek(0)
            
            headers={"Content-type": "image/jpeg"}
            
            st_binary = datetime.datetime.now()
            starttime_binary = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        
            with requests.Session() as sess:
                try:
                    r = sess.put(new_s_binary, data=file, headers=headers)
                    httperror_binary = 0
                    response_status_code_binary = r.status_code
                    if r.status_code == 201:
                        processed_binary = 1
                except requests.exceptions.RequestException as e:
                        print (e)
                        pass
            
            endtime_binary = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            et_binary = datetime.datetime.now()
            timedelta_binary = et_binary - st_binary
            
            oline = new_s_binary+ "; " + str(processed_binary) + "; " + str(response_status_code_binary) + "; " + str(timedelta) + "; "
            self.counter.results.append(oline)
            print(oline)

        i = {
            "processed": processed,
            "httperror": httperror,
            "response_status_code": response_status_code,
            "starttime": starttime,
            "endtime": endtime,
            "timedelta": timedelta,
            
            "processed_binary": processed_binary,
            "httperror_binary": httperror_binary,
            "response_status_code_binary": response_status_code_binary,
            "timedelta_binary": timedelta_binary,
        }
        self.counter.update(i, self.config["load_binary_data"])
        return
