#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp
import urllib
import socket

dicc_cache = {}

class cache_contenidos(webapp.webApp):

    def parse(self, request):

        URL = request.split()[1][1:].split('/')[0]
        cabeceras = request.split('\r\n', 1)[1]
        try:
            recurso = request.split()[1][1:].split('/')[1]
        except IndexError:
            recurso = ""

        return (URL, cabeceras, recurso)

    def process(self, parsedRequest):

        URL, cabeceras, recurso = parsedRequest;

        url = "http://" + URL
        proxy = "http://localhost:1234/" + URL
        links = ("<center><a href= '" + url + "'>Original webpage</a> | " +
                    "<a href= '" + proxy + "'>Reload</a> | " +
                    "<a href= '" + proxy + "/cache'>Cache</a> | " +
                    "<a href= '" + proxy + "/cabeceras1'>Cabeceras 1</a></center>")

        try:
            f = urllib.urlopen(url)
        except IOError:
            HttpCode = "400 Not Found"
            HtmlResponse = "<html><body><h1> Error. Pagina no encontrada.</h1></body></html>"
            return(HttpCode, HtmlResponse)
        
        if recurso == "cabeceras1":
            HttpCode = "200 OK"
            HtmlResponse = "<html><body>" + links + cabeceras + "</body></html>"
        elif recurso == "cache":
            try:
                HttpCode = "200 OK"
                HtmlResponse = dicc_cache[url]
            except KeyError:
                HttpCode = "400 Not Found"
                HtmlResponse = "<html><body><h1> Error. Pagina no encontrada en la cache.</h1></body></html>"
                return(HttpCode, HtmlResponse)
        else:
            html = f.read()
            dicc_cache[url] = html
            pos = html.find('<body>')
            pos_good = html.find(">", pos)
            html_mod = (html[:pos_good+1] + links + "\r\n\r\n" + html[(pos_good+1):])
        
            HttpCode = "200 OK"
            HtmlResponse = html_mod

        return(HttpCode, HtmlResponse)

if __name__ == "__main__":
    server = cache_contenidos("localhost", 1234)
