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
                    parsed_txt = self.parse(raw_txt)
                    f_write.write("<title>:")
                    f_write.write(self.parse_title(raw_txt) + "\n")
                    f_write.write("\n"+"<content>:" + "\n")
                    f_write.write(parsed_txt)

    def parse_title(self,txt):
        m_title = re.search("main-headline\"\>(.*?)\<\/",txt)
        if m_title:
            return m_title.group(1)
        else:
            print "title not found"
            return ""


    def parse(self,text):
        return self.parse_strong(text) + self.parse_widget(text)

    def parse_strong(self,text):
        """return content start with <p class="v5-txt-strong">"""
        m_strong = re.search("\<p class\=\"v5-txt-strong\">(.*?)\<div",text)
        if m_strong:
            only_p = m_strong.group(1)
            m_only_p = re.search("(.*)\<\/p\>",only_p)
            if m_only_p:
                 return self.delete_p(m_only_p.group(1))
        else:
            return " "

    def parse_widget(self,text):
        m_widget = re.findall("\<\/widget\>(.*?)\n?\<\/?[du]",text)
        if m_widget:
            new_string = ""
            for m_string in m_widget:
                new_string += m_string
            return self.delete_p(new_string)
        else:
            return " "

    def delete_p(self,text):
        """delete <p> and </p> <>in content"""
        delete_p = re.sub("\<\/?p\>","\n",text)
        delete_p2 = re.sub("\<\/?strong\>"," ",delete_p)
        delete_p3 = re.sub("\<\/?em\>","",delete_p2)
        return self.delete_h5(delete_p3)

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
    dir_read = cwd + "/html_files_14_15"
    dir_write = cwd + "/txt_files_14_15"
    extract_from = Extract(dir_read,dir_write)
    extract_from.write_to_file();

