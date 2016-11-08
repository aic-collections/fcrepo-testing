class Counter:

    def __init__(self):
        self.results = []
        self.total_processed = 0
        self.total_unprocessed = 0
        self.total_errors = 0
        self.total_httperrors = 0
        self.total_200s = 0
        self.total_201s = 0
        self.total_204s = 0
        self.total_4xxs = 0
        self.total_5xxs = 0
        self.total_unanticipated_responses = 0
        self.avgtime_sum = False
        
        self.total_processed_binary = 0
        self.total_unprocessed_binary = 0
        self.total_errors_binary = 0
        self.total_httperrors_binary = 0
    
    def output(self, starttime, endtime, timedelta, load_binary_data):
        print ()
        print ("Task started at: " + starttime)
        print ("Task ended at: " + endtime)
        print ("Elapsed time: ", str(timedelta))
        print ("Number of resources processed: ", str(self.total_processed))
        print ("Number of resources unprocessed: ", str(self.total_unprocessed))
        if load_binary_data:
            print ("Number of binaries processed: ", str(self.total_processed_binary))
            print ("Number of binaries unprocessed: ", str(self.total_unprocessed_binary))
            print ("Number of HTTP errors for binary: ", str(self.total_httperrors_binary))
        print ("Number of HTTP errors: ", str(self.total_httperrors))
        print ("Number of 200s: ", str(self.total_200s))
        print ("Number of 201s: ", str(self.total_201s))
        print ("Number of 204s: ", str(self.total_204s))
        print ("Number of 4xxs: ", str(self.total_4xxs))
        print ("Number of 5xxs: ", str(self.total_5xxs))
        print ("Number of unanticipated responses: ", str(self.total_unanticipated_responses))
        print()

    def update(self, i, load_binary_data):
        if self.avgtime_sum:
            self.avgtime_sum = self.avgtime_sum + i["timedelta"]
        else:
            self.avgtime_sum = i["timedelta"]
        
        if i["processed"] == 1:
            self.total_processed = self.total_processed + 1
        else:
            self.total_unprocessed = self.total_unprocessed + 1
        
        if i["httperror"] == 1:
            self.total_httperrors = self.total_httperrors + 1
        if i["response_status_code"] == 200:
            self.total_200s = self.total_200s + 1
        elif i["response_status_code"] == 201:
            self.total_201s = self.total_201s + 1
        elif i["response_status_code"] == 204:
            self.total_204s = self.total_204s + 1
        elif i["response_status_code"] > 399 and i["response_status_code"] < 500:
            self.total_4xxs = self.total_4xxs + 1
        elif i["response_status_code"] > 499:
            self.total_5xxs = self.total_5xxs + 1
        else:
            self.total_unanticipated_responses = self.total_unanticipated_responses + 1
        
        if load_binary_data:
            if self.avgtime_sum:
                self.avgtime_sum = self.avgtime_sum + i["timedelta_binary"]
            else:
                self.avgtime_sum = i["timedelta_binary"]
        
            if i["processed_binary"] == 1:
                self.total_processed_binary = self.total_processed_binary + 1
            else:
                self.total_unprocessed_binary = self.total_unprocessed_binary + 1
        
            if i["httperror"] == 1:
                self.total_httperrors_binary = self.total_httperrors_binary + 1
            if i["response_status_code_binary"] == 200:
                self.total_200s = self.total_200s + 1
            elif i["response_status_code_binary"] == 201:
                self.total_201s = self.total_201s + 1
            elif i["response_status_code_binary"] == 204:
                self.total_204s = self.total_204s + 1
            elif i["response_status_code_binary"] > 399 and i["response_status_code_binary"] < 500:
                self.total_4xxs = self.total_4xxs + 1
            elif i["response_status_code_binary"] > 499:
                self.total_5xxs = self.total_5xxs + 1
            else:
                self.total_unanticipated_responses = self.total_unanticipated_responses + 1