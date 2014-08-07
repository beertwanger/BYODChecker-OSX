import kivy

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from scapy.all import *

class Controller(FloatLayout):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''
    label_wid = ObjectProperty()
    button_wid = ObjectProperty()
    wifi_wid = ObjectProperty()
    ping_wid = ObjectProperty()
    dns_wid = ObjectProperty()
    http_wid = ObjectProperty()
    info = StringProperty()

    def do_action(self):

        def wifi_UP():
            wifi = 'DOWN'
            from subprocess import check_output
            words = (check_output(["ifconfig", "-a"])).split()
            for index in range(len(words)):
                if (words[index] == 'en1:'):
                    if (words[index+1].find("UP")):
                        wifi = 'UP'
            return wifi

        def default_gateway():
            gateway = 'None'
            from subprocess import check_output
            words = (check_output(["netstat", "-rn"])).split()
            for index in range(len(words)):
                if (words[index] == 'default'):
                    gateway = words[index+1]
            return gateway

        def ping_gateway(gw):
            ping = IP(dst=gw)/ICMP()
            reply = sr1(ping, timeout=1)
            if not (reply is None):
                return 'Gateway OK'
            else:
                return 'Gateway not reachable'

        def nameserver():
            dns = 'Fail'
            from subprocess import check_output
            words = (check_output(["cat", "/etc/resolv.conf"])).split()
            for index in range(len(words)):
                if (words[index] == 'nameserver'):
                    dns  = words[index+1]
                    query = IP(dst=dns)/UDP()/DNS(rd=1,qd=DNSQR(qname="www.bbc.co.uk"))
                    reply = sr1(query, timeout=1)
                    if (DNS in reply) and (reply.rcode==0L):
                        dns = 'DNS OK'
            return dns


        def httpGet():
            syn = IP(dst='www.bbc.co.uk')/TCP(dport=80, flags='S')
            syn_ack= sr1(syn,timeout=1)
            getStr = 'GET / HTTP/1.1\r\nHost: www.bbc.co.uk\r\n\r\n'
            request = IP(dst='www.bbc.co.uk')/TCP(dport=80,sport=syn_ack[TCP].dport,seq=syn_ack[TCP].ack,ack=syn_ack[TCP].seq+1,flags='A')/getStr
            reply = sr1(request,timeout=1)
            
            if (TCP in reply and reply[TCP].seq==syn_ack[TCP].seq+1):
                return 'http OK.'
            else:
                return 'bad response.'

        if (self.button_wid.state == 'down'):
            self.label_wid.text = 'Starting test...'
            self.button_wid.background_color = 3,0,0,1
            #
            # Check wifi signal
            #
            wifi = wifi_UP()
            if (wifi=='UP'):
                self.wifi_wid.background_color = 0,2,0,1
            else:
                self.wifi_wid.background_color = 2,0,0,1
            #
            # Ping default gateway
            #
            ping = 'Failed'
            if (wifi=='UP'):
                gateway = default_gateway()
                if (gateway=='None'):
                    self.ping_wid.background_color = 2,0,0,1
                else:
                    ping = ping_gateway(gateway)
                if (ping  == 'Gateway OK'):
                    self.ping_wid.background_color = 0,2,0,1
                else:
                    self.ping_wid.background_color = 2,0,0,1
            #
            # Query DNS
            #
            ns = 'Fail'
            if (ping == 'Gateway OK'):
                ns = nameserver()
                if (ns == 'DNS OK'):
                    self.dns_wid.background_color = 0,2,0,1
                else:
                    self.dns_wid.background_color = 2,0,0,1
            #
            # Send HTTP GET
            #
            if (ns == 'DNS OK'):
                http = httpGet()
                if (http == 'http OK.'):
                    self.http_wid.background_color = 0,2,0,1
                    self.button_wid.background_color = 0,1,0,1
                else:
                    self.http_wid.background_color = 2,0,0,1
                    self.buttons_wid.background_color = 2,0,0,1
            self.label_wid.text = 'Finished'
        else:
            self.label_wid.text = 'Stopped'
            self.button_wid.background_color = 0.59,0.59,0.59,1
            self.wifi_wid.background_color = 0.59,0.59,0.59,1
            self.ping_wid.background_color = 0.59,0.59,0.59,1
            self.dns_wid.background_color = 0.59,0.59,0.59,1
            self.http_wid.background_color = 0.59,0.59,0.59,1
        self.info = 'New info text'

class ControllerApp(App):

    def build(self):
        return Controller(info='Hello world')

if __name__ == '__main__':
    ControllerApp().run()
