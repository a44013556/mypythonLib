import csv

class BaseCsvReader:
  
  field_types : Dict[str, Any] = {}
  candidate_encoding = ['utf-8-sig', 'utf-8', 'shift_jis', 'cp932']
  encoding = ""
  with_header = True
  
  def __init__(self, file_path: str, with_header = True, header = []):
    self.file_path = file_path
    self.headers = header
    self.with_header = with_header
  
  def read_all(self) -> List[Dict[str,Any]]:
    results = []
    encode = self._detect_encoding()

    with open(self.file_path, mode = "r", encoding=encode, errors = 'replace') as f:
      if not self.with_header and not self.headers:
        sample = next(csv.reader(f),None)
        f.seek(0)
        if sample:
          self.headers = [f"column_{i+1}" for i in range(len(sample))]
      if self.with_header:
        reader = csv.DictReader(f)
      else:
        reader = csv.DictReader(f, fieldnames=self.headers)
      for row in reader:
        processed_row = self._process_row(row)
        results.append(processed_row)
    return results
  
  def getEncoding(self):
    return self.encoding
  
  def _detect_encoding(self):
    for enc in self.candidate_encoding:
      try:
        with open(self.file_path, "r", encoding=enc) as f:
          f.read(1024)
        self.encoding = enc
        return enc
      except UnicodeDecodeError:
        continue
    self.encoding = 'utf-8'
    return 'utf-8'
  def _process_row(self, row: Dict[str, str]) -> Dict[str, Any]:
    new_row = {}
    for key, value in row.items():
      transform = self.field_types.get(key)
      try:
        new_row[key] = transform(value) if transform and value else value
      except ValueError:
        new_row[key] = None
    return new_row

class tempCsvReader(BaseCsvReader):
  field_types = {}
  with_header = False