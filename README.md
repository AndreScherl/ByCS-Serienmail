# Tool zum Versenden von Serienmails mit der Dienstmail der BayernCloud Schule

## Motivation
Wenn Unterrichtsverteilung, Mehrarbeitsabrechnungen oder andere persönliche Informationen versendet werden sollen, ist eine Stapelverarbeitung sehr praktisch. Die Dienstmail der BayernCloud Schule (ByCS) kann nur über den Browser verwendet werden und somit ist der Weg einer Serienmail mit einem E-Mail-Programm nicht möglich. Dieses Programm hilft hier weiter, indem es den Browser fernsteuert und alle Schritte automatisiert durchführt, so dass jeder Empfänger seine individuelle E-Mail mit eigenem Anhang erhält.

## Verwendung
Sie brauchen eine csv-Datei, die die Felder _Vorname_, _Nachname_ und _Email_ enthält (vgl. empfaenger.csv). Das Trennzeichen muss ein Semikolon _;_ sein und die Kodierung der Datei _UTF-8_. Falls auch PDF-Anhänge versendet werden sollen, müssen die Dateien nach dem Schema _vorname.nachname.pdf_ benannt werden und in einem Verzeichnis liegen.
Im Text der E-Mail können die Platzhalter _{Vorname}_ und _{Nachname}_ verwendet werden, um die Empfänger individuell anzusprechen.

Starten Sie nun das Programm (die Exe-Datei liegt im Ordner _dist_) und füllen Sie die Felder der Eingabemaske aus. Anschließend drücken Sie auf _Start_ und warten bis sie eine Erfolgsmeldung erhalten.

## Fehlermeldungen
Sollte ein Fehler auftreten, wäre es hilfreich, wenn Sie die Fehlermeldung kopieren und hier in einem neu angelegten Issue posten.