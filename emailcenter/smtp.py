import smtplib
import socket
import ssl

from emailcenter import center
import config

email_template = ""
if config.email["use_email"]:
    with open("emailcenter/file.temp") as f:
        email_template = "".join(f.readlines())


class STMPSender:

    def __init__(self):
        self.builder = center.EmailBuilder()
        self.server = config.email["stmp_server_addr"]
        self.author = config.email["author"]
        self.to = config.email["recv_email"]
        self.msg = config.email["message"]
        self.title = config.email["title"]

    def build_email(self, context):
        self.builder.add_send_to(self.to)
        self.builder.add_author(self.author)
        self.builder.add_subject(self.title)
        self.builder.add_date()
        self.builder.add_id()
        self.builder.add_file(config.report["report_file_path"])
        self.builder.send_content(context)

    def content(self):
        with open(config.report["report_file_path"]) as f:
            pass

    def send_with_tls(self):
        conn = smtplib.SMTP(self.server)
        try:
            self.__send_message_securely(conn)
        except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as e:
            print(e.smtp_error.decode("utf8"))

    def __send_message_securely(self, conn):
        #  发送ehlo命令，如果服务器不支持ehlo也不会支持tls
        code = conn.ehlo()[0]
        # smtp服务器返回的结果代码，在200-2999之间表示成功，其他代码都是表示失败
        use = (200 <= code <= 299)
        if not use:
            code = conn.helo()[0]
            if not (200 <= code < 299):
                print("Remove server refused helo code :", code)
        if use and conn.has_extn("starttls"):
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.set_default_verify_paths()
            context.verify_mode = ssl.CERT_REQUIRED
            conn.starttls(context=context)
            code = conn.helo()[0]
            if not (200 <= code < 299):
                print("Error: ", code)
        else:
            print("server not support tls,using normal connection")
        try:
            conn.login(config.email["username"], config.email["password"])
        except smtplib.SMTPException as e:
            print(e.args)
        conn.sendmail(self.author, self.to, self.msg)
