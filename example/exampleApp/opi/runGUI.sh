#!/bin/bash
. /home/tools/bin/changeports 6064
EDMDATAFILES=.:/dls_sw/work/R3.14.8.2/support/CryoconM14/data
#EDMDATAFILES=.:../../../CryoconM14App/opi/edl
export EDMDATAFILES
edm -x -eolc -m "device=TS-ID-TMON-01" M14.edl &

