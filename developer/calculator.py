import traceback
class Calculator:
    last_res = None

#тз


    def sum(self, n1, n2):
        self.last_res = n1+n2

    def division(self, n1, n2):
        try:
            res = n1/n2
            self.last_res = res
            return res
        except:
            traceback.print_exc()
    def print_last_res(self):
        print(self.last_res)

