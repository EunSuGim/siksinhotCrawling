import pandas as pd

class DBConnect :

    def saveCsv(self, results):
        df = pd.DataFrame(results)
        df.to_csv('./data/susi.csv', index=False)

        print("csv데이터 저장완료")