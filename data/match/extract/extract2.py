__author__ = 'sleep'
__author__ = 'sleep'
import re
import os


class Extract(object):
    def __init__(self,dir_read,dir_write):
        self.dir_read = dir_read
        self.dir_write = dir_write

    def write_to_file(self):
        list = os.listdir(dir_read)
        for file in list:
            if not file.startswith("E0"):
                continue
            with open(dir_read + "/" + file, "r") as f_read:
                with open(dir_write + "/" + file + ".txt", "w") as f_write:
                    raw_txt = f_read.read()
                    parsed_txt = self.parse(raw_txt,file)
                    f_write.write("<title>")
                    f_write.write(self.parse_title(raw_txt,file) + "</title>")
                    f_write.write("\n"+"<content>" + "\n")
                    f_write.write(parsed_txt + "</content>")

    def parse_title(self,txt,file_name):
        m_title = re.search("main-headline\"\>(.*?)\<\/",txt)
        if m_title:
            return m_title.group(1)
        else:
            print "title not found" + file_name
            return ""

    def parse(self,txt,file):
        return self.parse_strong(txt,file) + self.parse_between_share_button(txt,file)

    def parse_between_share_button(self,txt,file):
        m = re.search("share-buttons\"\>(.*)\<ul class=\"-share-buttons\"\>",txt,re.DOTALL)
        if m:
            return self.parse_between_p(m.group(1))
        else:
            return ""
            print file + "share-button not found"

    def parse_between_p(self,txt):
        content = ""
        list_match = re.findall("\<p\>(.*?)\<\/p\>",txt)
        for match in list_match:
            content += self.delete_p(match) + "\n"
        if content != "":
            return self.delete_p(content)
        else:
            print self.parse_title + "t not found"
            print ""

    def parse_strong(self,text,file):
        """return content start with <p class="v5-txt-strong">"""
        m_strong = re.search("v5-txt-strong\"\>(.*?)\<\/p\>",text,re.DOTALL)
        if m_strong:
            return self.delete_p(m_strong.group(1) + "\n")
        else:
            print "strong not found" + file
            return ""


    def delete_p(self,text):
        """delete <p> and </p> <>in content"""
        delete_p1 = re.sub("\<\/?strong\>"," ",text)
        delete_p2 = re.sub("\<\/?em\>","",delete_p1)
        return self.delete_h5(delete_p2)

    def delete_h5(self,text):
        delete = re.sub("\<h5\>.*?\<\/h5\>","",text)
        return self.delete_non_char(delete)

    def delete_non_char(self,text):
        """delete $#1111; in content"""
        deleted = re.sub("&#[0-9]*;","",text)
        return deleted

def ExtractAll(object):
    list = os.listdir()

if __name__ == '__main__':
    cwd = os.getcwd()
    dir_read = cwd + "/html_files"
    dir_write = cwd + "/txt_files"
    extract_from = Extract(dir_read,dir_write)
    extract_from.write_to_file()
    # with open("E0_01_01_15_Aston_Villa","r") as file_read:
    #     txt = file_read.read()
    #     m = re.search("share-buttons\"\>(.*)\<ul class=\"-share-buttons\"\>",txt,re.DOTALL)
    #     if m:
    #         return self.parse_between_p(m.group(1))

