ENTRY
  { author title year journal volume number pages publisher booktitle editor }

FUNCTION {article}
{ output.bibitem
  "[" cite$ "]" write$
  author format.names write$
  ", \"" title * "\"," write$
  journal write$
  ", vol. " volume write$
  ", no. " number write$
  ", pp. " pages write$
  ", " year write$
}

FUNCTION {book}
{ output.bibitem
  "[" cite$ "]" write$
  author format.names write$
  ", " title write$
  ", " publisher write$
  ", " year write$
}

FUNCTION {inproceedings}
{ output.bibitem
  "[" cite$ "]" write$
  author format.names write$
  ", \"" title * "\"," write$
  booktitle write$
  ", " year write$
}
