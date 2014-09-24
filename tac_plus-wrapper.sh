#!/bin/bash

exec /usr/bin/tac_plus -C ${CONFIG} ${LOGFILE:+-l $LOGFILE}  ${WHOLOG:+-w $WHOLOG} ${DEBUG_LEVEL:+-d $DEBUG_LEVEL}
