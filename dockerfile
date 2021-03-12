FROM centos
WORKDIR /project
RUN > /project/sent.txt
RUN > /project/visited.txt
RUN yum update -y
RUN yum install -y python3
RUN pip3 install ipython
RUN pip3 install selenium
RUN pip3 install parsel
RUN pip3 install bs4
RUN yum install -y /project/google-chrome-stable_current_x86_64.rpm
RUN pip3 install beautifulsoup4
ENTRYPOINT ["python3","/project/linkedintest.py"]
