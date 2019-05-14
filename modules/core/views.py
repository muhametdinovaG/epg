# coding: utf-8
import os
import xml.etree.ElementTree as ET

from django.conf import settings
from django.http import HttpResponse
from modules.core.models import *


def create_xml(request):

    if not Channel.main_channel:
        return

    # header = ('<?xml version="1.0" encoding="windows-1251"?> <!DOCTYPE tv SYSTEM "xmltv.dtd">')
    tv = ET.Element("tv")

    channels = Channel.objects.filter(display=True).all()
    for channel in channels:
        id_ch = str(channel.id_channel)
        channel_name = str(channel.name)
        icon = str(channel.icon)

        chanel = ET.SubElement(tv, "channel", id=id_ch)
        ET.SubElement(chanel, "display-name", lang="ru").text = channel_name
        ET.SubElement(chanel, "icon", src=icon)

    programs = Program.objects.filter(channel_id=channel.id).all()
    for program in programs:
        channel_id = str(program.channel_id)
        broadcast_name = str(program.broadcast_name)
        description = str(program.description)
        date = str(program.date)
        broadcast_start = str(program.broadcast_start).replace(' ', '')
        broadcast_end = str(program.broadcast_end).replace(' ', '')
        category_id = str(program.category_id)
        dvb_id = str(program.dvb_name_id)

        categoryes = Category.objects.all().filter(id=category_id)
        for category in categoryes:
            cat = str(category.name)
            if category.name is not None:
                category_name = str(category.name)
            else:
                genres = DvbGenre.objects.all().filter(id=dvb_id)
                for genre in genres:
                    category_name = str(genre.name)

        program = ET.SubElement(
            # header,
                                tv, "programme",
                                start=broadcast_start.replace('-', '').replace(':', '').replace('+', ' +'),
                                stop=broadcast_end.replace('-', '').replace(':', '').replace('+', ' +'),
                                channel=channel_id)

        ET.SubElement(program, "title", lang="ru").text = broadcast_name
        ET.SubElement(program, "desc", lang="ru").text = description
        ET.SubElement(program, "category", lang="ru").text = category_name

    tree = ET.ElementTree(tv)
    tree.write(os.path.join(settings.MEDIA_ROOT, "epg.xml"))

    response = HttpResponse(open(settings.MEDIA_ROOT + '/epg.xml').read())
    response['Content-type'] = 'text/xml'

    return response
