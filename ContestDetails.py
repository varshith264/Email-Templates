from datetime import datetime
from lxml import html
from bs4 import BeautifulSoup
import requests

# now simply create an object of ContestDetails passing URL as argument and you can access all the details of contest 
# Contest times are specified in 24hr format.
# as an example
# Contest = ContestDetails('https://vjudge.net/contest/441295')
# Contest.print_details()

class ContestDetails:
    URL='?'
    def __init__(self,url):
        self.Name='?'
        self.Type = '?'
        self.Number='?'
        self.Date = '?'
        self.StartTime = '?'
        self.EndTime = '?'
        self.Duration = '?'
        self.URL = url
        self.scrape()
    
    def print_details(self):
        print('Name: '+ self.Name)
        print('Type' + ': ' + self.Type)
        print('Number' + ': ' + self.Number)
        print('Date' + ': ' + self.Date )
        print('StartTime' + ': ' + self.StartTime)
        print('EndTime' + ': ' + self.EndTime)
        print('Duration' + ': ' + self.Duration)
        print('Contest Link: ' + self.URL)

    def time_diff(self,s1, s2):
        time1 = int(s1[0:2]) * 60 + int(s1[3:5])
        time2 = int(s2[0:2]) * 60 + int(s2[3:5])
        minutes = 0
        if (s1 <= s2):
            minutes = time2 - time1
        else:
            total = 24 * 60
            minutes = total - time1 + time2
        hours = minutes // 60
        minutes -= hours * 60
        result = str(hours) + ':'
        if (minutes < 10):
            result += '0' + str(minutes)
        else:
            result += str(minutes)

        return result 

    def scrape(self):
        r = requests.get(self.URL).text
        soup = BeautifulSoup(r, 'lxml')
        article = soup.find('h3')
        s = article.text

        contest = ''
        prev = '-1'

        for i in range(63,len(s)):
            if prev==' ' and prev == s[i]:
                break
            else:
                contest = contest + s[i]
            prev = s[i]

        contest = contest.upper().strip()
        self.Name = contest

        times = []
        t=0

        for span in soup.find_all('span'):
            times.append(int(span.text[:10]))
            t += 1
            if (t == 2):
                break

        info = []

        for timestamp in times:
            dt_object = datetime.fromtimestamp(timestamp)
            temp = ''
            dt_object = str(dt_object)
            for i in dt_object:
                if (i == ' '):
                    info.append(temp)
                    temp = ''
                else:
                    temp += i
            info.append(temp)

        self.Date = info[0]
        self.StartTime = info[1]
        self.EndTime = info[3]

        num = ''
        flag = True

        if (contest.find('#') != -1):
            for i in range(contest.index('#')+1,len(contest)):
                num += contest[i]

            self.Number = num

        if (contest.find('MIRROR') != -1 or contest.find('ICPC') != -1):
            self.Type = 'ICPC MIRROR'
        elif (contest.find('BEGINNER') != -1):
            self.Type = 'BEGINNER CONTEST'

        self.Duration = (self.time_diff(info[1], info[3]))+' hrs'



