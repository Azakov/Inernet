��������� 4 �������� �� vars(a) - ��������� ��� ������ ������� ������, ��������� ���
Origin Timestamp - ����� ����� ������ �������� ������� ������
Receive Timestamp - ����� ����� ������ ������� ������
Transmit Timestamp - ����� ����� ������ ���������� ������
dest_timestamp - ����� ����� ntp �������� ������� ������

������ ������� � cmd:
>>> import ntplib
>>> c = ntplib.NTPClient()
>>> a = c.request("127.0.0.1") ��� a = c.request("127.0.0.1", port = 6000)
>>> vars(a) 

������ �������:
py server.py -s 100 - �������� ���� �� 100 ������