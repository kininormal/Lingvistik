import re

def normalize_text(text):
    """Gør forskellige linjeskift ens."""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    return text
def clean_text(text):
   """Rydder linjeskift og retter almindelige UTF-8/Windows-1252
    encoding-fejl fra Gutenberg-tekst."""
   text = normalize_text(text)
   """Rydder op i teksten (fofatter markeringer af fx tankepauser talestrøm)."""
   text = text.replace("_", " ") # eg jame ausin uses _ insted of blank to indicate words said with litte pause between them in some works
   text = text.replace("--", "  ") # eg jame ausin uses --  to indicate renovation pause
   # Alle former for linjeskift erstattes med mellemrum
   text = text.replace("\n", " ")

    # Flere whitespace-tegn reduceres til ét mellemrum
   text = re.sub(r"\s+", " ", text)
  
   return text.strip()