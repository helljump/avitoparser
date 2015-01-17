!define PROGNAME "zipta avito parser"
OutFile "c:\Users\snoa\YandexDisk\софт\zipta-avito-dist.exe"

!include "MUI2.nsh"
!include "FileFunc.nsh"
!define MUI_WELCOMEPAGE_TITLE_3LINES

Name "${PROGNAME}"
WindowIcon on
Icon "aaaa32.ico"
XPStyle on
SetCompressor /SOLID lzma
InstallDir ""
RequestExecutionLevel user

!define MUI_ABORTWARNING
!define MUI_WELCOMEPAGE_TITLE "Добро пожаловать в установщик ${PROGNAME}"
!define MUI_WELCOMEPAGE_TEXT "По вопросам поддержки обращайтесь на: http://zipta.ru/contact/ либо ICQ 125521555"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "docs\license.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "Russian"

Section ""
    SetOutPath $INSTDIR
    File /r /x *.pyc /x *.py build\exe.win32-2.7\*.*
SectionEnd
