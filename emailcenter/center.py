import email.message as message
import email.policy as policy
import email.utils as utils
import mimetypes
import re


class EmailBuilder:

    def __init__(self):
        self.msg = message.EmailMessage(policy.SMTP)

    def add_send_to(self, name):
        self.msg["To"] = name

    def add_author(self, name):
        self.msg["From"] = name

    def add_subject(self, name):
        self.msg["Subject"] = name

    def add_date(self):
        self.msg["Date"] = utils.formatdate(localtime=True)

    def add_id(self):
        self.msg["Message-ID"] = utils.make_msgid()

    def send_content(self, content, sub_type="plain"):
        self.msg.set_content(content, subtype=sub_type)

    def add_image(self, filename):
        cid = utils.make_msgid()
        self.msg.set_content("Thello", subtype="html")
        self.msg.add_related("", "image", self.file_type(filename), cid=cid, filename=filename)
        self.msg.add_alternative("HI")

    def add_file(self, filename):
        mime, encoding = mimetypes.guess_type(filename)
        if encoding or (mime is None):
            mime = "application/octet-stream"
        main, sub = mime.split("/")
        if main == "text":
            with open(filename, encoding="utf8") as f:
                text = f.read()
            filename = re.findall("/([\w\d]+?.[\w\d]+?)$",filename)[0]
            self.msg.add_attachment(text, sub, filename=filename)
        else:
            with open(filename, "rb") as f:
                data = f.read()
            filename = re.findall("/([\w\d]+?.[\w\d]+?)$",filename)[0]
            self.msg.add_attachment(data, main, sub, filename=filename)

    def file_type(self, file):
        if isinstance(file, str):
            filename = re.findall("/([\w\d]+?.[\w\d]+?)$", file)
            types = filename[0]
            return types[types.index(".") + 1:]

    def build_as_bytes(self):
        return self.msg.as_bytes()

    def build_as_string(self):
        return self.msg.as_string()


if __name__ == '__main__':
    e = EmailBuilder()
    e.add_send_to('123@qq.com')
    e.add_author("Test <sender@qq.com>")
    e.add_subject('Test msg')
    e.add_date()
    e.add_id()
    e.send_content("Hello")
    e.add_file("/Users/venmosnake/Documents/SeleniumAutoTest/case.xlsx")
    # print(e.file_type("/user/linux.gz"))
    print(e.build_as_string())
