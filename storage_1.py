import yadisk
import os
from dotenv import load_dotenv

load_dotenv()

class Storage():
    def __init__(self):
        self.disc = yadisk.YaDisk(token=os.getenv('TOKEN'))

    def upload_file(self, file_name, id_object ):
        t = file_name.split(".")[1]
        if self.disc.exists(f"/{id_object}"):
            number = len(list(self.disc.listdir(f"/{id_object}")))
            self.disc.upload(file_name, f"/{id_object}/{number}.{t}")
            #print(len(list(self.disc.listdir("/Загрузки"))))
        else:
            self.disc.mkdir(f"/{id_object}")
            self.disc.upload(file_name, f"/{id_object}/0.{t}")
        #self.disc.download(file_name, "text.txt")

    def download_file(self, id_object):
        number = len(list(self.disc.listdir(f"/{id_object}")))
        for i in range(0, number):
            try:
                self.disc.download(f"/{id_object}/{i}.txt", f"{i}.txt")
            except:
                os.remove(f"{i}.txt")
                try:
                    self.disc.download(f"/{id_object}/{i}.jpeg", f"{i}.jpeg")
                except:
                    pass
                    os.remove(f"{i}.jpeg")

    def get_link(self):
        l = list(self.disc.listdir(f"/1"))
        # l = str(l[0]).split("<ResourceObject")[1]
        # l = l.split(">")[0]
        # l = l.replace("'", '"')
        l = str(l[0]).split("'file': '")[1]
        l = l.split("'")[0]
        print(l)
        # l = l['file']
        # print(l)

# if __name__ == "__main__":
#     disk = Storage()
#     #disk.upload_file("4.jpeg", 2)
#
#     #disk.download_file(1)
#     disk.get_link()

