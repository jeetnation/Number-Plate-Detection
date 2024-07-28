import smtplib #pip install smtplib
import email_pass
import random #pip install random
import string

class sent_email:
    def __init__(self, to_):
        self.to_ = to_
        self.s = smtplib.SMTP('smtp.gmail.com', 587)
        self.s.starttls()
        self.email_ = email_pass.email_
        self.pass_ = email_pass.pass_
        self.s.login(self.email_, self.pass_)


    def Random_OTP(self, length):
        upper = string.ascii_uppercase
        num = string.digits
        all = upper + num

        temp = random.sample(all, length)
        password = "".join(temp)

        return password

    def Sent_mail(self, otp):
        subj = 'Reset Password OTP'
        msg = f'Dear Sir/Maam, \n\nYour Reset OTP is {str(otp)}.\n\nwith Regards,\nMall of India'
        msg = "Subject:{}\n\n{}".format(subj, msg)
        self.s.sendmail(self.email_, self.to_, msg)

        chk = self.s.ehlo()

        if chk[0] == 250:
            return 's'
        else:
            return 'f'