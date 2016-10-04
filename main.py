#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2016  Jan Vorwerk
#
#    This file is part of 'meos2ffco'
#
#    meos2ffco is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>. 
import codecs
import logging

_logger = logging.getLogger(__name__)

SEP = ';'
USE_CAT_AS_CIRCUIT = False

HEADERS=[
    'N° dép.',
    'Puce',
    'Ident. base de données',
    'Nom',
    'Prénom',
    'Né',
    'S',
    'Plage',
    'nc',
    'Départ',
    'Arrivée',
    'Temps',
    'Evaluation',
    'N° club',
    'Nom',
    'Ville',
    'Nat',
    'N° cat.',
    'Court',
    'Long',
    'Num1',
    'Num2',
    'Num3',
    'Text1',
    'Text2',
    'Text3',
    'Adr. nom',
    'Rue',
    'Ligne2',
    'Code Post.',
    'Ville',
    'Tél.',
    'Fax',
    'E-mail',
    'Id/Club',
    'Louée',
    'Engagement',
    'Payé',
    'Circuit N°',
    'Circuit',
    'km',
    'm',
    'Postes du circuit',
    'Pl',
    ]

def _formatTime(seconds, offset=0):
    '''Returns the formatted time from a number of seconds, if offset is specified, it is used only if seconds > 0
    
    >>> formatTime(0, 0)
    ''
    >>> formatTime(1, 0)
    '00:00:01'
    >>> formatTime(90, 0)
    '00:01:30'
    >>> formatTime(14399, 0)
    '03:59:59'
    >>> formatTime(0, 21600)
    ''
    >>> formatTime(10, 21600)
    '06:00:10'
    '''
    if seconds == 0:
        return ''
    m, s = divmod(seconds+offset, 60)
    h, m = divmod(m, 60)
    return '%02d:%02d:%02d' % (h, m, s)    

def _parseTime(s):
    '''Returns the number of seconds from a time string
    
    >>> parseTime('')
    0
    >>> parseTime('1')
    1
    >>> parseTime('30')
    30
    >>> parseTime('1:30')
    90
    >>> parseTime('01:30')
    90
    >>> parseTime('59:59')
    3599
    >>> parseTime('1:00:00')
    3600
    >>> parseTime('1:0:0')
    3600
    >>> parseTime('3:59:59')
    14399
    '''
    components = s.split(':')
    seconds = 0 
    for i, val in enumerate(reversed(components)):
        if val:
            seconds += pow(60,i) * int(val)
    return seconds

def parseFfcoArchive(inputFileName):
    ret = dict()
    with codecs.open(inputFileName, 'r', encoding='cp1252') as inputFile:
        for i, line in enumerate(inputFile.readlines()):
            if i > 0:
                _logger.debug('Reading line %d', i)
                fields = line.split(SEP)
                licenseNum = fields[0]
                lastName = fields[2]
                firstName = fields[3]
                ret[licenseNum] = dict(firstName=firstName, lastName=lastName)
    return ret


def parseMeos(ffco, inputFileName, outputFileName):
    with codecs.open(outputFileName, 'w', encoding='cp1252') as outputFile:
        with codecs.open(inputFileName, 'r', encoding='cp1252') as inputFile:
            outputFile.write(SEP.join(HEADERS))
            outputFile.write('\r\n')
            for i, line in enumerate(inputFile.readlines()):
                if i > 0:
                    _logger.debug('Reading line %d', i)
                    fields = line.split(SEP)
                    evaluation = int(fields[12])
                    if evaluation != 1: # absent

                        # MeOS has one single field for first name and surname,
                        # therefore we lookup the FFCO archive to retrieve the proper fields
                        # so that "Jean DU PONT" does not split up as "Jean DU" / "PONT"
                        licenseNum = fields[2]
                        if licenseNum in ffco:
                            fields[4], fields[3] = ffco[licenseNum]['firstName'], ffco[licenseNum]['lastName'],
                        else:
                            fields[3], fields[4] = fields[4], fields[3]

                        # NC column is missing
                        fields[8] = '0' if evaluation == 0 else 'X'

                        # time < 1h have missing hours
                        if fields[11] == '–':
                            fields[11] = ''
                        else:
                            fields[11] = _formatTime(_parseTime(fields[11]))
                        
                        # When there are circuit variations (mass-start) the MeOS circuit holds the variation
                        if USE_CAT_AS_CIRCUIT:
                            fields[38] = fields[17]
                            fields[39] = fields[18]

                        # write to outputFile
                        outputFile.write(SEP.join(fields))

if __name__ == '__main__':
    import sys
    ffco = parseFfcoArchive(sys.argv[1])
    parseMeos(ffco=ffco, inputFileName=sys.argv[2], outputFileName=sys.argv[3])
