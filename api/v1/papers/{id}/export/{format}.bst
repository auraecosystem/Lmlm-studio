ENTRY
  { author title year journal volume number pages publisher booktitle editor }

FUNCTION {article}
{ output.bibitem
  author format.names write$
  " (" year * ")" write$
  ". " title write$
  ". " journal write$
  ", " volume write$
  "(" number * ")" write$
  ", " pages write$
  "."
}

FUNCTION {workbook}
{ output.bibitem
  author format.names write$
  " (" year * ")" write$
  ". " title write$
  ". " publisher write$
  "."
}

FUNCTION {inproceedings}
{ output.bibitem
  author format.names write$
  " (" year * ")" write$
  ". " title write$
  ". In " editor format.names write$
  " (Ed.), " booktitle write$
  " (pp. " pages write$ ")."
}
