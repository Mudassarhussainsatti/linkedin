FROM centos
WORKDIR /project
RUN yum update -y
RUN yum install -y python3
RUN pip3 install ipython
RUN pip3 install selenium
RUN pip3 install parsel
RUN pip3 install bs4
RUN pip3 install beautifulsoup4
ADD google-chrome-stable_current_x86_64.rpm /project/google-chrome-stable_current_x86_64.rpm
ADD linkedintest.py /project/linkedintest.py
ADD sent.txt /project/sent.txt
ADD visited.txt /project/visited.txt
ADD chromedriver /project/chromedriver
RUN yum install -y google-chrome-stable_current_x86_64.rpm
ENTRYPOINT ["python3","/project/linkedintest.py"]
