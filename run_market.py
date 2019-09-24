from series import Series

#Main Run Thread
class Run_Market:
    
    def run(self):

        print(Series().fetch_series('nasdaq', 'AAPL'))
        
Run_Market().run()
