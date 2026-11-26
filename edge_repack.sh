#!/bin/bash
SRC_PACK=`ls *.exe`
if [ -f "$SRC_PACK" ]; then
  DST_PACK=${SRC_PACK:0:17}_Laster.7z
  if [ -f "MSEDGE.7z" ]; then
    rm -f "MSEDGE.7z"
  fi
  if [ -d Chrome-bin ]; then
    rm -rf Chrome-bin
  fi
  if [ -d Msedge ]; then
    rm -rf Msedge
  fi
  if [ -f "$DST_PACK" ]; then
    rm -f "$DST_PACK"
  fi
  /builds/worker/fetches/7zz/7zz e "$SRC_PACK"
  if [ -f "MSEDGE.7z" ]; then
    /builds/worker/fetches/7zz/7zz x MSEDGE.7z
    if [ -d Chrome-bin ]; then
      mkdir Msedge
      mv Chrome-bin/* Msedge/App
      if [ -f "Msedge/App/msedge.exe" ] && [ -f "msedge64++.7z" ]; then
        /builds/worker/fetches/7zz/7zz x msedge64++.7z -OMsedge/App
        if [ -f "Msedge/App/injectpe.bat" ]; then
          export WINEPREFIX=/builds/worker/fetches/.wine
          /builds/worker/fetches/wine/bin/wine cmd.exe /c Msedge/App/injectpe.bat -auto
          /builds/worker/fetches/7zz/7zz a "$DST_PACK" Msedge -mx9 -t7z
          rm -d Chrome-bin
          rm -f MSEDGE.7z
          rm -f msedge64++.7z
          rm -f "$SRC_PACK"
        fi
      fi
    fi
  fi
fi
